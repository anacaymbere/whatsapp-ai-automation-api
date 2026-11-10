# 💬 WhatsApp AI Automation & Webhook Engine

> A high-performance RESTful microservice built with **Python**, **FastAPI**, and **Pydantic** to receive incoming WhatsApp webhooks, process messages with AI logic (LLMs), and automate customer support responses.

---

## 🚀 Features

- **Webhook Receiver**: Readily integrates with No-Code & Automation platforms (Typebot, Make.com, ManyChat, Evolution API).
- **AI Processing Engine**: Handles contextual response generation for incoming customer queries.
- **In-Memory History Tracker**: Maintains user session context per WhatsApp phone number for multi-turn conversations.
- **Data Validation & Typing**: Enforces strict request payloads using **Pydantic**.
- **Interactive Documentation**: Auto-generated Swagger UI (`/docs`) and ReDoc (`/redoc`).

---

## 🛠️ Tech Stack

* **Python 3.11+**
* **FastAPI**: Modern, fast web framework for building APIs with Python.
* **Uvicorn**: High-performance ASGI web server.
* **Pydantic v2**: Data validation and setting management.

---

## 📂 Project Structure

```text
whatsapp-ai-automation/
│
├── main.py              # FastAPI core routes, Webhook endpoints, and AI logic
├── requirements.txt     # Python dependencies
└── README.md            # Technical documentation
