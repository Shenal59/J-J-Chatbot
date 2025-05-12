# Lens4U Chatbot MVP

A minimal, proof‑of‑concept chatbot for guiding first‑time contact lens users. Built with:

- **Backend**: FastAPI, Redis, and OpenAI RAG pipeline  
- **Frontend**: React, Tailwind CSS, and Axios  
- **Data**: JSONL seed file for FAQ entries  
- **Deployment**: Optional Docker & Docker Compose

---

## 🗂️ File Structure

```plaintext
lens4u-mvp/                # Project root

├── backend/               # FastAPI service
│   ├── main.py            # App factory, CORS, startup hooks
│   ├── router_chat.py     # /chat endpoint & Pydantic models
│   ├── services/          # Business logic modules
│   │   ├── rag.py         # RAG orchestration & strict FAQ fallback
│   │   ├── memory.py      # Redis session & embedding cache
│   │   ├── faq_store.py   # Load & embed FAQs from data/faqs.jsonl
│   │   └── logger.py      # Structured JSON logging
│   ├── data/              # Seed data
│   │   └── faqs.jsonl     # One‑line JSONL FAQ records
│   ├── requirements.txt   # Python dependencies
│   └── Dockerfile         # Containerization

├── frontend/              # React chat widget
│   ├── package.json       # npm dependencies & scripts
│   ├── tailwind.config.js # Tailwind CSS config
│   ├── postcss.config.js  # PostCSS config
│   ├── public/            # Static HTML
│   │   └── index.html     # Entry HTML file
│   └── src/               # React source code
│       ├── index.js       # App entry point
│       ├── index.css      # Tailwind directives
│       └── App.jsx        # Chat UI & API calls

├── docker-compose.yml     # Orchestrate backend + Redis
├── .env                   # Environment variables (ignored by git)
└── README.md              # This documentation
``` 

---

## 🔧 Prerequisites

- **Python** ≥ 3.11
- **Node.js** & **npm** ≥ 16.x
- **Redis** (local install or via Docker)
- **OpenAI API Key**

---

## ⚙️ Environment Variables

Create a file named `.env` at the project root with:

```dotenv
OPENAI_API_KEY=sk-<your-full-key>
REDIS_URL=redis://localhost:6379/0
```

> Ensure `.env` is in `.gitignore`. Use `python-dotenv` in `backend/main.py` to load it.

---

## 🚀 Backend Setup & Run

1. **Navigate to backend**  
   ```bash
   cd /backend
   ```
2. **Create a virtual environment**  
   ```bash
   python3 -m venv .venv
   .venv\Scripts\activate.bat
   ```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt
   ```
4. **Start Redis** (if not using Docker)  
   ```bash
   # In admin CMD
   cd "C:\Program Files\Redis"
   redis-server.exe

   # Alternatively run the file directly in your file manager

   # Test
   redis-cli.exe ping
   ```
   
5. **Launch the API server**  
   ```bash
   uvicorn main:app --reload --port 8000
   ```

- **Interactive docs**: open `http://localhost:8000/docs` and test `/chat`.

---

## 🖥️ Frontend Setup & Run

1. **Navigate to frontend**  
   ```bash
   cd frontend
   ```
2. **Install npm packages**  
   ```bash
   npm install
   ```
3. **Configure Tailwind** (if not done):
   ```bash
   npx tailwindcss init -p
   ```
   - Add `./src/**/*.{js,jsx}` to `content` in `tailwind.config.js`.
   - Include `@tailwind` directives in `src/index.css`.
4. **Start development server**  
   ```bash
   npm start
   ```

- **App URL**: `http://localhost:3000` (communicates with `http://localhost:8000/chat`).

---

## 🐳 Docker (Optional)

From project root:
```bash
docker-compose up --build
```
- **Backend**: `http://localhost:8000`  
- **Redis**: `localhost:6379`

---

## 🎯 Usage

1. Open the frontend at `http://localhost:3000`.  
2. Ask a question (e.g. “How often should I replace daily lenses?”).  
3. View the answer with citation.  
4. Follow guided prompts for lens type and personalized schedule.

---

## 🛠️ Customization

- **Add or update FAQs**: edit `backend/data/faqs.jsonl`.  
- **Adjust RAG threshold**: modify `RAG_CONFIDENCE_THRESHOLD` in `backend/services/rag.py`.  
- **UI tweaks**: update Tailwind classes in `src/App.jsx` or global styles.

---

## 🚀 Next Steps

- Deploy frontend to Vercel and backend to Azure Container Apps.  
- Integrate a managed vector store (e.g., Pinecone) for production.  
- Add voice channels (Twilio) and multilingual support.

---