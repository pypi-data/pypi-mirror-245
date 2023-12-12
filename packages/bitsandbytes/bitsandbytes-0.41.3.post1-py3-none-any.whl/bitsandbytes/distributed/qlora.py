from accelerate import init_empty_weights
from accelerate.utils import set_module_tensor_to_device
from peft import LoraConfig, TaskType, get_peft_model
import safetensors
import torch
from torch import nn
from transformers import (
    AutoConfig,
    AutoTokenizer,
    BitsAndBytesConfig,
    LlamaForCausalLM,
)
from transformers.integrations.bitsandbytes import replace_with_bnb_linear
from transformers.modeling_utils import no_init_weights
from transformers.utils import SAFE_WEIGHTS_INDEX_NAME, WEIGHTS_INDEX_NAME, hub

from bitsandbytes.nn import Linear4bit, Linear8bitLt

mid = "meta-llama/Llama-2-7b-hf"
# mid = "stabilityai/stablelm-3b-4e1t"
# mid = 'Phind/Phind-CodeLlama-34B-v2'

tokenizer = AutoTokenizer.from_pretrained(mid, trust_remote_code=True)
tokenizer.pad_token_id = tokenizer.eos_token_id
cfg = AutoConfig.from_pretrained(mid, trust_remote_code=True)

qcfg = BitsAndBytesConfig(load_in_8bit=True)

with init_empty_weights():
    model = LlamaForCausalLM(cfg).eval()
    model = replace_with_bnb_linear(model, quantization_config=qcfg)
    
model.is_loaded_in_8bit = True

idx = hub.cached_file(mid, SAFE_WEIGHTS_INDEX_NAME)
fns, maps = hub.get_checkpoint_shard_files(mid, idx)

for filename in fns:
    shard = safetensors.torch.load_file(filename)
    for name, parameter in shard.items():
        set_module_tensor_to_device(
            model,
            name,
            'cuda',
            value=parameter,
            dtype=torch.float16
        )

for name, buffer in model.named_buffers():
    submodule_name, _, buffer_name = name.rpartition('.')
    setattr(model.get_submodule(submodule_name), buffer_name, buffer.cuda())

target_modules = [l + "_proj" for l in ["k", 'v', "q", "o", "gate", "up", "down"]]
peft_config = LoraConfig(
    r=8,
    lora_alpha=32,
    target_modules=target_modules,
    bias="none",
    task_type="CAUSAL_LM",
    lora_dropout=0.05,
    inference_mode=False)

with no_init_weights():
    model = get_peft_model(model, peft_config)

model = FSDP(
    model,
    auto_wrap_policy= my_auto_wrapping_policy if train_config.use_peft else wrapping_policy,
    cpu_offload=CPUOffload(offload_params=True) if fsdp_config.fsdp_cpu_offload else None,
    mixed_precision=mixed_precision_policy if not fsdp_config.pure_bf16 else None,
    sharding_strategy=fsdp_config.sharding_strategy,
    device_id=torch.cuda.current_device(),
    limit_all_gathers=True,
    sync_module_states=train_config.low_cpu_fsdp,
    param_init_fn=lambda module: module.to_empty(device=torch.device("cuda"), recurse=False)

prompt = "Titus von Koeller is"
inputs = tokenizer(prompt, return_tensors="pt")

generate_ids = model.generate(
    **inputs.to('cuda'), max_length=300)[:, len(inputs['input_ids'][0]):]

print(f"{prompt} " +
    tokenizer.batch_decode(
        generate_ids, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0])
