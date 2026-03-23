#!/usr/bin/env python3
"""
DRAMA AI STUDIO - Google Colab Setup
Run each cell in order in Google Colab
Models saved to Google Drive permanently!
"""

# ============================================================
# CELL 1 - Mount Google Drive
# ============================================================
from google.colab import drive
drive.mount('/content/drive')

import os

# All models saved here permanently on your 2TB Drive
DRIVE_MODELS = '/content/drive/MyDrive/ComfyUI_Models'
COMFY_DIR = '/content/ComfyUI'

# Create model folders on Drive (only needed once!)
folders = [
    f'{DRIVE_MODELS}/diffusion_models',
    f'{DRIVE_MODELS}/text_encoders', 
    f'{DRIVE_MODELS}/vae',
    f'{DRIVE_MODELS}/checkpoints',
    f'{DRIVE_MODELS}/clip',
    f'{DRIVE_MODELS}/clip_vision',
    f'{DRIVE_MODELS}/insightface',
    f'{DRIVE_MODELS}/facerestore_models',
]
for f in folders:
    os.makedirs(f, exist_ok=True)

print("✅ Google Drive mounted and folders ready!")
print(f"📁 Models folder: {DRIVE_MODELS}")

# ============================================================
# CELL 2 - Install ComfyUI (every session)
# ============================================================
import os
import subprocess

COMFY_DIR = '/content/ComfyUI'
DRIVE_MODELS = '/content/drive/MyDrive/ComfyUI_Models'

if not os.path.exists(f'{COMFY_DIR}/main.py'):
    print("Installing ComfyUI...")
    subprocess.run(['git', 'clone', 'https://github.com/comfyanonymous/ComfyUI.git', COMFY_DIR])
    subprocess.run(['pip', 'install', '-q', '-r', f'{COMFY_DIR}/requirements.txt'])
    print("✅ ComfyUI installed!")
else:
    print("✅ ComfyUI already installed!")

# ============================================================
# CELL 3 - Install Custom Nodes (every session)
# ============================================================
import subprocess, os

NODES_DIR = '/content/ComfyUI/custom_nodes'

nodes = [
    ('ComfyUI-WanVideoWrapper', 'https://github.com/kijai/ComfyUI-WanVideoWrapper'),
    ('ComfyUI-VideoHelperSuite', 'https://github.com/Kosinkadink/ComfyUI-VideoHelperSuite'),
    ('ComfyUI-Geeky-Kokoro-TTS', 'https://github.com/GeekyGhost/ComfyUI-Geeky-Kokoro-TTS'),
    ('x-flux-comfyui', 'https://github.com/XLabs-AI/x-flux-comfyui'),
]

for name, url in nodes:
    path = f'{NODES_DIR}/{name}'
    if not os.path.exists(path):
        print(f"Installing {name}...")
        subprocess.run(['git', 'clone', url, path])
        req = f'{path}/requirements.txt'
        if os.path.exists(req):
            subprocess.run(['pip', 'install', '-q', '-r', req])
        print(f"✅ {name} installed!")
    else:
        print(f"✅ {name} already installed!")

print("\n✅ All nodes installed!")

# ============================================================
# CELL 4 - Link Drive Models to ComfyUI (every session)
# ============================================================
import os

COMFY_DIR = '/content/ComfyUI'
DRIVE_MODELS = '/content/drive/MyDrive/ComfyUI_Models'

# Remove default models folder and link to Drive
comfy_models = f'{COMFY_DIR}/models'
if os.path.exists(comfy_models) and not os.path.islink(comfy_models):
    import shutil
    shutil.rmtree(comfy_models)

if not os.path.islink(comfy_models):
    os.symlink(DRIVE_MODELS, comfy_models)
    print("✅ Models folder linked to Google Drive!")
else:
    print("✅ Models already linked to Google Drive!")

# ============================================================
# CELL 5 - Download Models (ONLY NEEDED ONCE!)
# ============================================================
import os, subprocess

DRIVE_MODELS = '/content/drive/MyDrive/ComfyUI_Models'

