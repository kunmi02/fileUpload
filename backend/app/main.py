from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import auth, upload, files
from .db.sqlite import init_db

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(files.router)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    init_db()

# Optional: Lambda handler for AWS Lambda deployment
def handler(event, context):
    # This could be implemented if you want to deploy to AWS Lambda
    pass
