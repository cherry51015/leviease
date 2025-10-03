import re
import numpy as np

# Rule-based checker
def run_document_verifier_rules(text: str):
    checks = {
        "signatures": bool(re.search(r"signature|signed by", text, re.IGNORECASE)),
        "dates": bool(re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", text)) or bool(re.search(r"\b\d{4}\b", text)),
        "parties": bool(re.search(r"between\s+\w+", text, re.IGNORECASE)),
        "jurisdiction": bool(re.search(r"jurisdiction|court|state of|high court|supreme court", text, re.IGNORECASE)),
    }
    score = sum(checks.values())
    return checks, score


# Main verifier — uses precomputed chunks & FAISS index
def run_document_verifier(doc_text, doc_chunks, doc_index, faiss_docs, top_k=3):
    rules, sufficiency_score = run_document_verifier_rules(doc_text)

    chunk_results = []
    for i, chunk in enumerate(doc_chunks):
        try:
            # Find nearest neighbors from prebuilt FAISS index
            emb = np.array([doc_index.reconstruct(i)], dtype="float32")
            D, I = doc_index.search(emb, top_k)

            similar_cases = []
            for idx, score in zip(I[0], D[0]):
                if 0 <= idx < len(faiss_docs["ids"]):
                    doc_meta = {
                        "id": faiss_docs["ids"][idx],
                        "summary": faiss_docs["texts"][idx][:300] + "...",
                        "similarity_score": float(score)
                    }
                    similar_cases.append(doc_meta)

        except Exception:
            similar_cases = []

        chunk_results.append({
            "chunk_index": i,
            "chunk_preview": chunk[:100] + "...",
            "similar_cases": similar_cases
        })

    return {
        "sufficiency_score": sufficiency_score,
        "rule_checklist": rules,
        "chunks": chunk_results
    }
