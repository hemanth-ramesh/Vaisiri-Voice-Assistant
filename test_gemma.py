"""
Test Google Gemma-2B-IT installation
"""
try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print("🧪 Testing Gemma-2B-IT...")
    print(f"Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
    
    # Test loading
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-2b-it")
    print("✅ Tokenizer loaded!")
    
    model = AutoModelForCausalLM.from_pretrained(
        "google/gemma-2b-it",
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        low_cpu_mem_usage=True
    )
    print("✅ Model loaded!")
    
    # Test generation
    messages = [{"role": "user", "content": "What is artificial intelligence?"}]
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(**inputs, max_new_tokens=50, temperature=0.7)
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    print(f"✅ Test response: {response[len(prompt):].strip()}")
    print("🎉 Gemma-2B-IT is working perfectly!")
    
except Exception as e:
    print(f"❌ Error: {e}")
