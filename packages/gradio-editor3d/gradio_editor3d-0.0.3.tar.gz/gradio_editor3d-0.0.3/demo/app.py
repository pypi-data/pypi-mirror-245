import gradio as gr
import sys
sys.path.append("../text2world/")
from models.controlnet_inpaint import ControlNetPipeline
from diffusers_helpers import attach_loaders_mixin
from diffusers.models.attention_processor import AttnProcessor
from cross_frame_attention import CrossFrameAttnProcessor
from dataclasses import dataclass
import PIL
import PIL.Image

import torch
import numpy as np
from gradio_editor3d import Editor3D as g3deditor
import copy
cn = ControlNetPipeline()
# lora_dir = "/datawaha/cggroup/bhatsf/checkpoints/layout_controlnet_lora/cnlora-steps200-bs12-gpu4-v1"
# lora_dir = "/datawaha/cggroup/bhatsf/checkpoints/layout_controlnet_lora/CNBoxyLoRA-lr1.00e-04-r8-step200-bs8"
lora_dir = "shariqfarooq/loose-control-3dbox"

device = torch.device('cuda:2') if torch.cuda.is_available() else torch.device('cpu')

cn.pipe.controlnet = attach_loaders_mixin(cn.pipe.controlnet)
cn.pipe.controlnet.load_attn_procs(lora_dir)
cn.pipe = cn.pipe.to(torch_device=device, torch_dtype=torch.float16)



def set_attn_processor(module, processor, _remove_lora=False):
    def fn_recursive_attn_processor(name: str, module: torch.nn.Module, processor):
        if hasattr(module, "set_processor"):
            if not isinstance(processor, dict):
                module.set_processor(processor, _remove_lora=_remove_lora)
            else:
                module.set_processor(processor.pop(f"{name}.processor"), _remove_lora=_remove_lora)

        for sub_name, child in module.named_children():
            fn_recursive_attn_processor(f"{name}.{sub_name}", child, processor)

    for name, module in module.named_children():
        fn_recursive_attn_processor(name, module, processor)

def set_attn_processor_unet_decoder(module, processor, _remove_lora=False):
    for upblocks in module.up_blocks[-2:]:
        set_attn_processor(upblocks, processor, _remove_lora=_remove_lora)


def set_normal_attention(cn):
    cn.pipe.unet.set_attn_processor(AttnProcessor())
    return cn

def set_cf_attention(cn):
    set_attn_processor_unet_decoder(cn.pipe.unet, CrossFrameAttnProcessor())
    return cn



cn_with_cf = copy.deepcopy(cn)
cn_with_cf = set_cf_attention(cn_with_cf) 

@dataclass
class FixedInputs:
    prompt: str
    seed: int
    depth: PIL.Image.Image




negative_prompt = "blurry, text, caption, lowquality, lowresolution, low res, grainy, ugly"
def depth2image(prompt, seed, depth):
    seed = int(seed)
    gen = cn.text2image(prompt, control_image=depth, controlnet_conditioning_scale=1.0, generator=torch.Generator().manual_seed(seed), num_inference_steps=20, negative_prompt=negative_prompt)
    return gen

def edit_previous(prompt, seed, depth, fixed_inputs):
    seed = int(seed)
    control_image = [fixed_inputs.depth, depth]
    prompt = [fixed_inputs.prompt, prompt]
    neg_prompt = [negative_prompt, negative_prompt]
    generator = [torch.Generator().manual_seed(fixed_inputs.seed), torch.Generator().manual_seed(seed)]
    gen = cn_with_cf.text2image(prompt, control_image=control_image, controlnet_conditioning_scale=1.0, generator=generator, num_inference_steps=20, negative_prompt=neg_prompt)[-1]
    return gen

def run(prompt, seed, depth, should_edit, fixed_inputs):
    # all values below [3,3,3] in depth are set to [255,255,255]
    depth = depth.convert("RGB")
    # depth = np.array(depth)
    # depth[depth < 3] = 255
    # depth = PIL.Image.fromarray(depth)

    fixed_inputs = fixed_inputs[0]
    if should_edit and fixed_inputs is not None:
        return edit_previous(prompt, seed, depth, fixed_inputs)
    else:
        return depth2image(prompt, seed, depth)
    
def handle_edit_change(edit, prompt, seed, image_input, fixed_inputs):
    if edit:
        fixed_inputs[0] = FixedInputs(prompt, int(seed), image_input)
    else:
        fixed_inputs[0] = None
    return fixed_inputs


css = """

#image_output {
width: 512px;
height: 512px; 
"""


main_description = """
# LooseControl

This is the official demo for the paper [LooseControl: Lifting ControlNet for Generalized Depth Conditioning](https://shariqfarooq123.github.io/loose-control/).
Our 3D Box Editing allows users to interactively edit the 3D boxes representing objects in the scene. Users can change the position, size, and orientation of 3D boxes, allowing to quickly create and edit the scenes to their liking in a 3D-aware manner.
Best viewed on desktop.
"""

instructions_editor3d = """
## Instructions for Editor3D UI
- Use 'WASD' keys to move the camera.
- Click on an object to select it.
- Use the sliders to change the position, size, and orientation of the selected object. Sliders support click and drag for faster editing.
- Use the 'Add Box', 'Delete', and 'Duplicate' buttons to add, delete, and duplicate objects.
- Delete and Duplicate buttons work on the selected object. Duplicate creates a copy and selects it.
- Use the 'Toggle Mode' to switch between "normal" and "depth" mode. Final image sent to the model should be in "depth" mode.
- Use the 'Render' button to render the scene and send it to the model for generation.

### Lock style checkbox - Fixes the style of the latest generated image. 
This allows users to edit the 3D boxes without changing the style of the generated image. This is useful when the user is satisfied with the style/content of the generated image and wants to edit the 3D boxes without changing the overall essence of the scene.
It can be used to create stop motion videos like those shown [here](https://shariqfarooq123.github.io/loose-control/).

"""



with gr.Blocks(css=css) as demo:
    gr.Markdown(main_description)

    fixed_inputs = gr.State([None])
    with gr.Row():
        prompt = gr.Textbox(placeholder="Write your prompt", elem_id="input")
        seed = gr.Textbox(value=42, label="Seed", elem_id="seed")
        should_edit = gr.Checkbox(label="Lock style", elem_id="edit")
    
    with gr.Row():
        image_input = g3deditor(elem_id="image_input")
    
    with gr.Row():
        image_output = gr.Image(elem_id="image_output", type='pil')

    should_edit.change(fn=handle_edit_change, inputs=[should_edit, prompt, seed, image_input, fixed_inputs], outputs=[fixed_inputs])
    image_input.change(fn=run, inputs=[prompt, seed, image_input, should_edit, fixed_inputs], outputs=[image_output])
    with gr.Accordion("Instructions"):
        gr.Markdown(instructions_editor3d)

demo.launch()