def download_model(name, url, path, min_size_gb=0.1):
    if os.path.exists(path):
        size = os.path.getsize(path) / (1024**3)
        if size > min_size_gb:
            print(f"✅ {name} already on Drive ({size:.1f}GB) - skipping!")
            return
    print(f"Downloading {name}...")
    subprocess.run(['wget', '-q', '--show-progress', '-O', path, url])
    print(f"✅ {name} downloaded!")

download_model(
    "WanVideo 14B fp8",
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors",
    f"{DRIVE_MODELS}/diffusion_models/Wan2_1-T2V-14B_fp8.safetensors",
    min_size_gb=10
)

download_model(
    "T5 Text Encoder fp8",
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors",
    f"{DRIVE_MODELS}/text_encoders/umt5-xxl-enc-fp8.safetensors",
    min_size_gb=5
)

download_model(
    "WanVideo VAE",
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors",
    f"{DRIVE_MODELS}/vae/Wan2_1_VAE_bf16.safetensors",
    min_size_gb=0.2
)

download_model(
    "FLUX Dev fp8",
    "https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors",
    f"{DRIVE_MODELS}/checkpoints/flux1-dev-fp8.safetensors",
    min_size_gb=10
)

download_model(
    "FLUX CLIP L",
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/clip_l.safetensors",
    f"{DRIVE_MODELS}/clip/clip_l.safetensors",
    min_size_gb=0.2
)

download_model(
    "FLUX T5XXL fp8",
    "https://huggingface.co/comfyanonymous/flux_text_encoders/resolve/main/t5xxl_fp8_e4m3fn.safetensors",
    f"{DRIVE_MODELS}/clip/t5xxl_fp8_e4m3fn.safetensors",
    min_size_gb=4
)

download_model(
    "FLUX VAE",
    "https://huggingface.co/Kijai/flux-fp8/resolve/main/flux-vae-bf16.safetensors",
    f"{DRIVE_MODELS}/vae/flux-vae-bf16.safetensors",
    min_size_gb=0.1
)

print("\n✅ All models ready on Google Drive!")

# ============================================================
# CELL 6 - Download Workflow
# ============================================================
import subprocess, os

COMFY_DIR = '/content/ComfyUI'
os.makedirs(f'{COMFY_DIR}/user/default/workflows', exist_ok=True)

subprocess.run(['wget', '-O', 
    f'{COMFY_DIR}/user/default/workflows/ANIME_DRAMA_WORKFLOW.json',
    'https://raw.githubusercontent.com/TheTechnook/drama-ai-workflow/main/ANIME_DRAMA_WORKFLOW%20(1).json'
])

# Fix workflow paths
import json
path = f'{COMFY_DIR}/user/default/workflows/ANIME_DRAMA_WORKFLOW.json'
with open(path) as f:
    w = json.load(f)
with open(path, 'w') as f:
    json.dump(w, f, indent=2)

print("✅ Workflow downloaded!")

# ============================================================
# CELL 7 - Start ComfyUI + Cloudflare Tunnel
# ============================================================
import subprocess, threading, time, re

# Install cloudflared
subprocess.run(['wget', '-q', '-O', '/tmp/cloudflared.deb',
    'https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb'])
subprocess.run(['dpkg', '-i', '/tmp/cloudflared.deb'])

# Start ComfyUI
print("Starting ComfyUI...")
comfy_process = subprocess.Popen(
    ['python3', 'main.py', '--listen', '0.0.0.0', '--port', '8188'],
    cwd='/content/ComfyUI',
    stdout=open('/tmp/comfy.log', 'w'),
    stderr=subprocess.STDOUT
)

time.sleep(15)

# Start cloudflare tunnel
tunnel_process = subprocess.Popen(
    ['cloudflared', 'tunnel', '--url', 'http://localhost:8188'],
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT
)

print("Getting public URL...")
for line in tunnel_process.stdout:
    line = line.decode()
    if 'trycloudflare.com' in line:
        url = re.search(r'https://[^\s]+trycloudflare\.com', line)
        if url:
            print(f"\n🔥 ComfyUI URL: {url.group()}")
            print("Open this URL in your browser!")
            break
