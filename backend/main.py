# .venv\Scripts\activate.bat

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router_chat import router as chat_router
from services.memory import init_pool
from services.faq_store import initialize_faq_store

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # http://localhost:5173
    allow_credentials=True,
    allow_methods=["*"],                          
    allow_headers=["*"],                          
)

@app.on_event("startup")
async def startup_event():
    initialize_faq_store()
    await init_pool()

app.include_router(chat_router)