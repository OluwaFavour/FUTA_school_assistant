import asyncio
from fastapi import (
    FastAPI,
    Request,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.middleware.cors import CORSMiddleware
import logging

from starlette.middleware.sessions import SessionMiddleware

from . import settings

app = FastAPI(
    debug=settings.DEBUG,
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Add Session Middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET_KEY,
    same_site=settings.SESSION_SAME_SITE,
    https_only=settings.SESSION_SECURE,
    max_age=(settings.SESSION_EXPIRE_DAYS * 24 * 60 * 60),
)

# Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings.ALLOW_CREDENTIALS,
    allow_methods=settings.ALLOWED_METHODS,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_headers=["*"],
)


# WebSocket route
@app.websocket("/ws/chat/soc")
async def soc_chat_route(websocket: WebSocket):
    welcome_message = (
        "Welcome to the chat, ask me anything about FUTA School of Computing!"
    )

    # Initialize or retrieve conversation history
    session_history: list[dict[str, str]] = websocket.session.get(
        "conversation_history", []
    )

    await websocket.accept()
    try:
        # Send the conversation history if it exists
        if session_history:
            for message in session_history:
                await websocket.send_json(data=message)
        else:
            # Send a welcome message if no history exists
            await websocket.send_text(welcome_message)
            session_history.append({"role": "assistant", "content": welcome_message})
            websocket.session["conversation_history"] = session_history

        # Initialize OpenAI client
        openai_client = settings.OPENAI_CLIENT

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            session_history.append({"role": "user", "content": data})

            # Validate and process the message
            if not data.strip():
                await websocket.send_text("Please provide a message, I'm here to help!")
                session_history.append(
                    {
                        "role": "assistant",
                        "content": "Please provide a message, I'm here to help!",
                    }
                )
                websocket.session["conversation_history"] = session_history
                continue

            try:
                # Query OpenAI API for an answer
                answer = await asyncio.to_thread(
                    openai_client.ask_soc_question,
                    messages=session_history,
                )
                await websocket.send_text(answer)
                session_history.append({"role": "assistant", "content": answer})
                websocket.session["conversation_history"] = session_history

            except Exception as e:
                logging.error(f"OpenAI API Error: {e}")
                error_message = (
                    "I'm sorry, I couldn't process your request. Please try again."
                )
                await websocket.send_text(error_message)
                session_history.append({"role": "assistant", "content": error_message})
                websocket.session["conversation_history"] = session_history

    except WebSocketDisconnect:
        logging.info("Client disconnected from WebSocket")
    except WebSocketException as e:
        logging.error(f"WebSocketException: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        # Ensure session is saved when the connection is closed
        websocket.session["conversation_history"] = session_history


# WebSocket route
@app.websocket("/ws/chat/admission")
async def admission_chat_route(websocket: WebSocket):
    welcome_message = "Welcome to the chat, ask me anything about Federal University of Technology Akure (FUTA) Admission Enquiry"

    # Initialize or retrieve conversation history
    session_history: list[dict[str, str]] = websocket.session.get(
        "conversation_history", []
    )

    await websocket.accept()
    try:
        # Send the conversation history if it exists
        if session_history:
            for message in session_history:
                await websocket.send_json(data=message)
        else:
            # Send a welcome message if no history exists
            await websocket.send_text(welcome_message)
            session_history.append({"role": "assistant", "content": welcome_message})
            websocket.session["conversation_history"] = session_history

        # Initialize OpenAI client
        openai_client = settings.OPENAI_CLIENT

        # Listen for messages
        while True:
            data = await websocket.receive_text()
            session_history.append({"role": "user", "content": data})

            # Validate and process the message
            if not data.strip():
                await websocket.send_text("Please provide a message, I'm here to help!")
                session_history.append(
                    {
                        "role": "assistant",
                        "content": "Please provide a message, I'm here to help!",
                    }
                )
                websocket.session["conversation_history"] = session_history
                continue

            try:
                # Query OpenAI API for an answer
                answer = await asyncio.to_thread(
                    openai_client.ask_admission_question,
                    messages=session_history,
                )
                await websocket.send_text(answer)
                session_history.append({"role": "assistant", "content": answer})
                websocket.session["conversation_history"] = session_history

            except Exception as e:
                logging.error(f"OpenAI API Error: {e}")
                error_message = (
                    "I'm sorry, I couldn't process your request. Please try again."
                )
                await websocket.send_text(error_message)
                session_history.append({"role": "assistant", "content": error_message})
                websocket.session["conversation_history"] = session_history

    except WebSocketDisconnect:
        logging.info("Client disconnected from WebSocket")
    except WebSocketException as e:
        logging.error(f"WebSocketException: {e}")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    finally:
        # Ensure session is saved when the connection is closed
        websocket.session["conversation_history"] = session_history
