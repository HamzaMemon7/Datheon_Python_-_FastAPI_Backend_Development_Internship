from fastapi import FastAPI

# Pehle se mojood charon apps ko import kar rahe hain
from main import app as bookstore_app
from auth_app import app as auth_app
from db_app import app as db_app
from bg_app import app as bg_app

# Master FastAPI App
app = FastAPI(
    title="Datheon Internship - Combined Tasks API",
    description="All 4 Tasks running together in a unified server.",
    version="1.0.0"
)

# Root route
@app.get("/")
def home():
    return {
        "status": "Online",
        "message": "All 4 Datheon backend tasks are loaded and running successfully!",
        "endpoints": {
            "task_1_bookstore": "/bookstore/docs/",
            "task_2_auth_rbac": "/auth/docs/",
            "task_3_database": "/database/docs/",
            "task_4_background_tasks": "/background/docs/"
        }
    }

# Charon apps ko alag-alag prefixes ke sath mount karna
app.mount("/bookstore", bookstore_app)
app.mount("/auth", auth_app)
app.mount("/database", db_app)
app.mount("/background", bg_app)