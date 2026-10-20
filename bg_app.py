import time
from fastapi import FastAPI, BackgroundTasks, Request, HTTPException, status
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Microservice with Background Tasks & Rate Limiter")

# Simple in-memory rate limiter (5 requests per 10 seconds per IP)
RATE_LIMIT_DURATION = 10
RATE_LIMIT_MAX_REQUESTS = 5
request_history = {}

def check_rate_limit(client_ip: str):
    now = time.time()
    history = request_history.get(client_ip, [])
    # 10 second se puraane timestamps hatao
    history = [t for t in history if now - t < RATE_LIMIT_DURATION]
    if len(history) >= RATE_LIMIT_MAX_REQUESTS:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded! Please wait before making more requests."
        )
    history.append(now)
    request_history[client_ip] = history

# Background Worker simulation (Async processing)
def process_email_notification(email: str, subject: str, message: str):
    print(f"\n[BACKGROUND TASK STARTED] Sending email to: {email}...")
    time.sleep(3)  # Heavy processing / API call delay
    with open("notifications_log.txt", "a") as f:
        f.write(f"To: {email} | Subject: {subject} | Content: {message}\n")
    print(f"[BACKGROUND TASK FINISHED] Email delivered to: {email}!\n")

# Pydantic Schema
class NotificationRequest(BaseModel):
    email: str
    subject: str
    message: str

@app.post("/send-notification/", status_code=status.HTTP_202_ACCEPTED)
async def trigger_notification(
    payload: NotificationRequest,
    background_tasks: BackgroundTasks,
    request: Request
):
    # 1. Rate limiter check
    client_ip = request.client.host if request.client else "127.0.0.1"
    check_rate_limit(client_ip)

    # 2. Background task queue me daalna
    background_tasks.add_task(
        process_email_notification,
        payload.email,
        payload.subject,
        payload.message
    )

    # 3. User ko foran 202 Accepted response wapas bhejna
    return {
        "status": "Accepted",
        "message": "Notification job queued in the background successfully.",
        "recipient": payload.email
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "background-worker-microservice"}