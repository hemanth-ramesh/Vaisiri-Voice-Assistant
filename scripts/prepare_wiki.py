#!/usr/bin/env python3
"""
Prepare Wikipedia paragraphs JSONL and FAISS index from HF wiki_dpr dataset
"""
import json
from pathlib import Path
from tqdm import tqdm
from datasets import load_dataset
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def main():
    # 1) Load wiki_dpr paragraphs from HF
    ds = load_dataset("wiki_dpr", "paragraphs", split="train")
    
    # 2) Ensure data directory
    out_dir = Path("data")
    out_dir.mkdir(exist_ok=True)
    
    # 3) Write JSONL of (id, text)
    passages_file = out_dir / "wiki_paragraphs.jsonl"
    print(f"💾 Writing paragraphs to {passages_file}")
    with open(passages_file, "w", encoding="utf-8") as f:
        for item in tqdm(ds, desc="Writing JSONL"):
            json.dump({"id": item["id"], "text": item["text"]}, f)
            f.write("\n")
    
    # 4) Embed with sentence-transformers
    print("🔍 Encoding paragraphs for FAISS index...")
    model = SentenceTransformer("all-MiniLM-L6-v2")
    texts = [item["text"] for item in ds]
    embeddings = model.encode(texts, show_progress_bar=True, convert_to_numpy=True)
    
    # 5) Build FAISS index
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    print("📦 Adding embeddings to FAISS index...")
    index.add(embeddings)
    
    index_file = out_dir / "wiki_index.faiss"
    print(f"💾 Saving FAISS index to {index_file}")
    faiss.write_index(index, str(index_file))
    
    print("✅ Preparation complete.")

if __name__ == "__main__":
    main()
