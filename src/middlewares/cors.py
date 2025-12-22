from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI


origins = [
    "https://psn-aks.vercel.app",
    "https://1m2h6kgl-3000.uks1.devtunnels.ms",
    "http://localhost:3000",  # if testing locally
]


def set_up_cors(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        expose_headers=["Set-Cookie"]
    )
