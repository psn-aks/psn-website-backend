import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import FastAPI


def set_up_cors(app: FastAPI):
    is_local = os.getenv("RENDER", "false").lower() != "true"

    if is_local:
        allowed_origins = [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
        ]
    else:
        allowed_origins = [
            "https://psn-aks.vercel.app",
        ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True
    )


def set_up_trusted_host(app: FastAPI):
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["psn-website-backend.onrender.com",
                       "*.onrender.com", "localhost", "127.0.0.1"]
    )
