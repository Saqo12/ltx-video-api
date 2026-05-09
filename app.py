import os
import subprocess
import json
import uuid
import threading
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# Queue for generation jobs
job_queue = []
active_job = None

def get_torch_device():
    import torch
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"

def run_generation(job_id, prompt, output_path):
    global active_job
    import torch
    from diffusers import LTXVideoPipeline
    from transformers import T5EncoderDynamic
    import numpy as np
    import PIL.Image
    
    active_job = {"id": job_id, "status": "loading_model"}
    
    try:
        device = get_torch_device()
        
        active_job["status"] = "loading_model"
        
        # Load pipeline
        pipe = LTXVideoPipeline.from_pretrained(
            "Lightricks/LTX-Video",
            torch_dtype=torch.bfloat16 if device == "cuda" else torch.float32
        )
        pipe = pipe.to(device)
        
        active_job["status"] = "generating"
        
        # Generate
        result = pipe(
            prompt=prompt,
            num_frames=41,
            num_inference_steps=40,
            guidance_scale=3.5,
            fps=24,
        )
        
        active_job["status"] = "saving"
        
        # Save frames as video using ffmpeg
        frames_dir = f"/tmp/frames_{job_id}"
        os.makedirs(frames_dir, exist_ok=True)
        
        for i, frame in enumerate(result.frames[0]):
            img = PIL.Image.fromarray(frame)
            img.save(f"{frames_dir}/{i:04d}.png")
        
        # Encode to video
        cmd = f"ffmpeg -y -framerate 24 -i {frames_dir}/%04d.png -c:v libx264 -pix_fmt yuv420p {output_path}"
        os.system(cmd)
        
        # Cleanup
        os.system(f"rm -rf {frames_dir}")
        
        active_job = {"id": job_id, "status": "done", "output": output_path}
        
    except Exception as e:
        active_job = {"id": job_id, "status": "error", "error": str(e)}

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "No prompt provided"}), 400
    
    job_id = str(uuid.uuid4())[:8]
    output_path = f"/tmp/output_{job_id}.mp4"
    
    # Run in background
    t = threading.Thread(target=run_generation, args=(job_id, prompt, output_path))
    t.start()
    
    return jsonify({"job_id": job_id, "status": "queued"})

@app.route("/status/<job_id>")
def status(job_id):
    global active_job
    if active_job and active_job["id"] == job_id:
        return jsonify(active_job)
    return jsonify({"job_id": job_id, "status": "unknown"})

@app.route("/health")
def health():
    return jsonify({"status": "ok", "gpu": get_torch_device() != "cpu"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7860)))