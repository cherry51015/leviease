
# ⚖️Levi- Legal AI Assistant

An AI-powered assistant for **legal document intelligence**. This project enables lawyers, paralegals, and businesses to upload legal documents and interact with them using advanced NLP features such as **semantic Q&A, document verification, legal briefings, and clause extraction**.

The system combines **LLM-powered reasoning** with **custom document pipelines** to help professionals save time, reduce errors, and get actionable insights from large legal texts.

---

## 🚀 Features

* **📂 Document Upload** – Upload PDF, DOCX, or TXT legal documents.
* **💬 Chat with Your Document** – Ask questions in plain language and get context-aware answers.
* **🔍 Document Verifier** – Run AI-based verification checks to validate clauses, missing sections, and inconsistencies.
* **📝 Brief Mode** – Generate concise legal briefings or summaries for faster case preparation.
* **⚡ Fast & Interactive UI** – Streamlit interface for smooth interaction.

---

## 🏗️ Architecture

```
Streamlit UI
   |
   |--> File Loader (PDF/TXT/DOCX → Text)
   |--> Verifier Pipeline (run_document_verifier)
   |--> Brief Mode Pipeline (run_brief_mode)
   |--> Chat (ask_gemini with context + doc_text)
   |
   --> Backend Models (Google Gemini / FAISS index / Custom pipelines)
```

### Key Modules:

* **`llm.py`** → `ask_gemini(prompt, document)` handles context-aware legal Q&A.
* **`verifier.py`** → `run_document_verifier(text)` runs compliance + legal checks.
* **`briefings.py`** → `run_brief_mode(mode, text)` generates concise legal briefings.
* **`utils/file_loader.py`** → Handles PDF, DOCX, and TXT ingestion.

---

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/legal-ai-assistant.git
cd legal-ai-assistant
```

Create and activate a virtual environment:

```bash
python -m venv .venv
.venv\Scripts\activate   # On Windows
source .venv/bin/activate  # On macOS/Linux
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Running the App

To launch the Streamlit UI:

```bash
streamlit run app.py
```

Open in browser at **[http://localhost:8501](http://localhost:8501)**.

---

## 📌 Usage

1. **Upload a document** (PDF, DOCX, TXT) from the sidebar.
2. Choose an action:

   * 🔍 Run Verifier → Get structured JSON results of compliance checks.
   * 📝 Generate Briefing → AI-generated legal summary.
   * 💬 Chat → Ask questions directly about the document.
3. Review AI outputs, copy insights, or export JSON results.

---

## 🛠️ Tech Stack

* **Frontend:** [Streamlit](https://streamlit.io/)
* **Backend:** Python (FastAPI-ready endpoints)
* **LLM Integration:** Google Gemini API
* **Embeddings / Indexing:** FAISS
* **Utilities:** PyPDF2, python-docx, JSON, Pandas

---

## 📂 Project Structure

```
legal-ai-assistant/
│── app.py                 # Streamlit frontend
│── llm.py                 # LLM integration (Gemini, embeddings)
│── verifier.py            # Document verification pipeline
│── briefings.py           # Legal briefing pipeline
│── utils/
│   └── file_loader.py     # Document ingestion utilities
│── data/
│   └── faiss_index.bin    # Vector index for semantic search
│── requirements.txt
│── README.md
```

---

## 🔮 Roadmap

* [ ] Export results (JSON/PDF briefings).
* [ ] Add **clause comparison across multiple documents**.
* [ ] Integrate **legal precedent search** with multi-doc context.
* [ ] Deploy as a **FastAPI backend + Streamlit frontend** for production use.
* [ ] User authentication & document history.

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

---

## 📜 License

This project is licensed under the **MIT License**.

---

⚖ Built with AI to make legal work **simpler, faster, and smarter**.

---
