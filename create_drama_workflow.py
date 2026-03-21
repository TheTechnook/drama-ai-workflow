import json

workflow = {
    "last_node_id": 40,
    "last_link_id": 50,
    "nodes": [
        # ─── FLUX IMAGE GENERATION ───
        {
            "id": 1,
            "type": "CheckpointLoaderSimple",
            "pos": [0, 0],
            "size": [300, 100],
            "flags": {},
            "order": 0,
            "mode": 0,
            "inputs": [],
            "outputs": [
                {"name": "MODEL", "type": "MODEL", "links": [1]},
                {"name": "CLIP", "type": "CLIP", "links": [2]},
                {"name": "VAE", "type": "VAE", "links": [3]}
            ],
            "properties": {},
            "widgets_values": ["flux1-dev-fp8.safetensors"]
        },
        {
            "id": 2,
            "type": "CLIPTextEncodeFlux",
            "pos": [350, 0],
            "size": [400, 150],
            "flags": {},
            "order": 1,
            "mode": 0,
            "inputs": [{"name": "clip", "type": "CLIP", "link": 2}],
            "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [4]}],
            "properties": {},
            "widgets_values": [
                "A realistic teenage boy, 16 years old, short dark hair, brown skin, wearing school uniform white shirt, school hallway background, cinematic lighting, photorealistic",
                "A realistic teenage boy, 16 years old, short dark hair, brown skin, wearing school uniform white shirt, school hallway background, cinematic lighting, photorealistic",
                3.5
            ]
        },
        {
            "id": 3,
            "type": "CLIPTextEncodeFlux",
            "pos": [350, 200],
            "size": [400, 150],
            "flags": {},
            "order": 2,
            "mode": 0,
            "inputs": [{"name": "clip", "type": "CLIP", "link": 2}],
            "outputs": [{"name": "CONDITIONING", "type": "CONDITIONING", "links": [5]}],
            "properties": {},
            "widgets_values": [
                "blurry, ugly, deformed, watermark, text",
                "blurry, ugly, deformed, watermark, text",
                3.5
            ]
        },
        {
            "id": 4,
            "type": "EmptyLatentImage",
            "pos": [350, 400],
            "size": [300, 100],
            "flags": {},
            "order": 3,
            "mode": 0,
            "inputs": [],
            "outputs": [{"name": "LATENT", "type": "LATENT", "links": [6]}],
            "properties": {},
            "widgets_values": [512, 768, 1]
        },
        {
            "id": 5,
            "type": "KSampler",
            "pos": [800, 100],
            "size": [350, 300],
            "flags": {},
            "order": 4,
            "mode": 0,
            "inputs": [
                {"name": "model", "type": "MODEL", "link": 1},
                {"name": "positive", "type": "CONDITIONING", "link": 4},
                {"name": "negative", "type": "CONDITIONING", "link": 5},
                {"name": "latent_image", "type": "LATENT", "link": 6}
            ],
            "outputs": [{"name": "LATENT", "type": "LATENT", "links": [7]}],
            "properties": {},
            "widgets_values": [42, "euler", "simple", 20, 3.5, "disable", 1]
        },
        {
            "id": 6,
            "type": "VAEDecode",
            "pos": [1200, 100],
            "size": [200, 100],
            "flags": {},
            "order": 5,
            "mode": 0,
            "inputs": [
                {"name": "samples", "type": "LATENT", "link": 7},
                {"name": "vae", "type": "VAE", "link": 3}
            ],
            "outputs": [{"name": "IMAGE", "type": "IMAGE", "links": [8, 9]}],
            "properties": {}
        },
        {
            "id": 7,
            "type": "SaveImage",
            "pos": [1450, 0],
            "size": [300, 100],
            "flags": {},
            "order": 6,
            "mode": 0,
            "inputs": [{"name": "images", "type": "IMAGE", "link": 8}],
            "outputs": [],
            "properties": {},
            "widgets_values": ["actor_reference"]
        },

        # ─── WANVIDEO T2V ───
        {
            "id": 10,
            "type": "WanVideoModelLoader",
            "pos": [0, 600],
            "size": [350, 150],
            "flags": {},
            "order": 7,
            "mode": 0,
            "inputs": [],
            "outputs": [{"name": "model", "type": "WANVIDEOMODEL", "links": [10]}],
            "properties": {},
            "widgets_values": [
                "Wan2_1-T2V-14B_fp8.safetensors",
                "fp8_e4m3fn",
                "offload_full_models",
                True,
                19,
                "fp16",
                "disabled"
            ]
        },
        {
            "id": 11,
            "type": "LoadWanVideoT5TextEncoder",
            "pos": [0, 800],
            "size": [350, 100],
            "flags": {},
            "order": 8,
            "mode": 0,
            "inputs": [],
            "outputs": [{"name": "t5", "type": "WANVIDEOT5", "links": [11]}],
            "properties": {},
            "widgets_values": ["umt5-xxl-enc-fp8.safetensors", "fp8_e4m3fn", True]
        },
        {
            "id": 12,
            "type": "WanVideoTextEncode",
            "pos": [400, 700],
            "size": [500, 200],
            "flags": {},
            "order": 9,
            "mode": 0,
            "inputs": [{"name": "t5", "type": "WANVIDEOT5", "link": 11}],
            "outputs": [{"name": "conditioning", "type": "WANVIDEOCONDITIONING", "links": [12]}],
            "properties": {},
            "widgets_values": [
                "Two teenage students arguing in a school hallway, one pointing finger accusingly, other looking defensive, other students watching, dramatic lighting, cinematic, realistic",
                "blurry, ugly, watermark, text, deformed",
                True
            ]
        },
        {
            "id": 13,
            "type": "WanVideoEmptyEmbeds",
            "pos": [400, 950],
            "size": [300, 150],
            "flags": {},
            "order": 10,
            "mode": 0,
            "inputs": [],
            "outputs": [{"name": "embeds", "type": "WANVIDEOEMBED", "links": [13]}],
            "properties": {},
            "widgets_values": [480, 288, 17, 16]
        },
        {
            "id": 14,
            "type": "WanVideoSampler",
            "pos": [750, 800],
            "size": [400, 300],
            "flags": {},
            "order": 11,
            "mode": 0,
            "inputs": [
                {"name": "model", "type": "WANVIDEOMODEL", "link": 10},
                {"name": "conditioning", "type": "WANVIDEOCONDITIONING", "link": 12},
                {"name": "embeds", "type": "WANVIDEOEMBED", "link": 13}
            ],
            "outputs": [{"name": "samples", "type": "LATENT", "links": [14]}],
            "properties": {},
            "widgets_values": [42, 6, 5.0, "unipc", "fp8_e4m3fn", True]
        },
        {
            "id": 15,
            "type": "WanVideoVAELoader",
            "pos": [0, 1000],
            "size": [300, 100],
            "flags": {},
            "order": 12,
            "mode": 0,
            "inputs": [],
            "outputs": [{"name": "vae", "type": "VAE", "links": [15]}],
            "properties": {},
            "widgets_values": ["Wan2_1_VAE_bf16.safetensors", "bf16"]
        },
        {
            "id": 16,
            "type": "WanVideoDecode",
            "pos": [1200, 800],
            "size": [300, 150],
            "flags": {},
            "order": 13,
            "mode": 0,
            "inputs": [
                {"name": "vae", "type": "VAE", "link": 15},
                {"name": "samples", "type": "LATENT", "link": 14}
            ],
            "outputs": [{"name": "images", "type": "IMAGE", "links": [16]}],
            "properties": {},
            "widgets_values": [True, 64, 4]
        },

        # ─── REACTOR FACE SWAP ───
        {
            "id": 20,
            "type": "ReActorFaceSwap",
            "pos": [1600, 700],
            "size": [400, 300],
            "flags": {},
            "order": 14,
            "mode": 0,
            "inputs": [
                {"name": "input_image", "type": "IMAGE", "link": 16},
                {"name": "source_image", "type": "IMAGE", "link": 9}
            ],
            "outputs": [{"name": "image", "type": "IMAGE", "links": [17]}],
            "properties": {},
            "widgets_values": [
                True,
                "inswapper_128.onnx",
                "CodeFormer",
                0.8,
                "FULL_PP",
                "FULL_PP",
                True,
                True,
                "GFPGANv1.4",
                0,
                0
            ]
        },

        # ─── KOKORO TTS ───
        {
            "id": 25,
            "type": "GeekyKokoroTTS",
            "pos": [0, 1200],
            "size": [500, 250],
            "flags": {},
            "order": 15,
            "mode": 0,
            "inputs": [],
            "outputs": [{"name": "audio", "type": "AUDIO", "links": [20]}],
            "properties": {},
            "widgets_values": [
                "Yo man, did you hear what happened? Marcus snitched on the whole crew.",
                "am_michael",
                1.0,
                1.0,
                24000
            ]
        },

        # ─── LATSYNC LIP SYNC ───
        {
            "id": 30,
            "type": "LatentSyncNode",
            "pos": [1600, 1100],
            "size": [400, 200],
            "flags": {},
            "order": 16,
            "mode": 0,
            "inputs": [
                {"name": "video", "type": "IMAGE", "link": 17},
                {"name": "audio", "type": "AUDIO", "link": 20}
            ],
            "outputs": [{"name": "video", "type": "IMAGE", "links": [30]}],
            "properties": {},
            "widgets_values": [25, 42]
        },

        # ─── VIDEO SAVE ───
        {
            "id": 35,
            "type": "VHS_VideoCombine",
            "pos": [2050, 900],
            "size": [350, 200],
            "flags": {},
            "order": 17,
            "mode": 0,
            "inputs": [
                {"name": "images", "type": "IMAGE", "link": 30},
                {"name": "audio", "type": "AUDIO", "link": 20}
            ],
            "outputs": [],
            "properties": {},
            "widgets_values": [
                24,
                "mp4",
                "drama_scene",
                True,
                False,
                "default"
            ]
        }
    ],
    "links": [
        [1, 1, 0, 5, 0, "MODEL"],
        [2, 1, 1, 2, 0, "CLIP"],
        [2, 1, 1, 3, 0, "CLIP"],
        [3, 3, 0, 5, 2, "CONDITIONING"],
        [4, 2, 0, 5, 1, "CONDITIONING"],
        [5, 3, 0, 5, 2, "CONDITIONING"],
        [6, 4, 0, 5, 3, "LATENT"],
        [7, 5, 0, 6, 0, "LATENT"],
        [8, 6, 0, 7, 0, "IMAGE"],
        [9, 6, 0, 20, 1, "IMAGE"],
        [10, 10, 0, 14, 0, "WANVIDEOMODEL"],
        [11, 11, 0, 12, 0, "WANVIDEOT5"],
        [12, 12, 0, 14, 1, "WANVIDEOCONDITIONING"],
        [13, 13, 0, 14, 2, "WANVIDEOEMBED"],
        [14, 14, 0, 16, 1, "LATENT"],
        [15, 15, 0, 16, 0, "VAE"],
        [16, 16, 0, 20, 0, "IMAGE"],
        [17, 20, 0, 30, 0, "IMAGE"],
        [20, 25, 0, 30, 1, "AUDIO"],
        [20, 25, 0, 35, 1, "AUDIO"],
        [30, 30, 0, 35, 0, "IMAGE"]
    ],
    "groups": [
        {"title": "🎨 FLUX Actor Image Generator", "bounding": [-20, -20, 1800, 550], "color": "#3d5a7a"},
        {"title": "🎬 WanVideo Scene Generator", "bounding": [-20, 570, 1800, 650], "color": "#5a3d7a"},
        {"title": "👤 ReActor Face Swap", "bounding": [1550, 650, 500, 400], "color": "#7a3d3d"},
        {"title": "🎤 Kokoro TTS Voice", "bounding": [-20, 1170, 550, 300], "color": "#3d7a5a"},
        {"title": "👄 LatentSync Lip Sync + Export", "bounding": [1550, 1050, 900, 350], "color": "#7a6a3d"}
    ],
    "config": {},
    "extra": {"ds": {"scale": 0.5, "offset": [0, 0]}},
    "version": 0.4
}

output_path = "/workspace/ComfyUI/user/default/workflows/DRAMA_MASTER_WORKFLOW.json"
with open(output_path, "w") as f:
    json.dump(workflow, f, indent=2)

print(f"✅ Master workflow saved to: {output_path}")
print("📋 Load it in ComfyUI: Click folder icon → select DRAMA_MASTER_WORKFLOW.json")
print("\n🎬 Workflow includes:")
print("  🎨 FLUX - Generate actor reference images")
print("  🎬 WanVideo 14B - Generate video scenes")
print("  👤 ReActor - Consistent face swap")
print("  🎤 Kokoro TTS - Teen voices")
print("  👄 LatentSync - Lip sync")
print("  💾 Video export with audio")
