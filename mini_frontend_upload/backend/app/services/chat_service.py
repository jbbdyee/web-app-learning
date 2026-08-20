# chat_service.py
import os

from google import genai

from app.schemas.chat_schema import ChatRequest, ChatResponse
from app.core.supabase_config import get_supabase


def call_gemini(chat_request: ChatRequest) -> ChatResponse:
    api_key = os.getenv("GEMINI_API_KEY")
    model = os.getenv("GEMINI_MODEL","gemini-2.5-flash-lite",)

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(model=model,contents=chat_request.prompt,)

    reply = response.text

    supabase = get_supabase()

    supabase.table("chat_logs").insert({"user_id": chat_request.user_id,"prompt": chat_request.prompt,"reply": reply,}).execute()

    return ChatResponse(answer=reply)