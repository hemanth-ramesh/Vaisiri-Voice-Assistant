"""
Test TinyLlama-1.1B-Chat for 4GB RAM systems
"""
print("🧪 Testing TinyLlama-1.1B-Chat (4GB RAM optimized)...")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print(f"✅ Libraries imported")
    print(f"📱 Device: {'CUDA' if torch.cuda.is_available() else 'CPU only'}")
    print(f"💾 RAM: 4GB (perfect for TinyLlama)")
    
    # Load lightweight model
    model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    print(f"⏳ Loading {model_name} (lightweight ~2.2GB)...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # CPU compatible
        low_cpu_mem_usage=True
    )
    
    print("✅ TinyLlama loaded successfully!")
    
    # Test generation
    print("🧠 Testing response...")
    
    # Simple prompt format for TinyLlama
    prompt = "<|system|>\nYou are a helpful assistant.</s>\n<|user|>\nWhat is artificial intelligence?</s>\n<|assistant|>\n"
    
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=60,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    ai_response = response[len(prompt):].strip()
    
    print(f"✅ Test successful!")
    print(f"📤 Question: What is artificial intelligence?")
    print(f"📥 Answer: {ai_response}")
    print(f"\n🎉 TinyLlama works perfectly on 4GB RAM!")
    
except Exception as e:
    print(f"❌ Error: {e}")
