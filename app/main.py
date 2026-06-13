from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os

from app.models.user import User
from app.models.document import DocumentTracker

from app.api.auth import router as auth_router
from app.api.documents import router as document_router
from app.api.document_upload import router as document_upload_router

app = FastAPI(
    title="AIRAG API"
)

# =========================
# ROUTERS
# =========================
app.include_router(auth_router)
app.include_router(document_router)
app.include_router(document_upload_router)

# =========================
# STATIC FILE SERVING (IMPORTANT FIX)
# =========================
UPLOAD_DIR = "uploads"

if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

app.mount(
    "/uploads",
    StaticFiles(directory=UPLOAD_DIR),
    name="uploads"
)

# =========================
# ROOT
# =========================
@app.get("/")
def root():
    return {
        "message": "AIRAG API Running"
    }