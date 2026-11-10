"""
WhatsApp AI Automation & Webhook API
------------------------------------
A backend microservice built with FastAPI to receive incoming WhatsApp webhooks
(via Typebot, ManyChat, Make, or Evolution API), process client queries using AI logic,
and return contextualized, automated responses.
"""

from fastapi import FastAPI, HTTPException, status, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import datetime

# Initialize FastAPI app with metadata for Swagger UI
app = FastAPI(
    title="WhatsApp AI Automation Engine",
    description="A microservice designed to handle WhatsApp message automation, AI response generation, and webhook integrations.",
    version="1.0.0"
)

# ------------------------------------------------------------------------------
# Data Models (Pydantic Schemas)
# ------------------------------------------------------------------------------

class IncomingMessagePayload(BaseModel):
    """Schema for incoming WhatsApp messages received via Webhook."""
    phone_number: str = Field(..., example="5511999999999", description="Sender's WhatsApp number with country code")
    user_name: Optional[str] = Field(default="Cliente", example="Carlos Silva", description="Name of the user sending the message")
    message_text: str = Field(..., example="Olá, gostaria de saber os preços e planos disponíveis.", description="Message text sent by the client")
    session_id: Optional[str] = Field(default=None, example="sess_123456", description="Optional conversation session ID")

class AIResponse(BaseModel):
    """Schema for outbound AI-generated response."""
    status: str = Field(..., example="success")
    phone_number: str = Field(..., example="5511999999999")
    reply_text: str = Field(..., example="Olá Carlos! Nossos planos começam a partir de R$ 99/mês...")
    timestamp: str = Field(..., example="2026-11-09T22:50:00Z")

# ------------------------------------------------------------------------------
# In-Memory Database / Simulators (For Prototyping)
# ------------------------------------------------------------------------------

# Simple system prompt configuration for the AI behavior
SYSTEM_PROMPT = (
    "Você é um assistente virtual de atendimento ao cliente amigável e profissional. "
    "Sua função é responder dúvidas sobre serviços, preços e automações de forma clara e objetiva."
)

# Conversation history cache (Simulated memory per phone number)
conversation_history: Dict[str, List[Dict[str, str]]] = {}

# ------------------------------------------------------------------------------
# Core AI Logic Helper
# ------------------------------------------------------------------------------

def process_ai_response(phone: str, user_name: str, message: str) -> str:
    """
    Simulates AI LLM processing (OpenAI / Gemini API).
    In production, replace this block with an actual API call using official SDKs.
    """
    # Maintain basic conversation history per user
    if phone not in conversation_history:
        conversation_history[phone] = []
    
    conversation_history[phone].append({"role": "user", "content": message})
    
    # Placeholder rule-based AI simulation
    lowered_msg = message.lower()
    if "preço" in lowered_msg or "valor" in lowered_msg or "quanto custa" in lowered_msg:
        reply = f"Olá {user_name}! Nossos pacotes de automação variam conforme a necessidade do seu negócio. O plano básico começa em R$ 150/mês. Gostaria de agendar uma demonstração?"
    elif "funciona" in lowered_msg or "suporte" in lowered_msg:
        reply = f"Olá {user_name}! Nossa automação responde clientes 24/7 via WhatsApp, qualifica leads e envia dados para seu CRM. Posso te enviar um resumo?"
    else:
        reply = f"Olá {user_name}! Recebi sua mensagem: '{message}'. Como posso ajudar no atendimento da sua empresa hoje?"
        
    conversation_history[phone].append({"role": "assistant", "content": reply})
    return reply

# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    """Health check endpoint to verify service availability."""
    return {
        "status": "online",
        "service": "WhatsApp AI Automation API",
        "documentation": "/docs",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }

@app.post("/v1/webhook/whatsapp", response_model=AIResponse, status_code=status.HTTP_200_OK)
def handle_whatsapp_webhook(payload: IncomingMessagePayload):
    """
    Webhook Endpoint: Receives messages from WhatsApp integrations (Make, Typebot, ManyChat),
    processes the text through AI, and returns the response payload.
    """
    if not payload.message_text.strip():
        raise HTTPException(
            status_code=Status.HTTP_400_BAD_REQUEST,
            detail="Message text cannot be empty."
        )
    
    # Process AI logic
    reply_text = process_ai_response(
        phone=payload.phone_number,
        user_name=payload.user_name,
        message=payload.message_text
    )
    
    return AIResponse(
        status="success",
        phone_number=payload.phone_number,
        reply_text=reply_text,
        timestamp=datetime.datetime.utcnow().isoformat()
    )

@app.get("/v1/history/{phone_number}")
def get_user_history(phone_number: str):
    """Retrieves conversation history for a specific WhatsApp phone number."""
    if phone_number not in conversation_history:
        raise HTTPException(status_code=404, detail="No conversation history found for this phone number.")
    
    return {
        "phone_number": phone_number,
        "history": conversation_history[phone_number]
    }