#!/bin/bash

# ============================================================
#   DRAMA AI STUDIO - COMPLETE SETUP SCRIPT
#   GitHub: TheTechnook/drama-ai-workflow
#   Run this on any fresh GPU to get fully set up!
# ============================================================

GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}"
echo "  ██████╗ ██████╗  █████╗ ███╗   ███╗ █████╗      █████╗ ██╗"
echo "  ██╔══██╗██╔══██╗██╔══██╗████╗ ████║██╔══██╗    ██╔══██╗██║"
echo "  ██║  ██║██████╔╝███████║██╔████╔██║███████║    ███████║██║"
echo "  ██║  ██║██╔══██╗██╔══██║██║╚██╔╝██║██╔══██║    ██╔══██║██║"
echo "  ██████╔╝██║  ██║██║  ██║██║ ╚═╝ ██║██║  ██║    ██║  ██║██║"
echo "  ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝    ╚═╝  ╚═╝╚═╝"
echo -e "${NC}"
echo -e "${GREEN}  DRAMA AI STUDIO - Full Production Pipeline Setup${NC}"
echo "  ============================================================"
echo ""

WORKSPACE="/workspace"
COMFY_DIR="$WORKSPACE/ComfyUI"
MODELS_DIR="$COMFY_DIR/models"
NODES_DIR="$COMFY_DIR/custom_nodes"

# ─── STEP 1: INSTALL COMFYUI ───
echo -e "${YELLOW}[1/7] Installing ComfyUI...${NC}"
if [ ! -d "$COMFY_DIR" ]; then
    apt-get install -y git wget unzip > /dev/null 2>&1
    git clone https://github.com/comfyanonymous/ComfyUI.git $COMFY_DIR
    pip install -q -r $COMFY_DIR/requirements.txt
    echo -e "${GREEN}✅ ComfyUI installed!${NC}"
else
    echo -e "${GREEN}✅ ComfyUI already exists, skipping...${NC}"
fi

# ─── STEP 2: INSTALL CUSTOM NODES ───
echo -e "${YELLOW}[2/7] Installing custom nodes...${NC}"

install_node() {
    NAME=$1
    URL=$2
    DIR="$NODES_DIR/$NAME"
    if [ ! -d "$DIR" ]; then
        echo "  Installing $NAME..."
        wget -q -O /tmp/node.zip "$URL" && unzip -q /tmp/node.zip -d /tmp/node_extract
        EXTRACTED=$(ls /tmp/node_extract)
        mv /tmp/node_extract/$EXTRACTED $DIR
        rm -rf /tmp/node.zip /tmp/node_extract
        if [ -f "$DIR/requirements.txt" ]; then
            pip install -q -r $DIR/requirements.txt --break-system-packages 2>/dev/null
        fi
        echo -e "  ${GREEN}✅ $NAME installed!${NC}"
    else
        echo -e "  ${GREEN}✅ $NAME already installed, skipping...${NC}"
    fi
}

install_node "ComfyUI-WanVideoWrapper" "https://codeload.github.com/kijai/ComfyUI-WanVideoWrapper/zip/refs/heads/main"
install_node "ComfyUI-VideoHelperSuite" "https://codeload.github.com/Kosinkadink/ComfyUI-VideoHelperSuite/zip/refs/heads/main"
install_node "comfyui-reactor-node" "https://codeload.github.com/Gourieff/ComfyUI-ReActor/zip/refs/heads/main"
install_node "ComfyUI-LatentSyncWrapper" "https://codeload.github.com/ShmuelRonen/ComfyUI-LatentSyncWrapper/zip/refs/heads/main"
install_node "x-flux-comfyui" "https://codeload.github.com/XLabs-AI/x-flux-comfyui/zip/refs/heads/main"
install_node "ComfyUI-Geeky-Kokoro-TTS" "https://codeload.github.com/GeekyGhost/ComfyUI-Geeky-Kokoro-TTS/zip/refs/heads/main"
install_node "ACE-Step-ComfyUI" "https://codeload.github.com/ace-step/ACE-Step-ComfyUI/zip/refs/heads/main"

# ─── STEP 3: FIX PROTOBUF FOR REACTOR ───
echo -e "${YELLOW}[3/7] Fixing dependencies...${NC}"
pip install -q protobuf==3.20.3 --break-system-packages 2>/dev/null
pip install -q onnxruntime-gpu --break-system-packages 2>/dev/null
echo -e "${GREEN}✅ Dependencies fixed!${NC}"

# ─── STEP 4: DOWNLOAD MODELS ───
echo -e "${YELLOW}[4/7] Checking and downloading models...${NC}"

mkdir -p $MODELS_DIR/diffusion_models
mkdir -p $MODELS_DIR/text_encoders
mkdir -p $MODELS_DIR/vae
mkdir -p $MODELS_DIR/checkpoints
mkdir -p $MODELS_DIR/insightface
mkdir -p $MODELS_DIR/facerestore_models

