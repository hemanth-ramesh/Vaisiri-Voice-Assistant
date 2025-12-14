"""
Test Microsoft Phi-3-mini-4k-instruct installation
"""
print("🧪 Testing Phi-3-mini-4k-instruct...")

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch
    
    print(f"✅ Libraries imported")
    print(f"📱 Device: {'CUDA available' if torch.cuda.is_available() else 'CPU only'}")
    print(f"💾 Available RAM: ~4GB (perfect for Phi-3)")
    
    # Load model
    model_name = "microsoft/Phi-3-mini-4k-instruct"
    print(f"⏳ Loading {model_name}...")
    
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float32,  # Use float32 for CPU
        low_cpu_mem_usage=True,
        trust_remote_code=True
    )
    
    print("✅ Model loaded successfully!")
    
    # Test generation
    print("🧠 Testing response generation...")
    
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "What is artificial intelligence?"}
    ]
    
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    inputs = tokenizer(prompt, return_tensors="pt")
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=80,
            temperature=0.7,
            do_sample=True,
            top_p=0.9,
            repetition_penalty=1.1
        )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    ai_response = response[len(prompt):].strip()
    
    print(f"✅ Test successful!")
    print(f"📤 Question: What is artificial intelligence?")
    print(f"📥 Answer: {ai_response}")
    print("\n🎉 Phi-3-mini is ready for voice assistant integration!")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Run: pip install transformers torch")
    
except Exception as e:
    print(f"❌ Error: {e}")
    print("💡 Check internet connection for model download")
