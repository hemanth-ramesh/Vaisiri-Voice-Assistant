# scripts/build_faiss_index.py
import argparse
import json
from pathlib import Path
from tqdm import tqdm
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

def parse_args():
    parser = argparse.ArgumentParser(
        description="Build a FAISS index from Wikipedia paragraphs"
    )
    parser.add_argument(
        "--input", required=True,
        help="Path to JSONL file with one paragraph per line {\"id\":..., \"text\":...}"
    )
    parser.add_argument(
        "--index-path", required=True,
        help="Output file for FAISS index (e.g. data/wiki_index.faiss)"
    )
    parser.add_argument(
        "--passages-output", required=True,
        help="Outputs the passages file needed by the retriever (JSONL)"
    )
    return parser.parse_args()

def load_paragraphs(path):
    paragraphs = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            obj = json.loads(line)
            paragraphs.append((obj["id"], obj["text"]))
    return paragraphs

def main():
    args = parse_args()
    
    # Load paragraphs
    paras = load_paragraphs(args.input)
    ids, texts = zip(*paras)
    
    # Use a SentenceTransformer to embed
    model = SentenceTransformer("all-MiniLM-L6-v2")  # small, fast
    print("🔍 Encoding paragraphs...")
    embeddings = model.encode(list(texts), show_progress_bar=True, convert_to_numpy=True)
    
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    print("📦 Adding to FAISS index...")
    index.add(embeddings)
    
    # Save index
    print(f"💾 Writing FAISS index to {args.index_path}")
    faiss.write_index(index, args.index_path)
    
    # Save passages JSONL required by RagRetriever
    Path(args.passages_output).parent.mkdir(parents=True, exist_ok=True)
    print(f"💾 Writing passages to {args.passages_output}")
    with open(args.passages_output, "w", encoding="utf-8") as out:
        for pid, txt in paras:
            json.dump({"title": "", "text": txt}, out)
            out.write("\n")
    
    print("✅ FAISS index and passages file created successfully.")

if __name__ == "__main__":
    main()