download_model() {
    NAME=$1
    URL=$2
    PATH_=$3
    SIZE_EXPECTED=$4
    if [ -f "$PATH_" ]; then
        SIZE=$(du -m "$PATH_" | cut -f1)
        if [ "$SIZE" -gt "$SIZE_EXPECTED" ]; then
            echo -e "  ${GREEN}✅ $NAME already downloaded ($SIZE MB)${NC}"
            return
        fi
    fi
    echo "  Downloading $NAME..."
    wget -q --show-progress -O "$PATH_" "$URL"
    echo -e "  ${GREEN}✅ $NAME downloaded!${NC}"
}

download_model \
    "WanVideo 14B fp8" \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1-T2V-14B_fp8_e4m3fn.safetensors" \
    "$MODELS_DIR/diffusion_models/Wan2_1-T2V-14B_fp8.safetensors" \
    5000

download_model \
    "T5 Text Encoder fp8" \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/umt5-xxl-enc-fp8_e4m3fn.safetensors" \
    "$MODELS_DIR/text_encoders/umt5-xxl-enc-fp8.safetensors" \
    5000

download_model \
    "WanVideo VAE bf16" \
    "https://huggingface.co/Kijai/WanVideo_comfy/resolve/main/Wan2_1_VAE_bf16.safetensors" \
    "$MODELS_DIR/vae/Wan2_1_VAE_bf16.safetensors" \
    200

download_model \
    "FLUX Dev fp8" \
    "https://huggingface.co/Kijai/flux-fp8/resolve/main/flux1-dev-fp8.safetensors" \
    "$MODELS_DIR/checkpoints/flux1-dev-fp8.safetensors" \
    10000

download_model \
    "ReActor Face Swap Model" \
    "https://huggingface.co/ezioruan/inswapper_128.onnx/resolve/main/inswapper_128.onnx" \
    "$MODELS_DIR/insightface/inswapper_128.onnx" \
    400

download_model \
    "GFPGAN Face Restore" \
    "https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/GFPGANv1.4.pth" \
    "$MODELS_DIR/facerestore_models/GFPGANv1.4.pth" \
    200

# ─── STEP 5: SECURITY FIX ───
echo -e "${YELLOW}[5/7] Applying security fix...${NC}"
mkdir -p $COMFY_DIR/user/default
cat > $COMFY_DIR/user/default/manager_config.yaml << 'EOF'
security_level: normal
network_mode: personal_cloud
EOF
echo -e "${GREEN}✅ Security fixed!${NC}"

# ─── STEP 6: GENERATE WORKFLOW ───
echo -e "${YELLOW}[6/7] Downloading and generating master workflow...${NC}"
wget -q -O /tmp/drama_workflow.py "https://raw.githubusercontent.com/TheTechnook/drama-ai-workflow/main/create_drama_workflow.py"
python /tmp/drama_workflow.py
echo -e "${GREEN}✅ Master workflow ready!${NC}"

# ─── STEP 7: INSTALL NGROK + START ───
echo -e "${YELLOW}[7/7] Installing ngrok...${NC}"
if [ ! -f "$WORKSPACE/ngrok" ]; then
    wget -q https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-amd64.tgz -O /tmp/ngrok.tgz
    tar -xzf /tmp/ngrok.tgz -C $WORKSPACE
    echo -e "${GREEN}✅ ngrok installed!${NC}"
else
    echo -e "${GREEN}✅ ngrok already installed!${NC}"
fi

# ─── VERIFY EVERYTHING ───
echo ""
echo -e "${BLUE}============================================================${NC}"
echo -e "${GREEN}  ✅ DRAMA AI STUDIO SETUP COMPLETE!${NC}"
echo -e "${BLUE}============================================================${NC}"
echo ""
echo -e "${YELLOW}📋 MODEL CHECK:${NC}"
for f in \
    "$MODELS_DIR/diffusion_models/Wan2_1-T2V-14B_fp8.safetensors" \
    "$MODELS_DIR/text_encoders/umt5-xxl-enc-fp8.safetensors" \
    "$MODELS_DIR/vae/Wan2_1_VAE_bf16.safetensors" \
    "$MODELS_DIR/checkpoints/flux1-dev-fp8.safetensors" \
    "$MODELS_DIR/insightface/inswapper_128.onnx" \
    "$MODELS_DIR/facerestore_models/GFPGANv1.4.pth"
do
    if [ -f "$f" ]; then
        SIZE=$(du -h "$f" | cut -f1)
        echo -e "  ${GREEN}✅ $(basename $f) ($SIZE)${NC}"
    else
        echo -e "  ${RED}❌ MISSING: $(basename $f)${NC}"
    fi
done

echo ""
echo -e "${YELLOW}🚀 NEXT STEPS:${NC}"
echo "  1. Add ngrok token:  $WORKSPACE/ngrok config add-authtoken YOUR_TOKEN"
echo "  2. Start ComfyUI:    cd $COMFY_DIR && python main.py --listen 0.0.0.0 --port 8188 --lowvram &"
echo "  3. Start tunnel:     sleep 15 && $WORKSPACE/ngrok http 8188"
echo "  4. Open URL in browser"
echo "  5. Load DRAMA_MASTER_WORKFLOW and generate! 🎬"
echo ""
