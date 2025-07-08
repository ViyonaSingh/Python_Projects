from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# === Load DeepSeek Code model ===
model_name = "deepseek-ai/deepseek-coder-1.3b-instruct"
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True, torch_dtype=torch.float32)

print("💡 Ask me to write code! (type 'exit' to quit)\n")

while True:
    instruction = input("📝 Instruction: ")
    if instruction.lower() == "exit":
        break

    prompt = f"<|user|>\n{instruction}\n<|assistant|>\n"
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=128,
        do_sample=True,
        top_p=0.95,
        temperature=0.7
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    answer = response.split("<|assistant|>")[-1].strip()

    print("\n✅ Generated Code:\n")
    print(answer)
    print("\n" + "="*50 + "\n")
