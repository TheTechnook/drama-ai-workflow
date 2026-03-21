import json, os

workflow = {
    "last_node_id": 19,
    "last_link_id": 20,
    "nodes": [
        {
            "id": 1, "type": "DualCLIPLoader",
            "pos": [0, 0], "size": [320, 100],
            "flags": {}, "order": 0, "mode": 0, "inputs": [],
            "outputs": [{"name": "CLIP", "type": "CLIP", "links": [1, 2], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["clip_l.safetensors", "t5xxl_fp8_e4m3fn.safetensors", "flux"]
        },
        {
            "id": 2, "type": "CLIPTextEncodeFlux",
            "pos": [370, 0], "size": [500, 150],
            "flags": {}, "order": 1, "mode": 0,
            "inputs": [{"name": "clip", "type": "CLIP", "link": 1}],
            "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [3], "slot_index": 0}],
            "properties": {},
            "widgets_values": [
                "anime style, jujutsu kaisen art, teenage boy, 17 years old, dark skin, short spiky black hair, school uniform, sharp clean lines, expressive eyes, cinematic lighting, masterpiece",
                "anime style, jujutsu kaisen art, teenage boy, 17 years old, dark skin, short spiky black hair, school uniform, sharp clean lines, expressive eyes, cinematic lighting, masterpiece",
                3.5
            ]
        },
        {
            "id": 3, "type": "CLIPTextEncodeFlux",
            "pos": [370, 200], "size": [500, 150],
            "flags": {}, "order": 2, "mode": 0,
            "inputs": [{"name": "clip", "type": "CLIP", "link": 2}],
            "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [4], "slot_index": 0}],
            "properties": {},
            "widgets_values": [
                "blurry, ugly, deformed, watermark, text, bad anatomy, low quality, realistic, 3d, photograph",
                "blurry, ugly, deformed, watermark, text, bad anatomy, low quality, realistic, 3d, photograph",
                3.5
            ]
        },
        {
            "id": 4, "type": "EmptyLatentImage",
            "pos": [370, 380], "size": [300, 100],
            "flags": {}, "order": 3, "mode": 0, "inputs": [],
            "outputs": [{"name": "LATENT", "type": "LATENT", "links": [5], "slot_index": 0}],
            "properties": {},
            "widgets_values": [768, 1024, 1]
        },
        {
            "id": 5, "type": "KSampler",
            "pos": [920, 0], "size": [350, 280],
            "flags": {}, "order": 4, "mode": 0,
            "inputs": [
                {"name": "model", "type": "MODEL", "link": 20},
                {"name": "positive", "type": "CONDITIONING", "link": 3},
                {"name": "negative", "type": "CONDITIONING", "link": 4},
                {"name": "latent_image", "type": "LATENT", "link": 5}
            ],
            "outputs": [{"name": "LATENT", "type": "LATENT", "links": [6], "slot_index": 0}],
            "properties": {},
            "widgets_values": [42, "fixed", "euler", "simple", 20, 3.5, 1]
        },
        {
            "id": 6, "type": "UNETLoader",
            "pos": [0, 180], "size": [320, 100],
            "flags": {}, "order": 5, "mode": 0, "inputs": [],
            "outputs": [{"name": "MODEL", "type": "MODEL", "links": [20], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["flux1-dev-fp8.safetensors", "fp8_e4m3fn"]
        },
        {
            "id": 7, "type": "VAELoader",
            "pos": [0, 320], "size": [320, 100],
            "flags": {}, "order": 6, "mode": 0, "inputs": [],
            "outputs": [{"name": "VAE", "type": "VAE", "links": [7], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["flux-vae-bf16.safetensors"]
        },
        {
            "id": 8, "type": "VAEDecode",
            "pos": [1320, 0], "size": [200, 100],
            "flags": {}, "order": 7, "mode": 0,
            "inputs": [
                {"name": "samples", "type": "LATENT", "link": 6},
                {"name": "vae", "type": "VAE", "link": 7}
            ],
            "outputs": [{"name": "IMAGE", "type": "IMAGE", "links": [8, 9], "slot_index": 0}],
            "properties": {}
        },
        {
            "id": 9, "type": "SaveImage",
            "pos": [1570, 0], "size": [300, 100],
            "flags": {}, "order": 8, "mode": 0,
            "inputs": [{"name": "images", "type": "IMAGE", "link": 8}],
            "outputs": [], "properties": {},
            "widgets_values": ["anime_character"]
        },
        {
            "id": 10, "type": "CLIPVisionLoader",
            "pos": [0, 500], "size": [320, 100],
            "flags": {}, "order": 9, "mode": 0, "inputs": [],
            "outputs": [{"name": "CLIP_VISION", "type": "CLIP_VISION", "links": [10], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["clip_vision_h.safetensors"]
        },
        {
            "id": 11, "type": "WanVideoClipVisionEncode",
            "pos": [370, 500], "size": [400, 200],
            "flags": {}, "order": 10, "mode": 0,
            "inputs": [
                {"name": "clip_vision", "type": "CLIP_VISION", "link": 10},
                {"name": "image_1", "type": "IMAGE", "link": 9}
            ],
            "outputs": [{"name": "image_embeds", "type": "WANVIDIMAGE_EMBEDS", "links": [11], "slot_index": 0}],
            "properties": {},
            "widgets_values": [1.0, 1.0, "center", "average", True]
        },
        {
            "id": 12, "type": "WanVideoModelLoader",
            "pos": [0, 700], "size": [350, 180],
            "flags": {}, "order": 11, "mode": 0, "inputs": [],
            "outputs": [{"name": "model", "type": "WANVIDEOMODEL", "links": [12], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["Wan2_1-T2V-14B_fp8.safetensors", "bf16", "fp8_e4m3fn", "offload_device", "sdpa"]
        },
        {
            "id": 13, "type": "LoadWanVideoT5TextEncoder",
            "pos": [0, 920], "size": [350, 100],
            "flags": {}, "order": 12, "mode": 0, "inputs": [],
            "outputs": [{"name": "t5", "type": "WANVIDEOT5", "links": [13], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["umt5-xxl-enc-fp8.safetensors", "fp8_e4m3fn", True]
        },
        {
            "id": 14, "type": "WanVideoTextEncode",
            "pos": [400, 700], "size": [500, 200],
            "flags": {}, "order": 13, "mode": 0,
            "inputs": [{"name": "t5", "type": "WANVIDEOT5", "link": 13}],
            "outputs": [{"name": "text_embeds", "type": "WANVIDEOTEXTEMBEDS", "links": [14], "slot_index": 0}],
            "properties": {},
            "widgets_values": [
                "anime style jujutsu kaisen, teenage boy talking, emotional school drama, mouth moving, expressive eyes, school hallway, dramatic lighting, cinematic",
                "blurry, ugly, watermark, text, deformed, realistic",
                True
            ]
        },
        {
            "id": 15, "type": "WanVideoSampler",
            "pos": [950, 600], "size": [400, 320],
            "flags": {}, "order": 14, "mode": 0,
            "inputs": [
                {"name": "model", "type": "WANVIDEOMODEL", "link": 12},
                {"name": "image_embeds", "type": "WANVIDIMAGE_EMBEDS", "link": 11},
                {"name": "text_embeds", "type": "WANVIDEOTEXTEMBEDS", "link": 14}
            ],
            "outputs": [{"name": "samples", "type": "LATENT", "links": [15], "slot_index": 0}],
            "properties": {},
            "widgets_values": [42, 20, 6.0, 5.0, 0, True, "unipc", 0]
        },
        {
            "id": 16, "type": "WanVideoVAELoader",
            "pos": [0, 1050], "size": [320, 100],
            "flags": {}, "order": 15, "mode": 0, "inputs": [],
            "outputs": [{"name": "vae", "type": "WANVAE", "links": [16], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["Wan2_1_VAE_bf16.safetensors", "bf16"]
        },
        {
            "id": 17, "type": "WanVideoDecode",
            "pos": [1400, 600], "size": [300, 200],
            "flags": {}, "order": 16, "mode": 0,
            "inputs": [
                {"name": "vae", "type": "WANVAE", "link": 16},
                {"name": "samples", "type": "LATENT", "link": 15}
            ],
            "outputs": [{"name": "images", "type": "IMAGE", "links": [17], "slot_index": 0}],
            "properties": {},
            "widgets_values": [True, 272, 272, 144, 144]
        },
        {
            "id": 18, "type": "GeekyKokoroTTS",
            "pos": [0, 1200], "size": [500, 250],
            "flags": {}, "order": 17, "mode": 0, "inputs": [],
            "outputs": [{"name": "audio", "type": "AUDIO", "links": [18], "slot_index": 0}],
            "properties": {},
            "widgets_values": ["Yo, did you hear what Marcus did? He snitched on everyone!", "am_fenrir", 1.0, 1.0, 24000]
        },
        {
            "id": 19, "type": "VHS_VideoCombine",
            "pos": [1750, 600], "size": [350, 250],
            "flags": {}, "order": 18, "mode": 0,
            "inputs": [
                {"name": "images", "type": "IMAGE", "link": 17},
                {"name": "audio", "type": "AUDIO", "link": 18}
            ],
            "outputs": [], "properties": {},
            "widgets_values": [24, "video/h264-mp4", "anime_drama", 0, True, "default"]
        }
    ],
    "links": [
        [1, 1, 0, 2, 0, "CLIP"],
        [2, 1, 0, 3, 0, "CLIP"],
        [3, 2, 0, 5, 1, "CONDITIONING"],
        [4, 3, 0, 5, 2, "CONDITIONING"],
        [5, 4, 0, 5, 3, "LATENT"],
        [6, 5, 0, 8, 0, "LATENT"],
        [7, 7, 0, 8, 1, "VAE"],
        [8, 8, 0, 9, 0, "IMAGE"],
        [9, 8, 0, 11, 1, "IMAGE"],
        [10, 10, 0, 11, 0, "CLIP_VISION"],
        [11, 11, 0, 15, 1, "WANVIDIMAGE_EMBEDS"],
        [12, 12, 0, 15, 0, "WANVIDEOMODEL"],
        [13, 13, 0, 14, 0, "WANVIDEOT5"],
        [14, 14, 0, 15, 2, "WANVIDEOTEXTEMBEDS"],
        [15, 15, 0, 17, 1, "LATENT"],
        [16, 16, 0, 17, 0, "WANVAE"],
        [17, 17, 0, 19, 0, "IMAGE"],
        [18, 18, 0, 19, 1, "AUDIO"],
        [20, 6, 0, 5, 0, "MODEL"]
    ],
    "groups": [
        {"title": "FLUX Anime Character Generator", "bounding": [-20, -20, 1900, 470], "color": "#3d5a7a"},
        {"title": "WanVideo Animate Character", "bounding": [-20, 470, 2200, 620], "color": "#5a3d7a"},
        {"title": "Voice + Export", "bounding": [-20, 1150, 900, 320], "color": "#3d7a5a"}
    ],
    "config": {},
    "extra": {"ds": {"scale": 0.4, "offset": [0, 0]}},
    "version": 0.4
}

os.makedirs("/workspace/ComfyUI/user/default/workflows", exist_ok=True)
path = "/workspace/ComfyUI/user/default/workflows/ANIME_DRAMA_WORKFLOW.json"
with open(path, "w") as f:
    json.dump(workflow, f, indent=2)
print("✅ CLEAN ANIME DRAMA WORKFLOW created!")
print("📂 Load in ComfyUI: folder icon → ANIME_DRAMA_WORKFLOW")
