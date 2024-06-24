import bpy
from bpy import context
import os
from PIL import Image
from clip_interrogator import Config, Interrogator
import argparse


def model_to_prompt(model_path, clip_model_name, lowvram: bool):
    output_image_path = os.getcwd() + '\\screenshot.png'

    # CLEANING THE SCENE
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

    # IMPORTING MODEL
    if model_path[-3:] == 'obj':
        bpy.ops.wm.obj_import(filepath=model_path, filter_glob='*.obj;*.mtl')  # MUST HAVE TEXTURES
    #elif model_path[-3:] == 'dae':
    #    bpy.ops.wm.collada_import(filepath=model_path, auto_connect = True,
    #                      find_chains = True,
    #                      fix_orientation = True)
    #elif model_path[-3:] in ['STL', 'stl']:
    #    bpy.ops.wm.stl_import(filepath=model_path) #NO TEXTURES
    #elif model_path[-3:] == 'ply':
    #    bpy.ops.wm.ply_import(filepath=model_path)
    elif model_path[-4:] in ['usdz', '.usd']:
        bpy.ops.wm.usd_import(filepath=model_path)  # ALREADY HAS TEXTURES
    elif model_path[-3:] == 'x3d':
        bpy.ops.import_scene.x3d(filepath=model_path)  # MUST HAVE TEXTURES
    elif model_path[-4:] in ['gltf', '.glb']:
        bpy.ops.import_scene.gltf(filepath=model_path)  # ALREADY HAS TEXTURES
    elif model_path[-3:] in ['FBX', 'fbx']:
        bpy.ops.import_scene.fbx(filepath=model_path)  # MUST HAVE TEXTURES
    elif model_path[-5:] == 'blend':
        bpy.ops.wm.open_mainfile(filepath=model_path)  # ALREADY HAS TEXTURES

    # SETTING UP THE CAMERA
    bpy.ops.object.camera_add(location=(0, -10, 10))
    camera = bpy.context.object
    camera.rotation_euler = (1.1, 0, 0.8)
    bpy.context.scene.camera = camera

    # FOCUSING THE CAMERA ON OUR MODEL
    for obj in context.scene.objects:
        obj.select_set(False)
    for obj in context.visible_objects:
        if not (obj.hide_get() or obj.hide_render):
            obj.select_set(True)
    bpy.ops.view3d.camera_to_view_selected()

    # SETTING UP THE LIGHTS
    bpy.ops.object.light_add(type='SUN', location=(camera.location[0], camera.location[1], camera.location[2] + 5), rotation=camera.rotation_euler)
    light = bpy.context.object
    light.data.energy = 3

    # RENDER SETTINGS
    bpy.context.scene.render.engine = 'CYCLES'
    bpy.context.scene.cycles.samples = 100
    bpy.context.scene.render.resolution_x = 1920
    bpy.context.scene.render.resolution_y = 1080
    bpy.context.scene.render.resolution_percentage = 100

    # SETTING OUTPUT IMAGE PATH AND FORMAT
    bpy.context.scene.render.filepath = output_image_path
    bpy.context.scene.render.image_settings.file_format = 'PNG'  # Используйте 'JPEG' для JPG

    # RENDERING
    bpy.ops.render.render(write_still=True)



    ## RUNNING CLIP ##

    image = Image.open(output_image_path).convert('RGB')
    config = Config(clip_model_name=clip_model_name)
    if lowvram:
        config.apply_low_vram_defaults()
    ci = Interrogator(config)
    prompt = ci.interrogate(image)

    return prompt


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model_path", type=str, help="Path to a model"
    )
    parser.add_argument(
        "--clip_model_name", default="ViT-L-14/openai", type=str, help="Name of a CLIP model to use"
    )
    parser.add_argument(
        "--lowvram", action="store_true", help="Flag for low VRAM settings"
    )
    args = parser.parse_args()

    model_path = os.path.abspath(args.model_path)

    prompt = model_to_prompt(model_path=model_path,
                             clip_model_name=args.clip_model_name,
                             lowvram=args.lowvram)
    print(prompt)


if __name__ == "__main__":
    main()
