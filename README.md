# Get a text prompt describing a 3D-model with help of Python, Blender Python API and CLIP.

Simple Python script to get a text prompt of a 3D-model. 

## Prerequisites: 
- Python 3.10


## Setting up:

```
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install numpy==1.26.4
pip install clip-interrogator==0.5.4
pip install transformers==4.26.1
pip install -r requirements.txt
```

## Usage
```
python 3D-to-prompt.py --model_path="YOUR_MODEL_PATH" --clip_model_name="CLIP_MODEL_NAME" --lowvram
```

For the best prompts for Stable Diffusion 1.X use `ViT-L-14/openai` for clip_model_name. For Stable Diffusion 2.0 use `ViT-H-14/laion2b_s32b_b79k`.
On systems with low VRAM you can use `--lowvram` flag to reduce the amount of VRAM needed (at the cost of some speed and quality). The default settings use about 6.3GB of VRAM and the low VRAM settings use about 2.7GB.


## Supported models
- .obj (must come with image textures, not .mtl)
- .fbx (must come with image textures, not .mtl)
- .usd/.usdz
- .x3d
- .gltf/.glb
- .blend

