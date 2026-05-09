#!/bin/bash
# entrypoint.sh - downloads models on first startup, then serves

echo "=== LTX-Video API starting up ==="

# Download model if not cached
MODEL_DIR=${HOME}/.cache/huggingface/hub
if [ ! -d "$MODEL_DIR" ]; then
    echo "First startup: downloading LTX-Video model..."
    python3 -c "
from ltх_video.pipeline import LTXVideoPipeline
pipe = LTXVideoPipeline.from_pretrained('Lightricks/LTX-Video', cache_dir='${MODEL_DIR}')
print('Model downloaded successfully')
" 2>&1 | head -20
fi

echo "Starting API server..."
exec "$@"
