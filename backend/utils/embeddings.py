import os
import json
import time
import numpy as np
import google.generativeai as genai
from tqdm import tqdm
from dotenv import load_dotenv

# ========== CONFIG ==========
DATA_PATH = "merged_dataset.jsonl"
EMB_PATH = "embeddings.jsonl"
BATCH_SIZE = 50         # batch for speed + quota
MAX_RETRIES = 5
RETRY_DELAY = 10        # exponential backoff
SLEEP_ON_ALL_KEYS = 60  # wait if all keys exhausted
EMBED_MODEL = "models/embedding-001"  # 768-dim
# ============================

# 🔑 Load environment variables
load_dotenv()
# "AIzaSyBpLF4w6gUTFf5PtNMX17DKUFjH9DPPtmE",
API_KEYS = ["YOU API KEY 1 HERE","IF YOU HAVE ANOTHER BILLING KEY THEN KEY 2"]
API_KEYS = [k.strip() for k in API_KEYS if k.strip()]
if not API_KEYS:
    raise ValueError("❌ GEMINI_KEYS not found in .env (format: GEMINI_KEYS=key1,key2)")

# Keep rotating index
key_index = -1
def switch_key():
    """Rotate API key."""
    global key_index
    key_index = (key_index + 1) % len(API_KEYS)
    genai.configure(api_key=API_KEYS[key_index])
    print(f"🔑 Using API key {key_index+1}/{len(API_KEYS)}")

# Initialize first key
switch_key()

def get_embeddings_batch(texts, batch_id=0, attempt=1, tried_keys=None):
    """Get embeddings for a batch of texts with retries + multi-key rotation."""
    global key_index
    if tried_keys is None:
        tried_keys = set()

    try:
        print(f"\n🔍 DEBUG: Embedding batch {batch_id}, attempt {attempt}, using key {key_index+1}")
        embeddings = []
        for t in texts:
            resp = genai.embed_content(
                model=EMBED_MODEL,
                content=t,
                task_type="retrieval_document"
            )
            emb = np.array(resp["embedding"], dtype="float32")
            embeddings.append(emb)

        print(f"✅ Success: Got {len(embeddings)} embeddings of length {len(embeddings[0])}")
        return embeddings


    except Exception as e:
        err = str(e).lower()
        print(f"❌ Error on batch {batch_id}, attempt {attempt}: {e}")

        # Handle quota/rate errors
        if "quota" in err or "429" in err:
            tried_keys.add(key_index)
            if len(tried_keys) >= len(API_KEYS):
                print(f"⏳ All {len(API_KEYS)} API keys exhausted. Sleeping {SLEEP_ON_ALL_KEYS}s...")
                time.sleep(SLEEP_ON_ALL_KEYS)
                tried_keys.clear()
            switch_key()
            return get_embeddings_batch(texts, batch_id, attempt, tried_keys)

        # Other errors → exponential backoff
        elif attempt < MAX_RETRIES:
            wait_time = RETRY_DELAY * attempt
            print(f"⏳ Waiting {wait_time}s before retry...")
            time.sleep(wait_time)
            return get_embeddings_batch(texts, batch_id, attempt + 1, tried_keys)
        else:
            print(f"🚨 Failed batch {batch_id} after {MAX_RETRIES} retries")
            return [None] * len(texts)
# 🔧 Force resume batch number
RESUME_BATCH = 2957  # 👈 change this if needed

def embed_texts(text: str):
    """
    Get embedding vector for a single document (float32 numpy array).
    """
    try:
        resp = genai.embed_content(
            model=EMBED_MODEL,
            content=text,
            task_type="retrieval_query"   # query mode for search
        )
        return np.array(resp["embedding"], dtype="float32")
    except Exception as e:
        print(f"❌ Failed to embed single text: {e}")
        return None



def main():
    print(f"📖 Reading dataset: {DATA_PATH}")
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f]

    print(f"✅ Loaded {len(records)} records")

    # ✅ Force resume from specific batch
    processed = RESUME_BATCH * BATCH_SIZE
    print(f"🔄 Forcing resume from record {processed} (batch {RESUME_BATCH})")

    # Open in append mode instead of overwrite
    with open(EMB_PATH, "a", encoding="utf-8") as out_f:
        for i in tqdm(range(processed, len(records), BATCH_SIZE), desc="🔢 Embedding batches"):
            batch_records = records[i:i + BATCH_SIZE]
            texts, meta = [], []

            for j, r in enumerate(batch_records):
                text = r.get("output") or r.get("input") or r.get("text", "")
                if not text.strip():
                    continue
                text = text.strip()
                texts.append(text)
                meta.append({
                    "id": r.get("id", f"record_{i+j}"),
                    "text": text
                })

            if not texts:
                continue

            embeddings = get_embeddings_batch(texts, batch_id=i // BATCH_SIZE)

            for m, emb in zip(meta, embeddings):
                if emb is None:
                    continue
                out_f.write(json.dumps({
                    "id": m["id"],
                    "text": m["text"],
                    "embedding": emb.tolist()
                }, ensure_ascii=False) + "\n")

                snippet = m["text"][:60].replace("\n", " ")
                print(f"✅ Embedded ({m['id']}): {snippet}...")

    print(f"💾 Saved embeddings to {EMB_PATH}")
    print("🎉 All embeddings generated successfully!")



if __name__ == "__main__":
    main()
