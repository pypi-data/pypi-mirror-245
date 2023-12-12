from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    "facebook/opt-350m", 
    load_in_4bit=True,
    device_map="auto"
)
...