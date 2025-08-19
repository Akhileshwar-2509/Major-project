from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import predict, recommend, classify, optimize, explain
from .routers import export as export_router
from .db import Base, engine
from .seed import run_seed

app = FastAPI(title="Allelopathy Advisor", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, prefix="/predict", tags=["predict"])
app.include_router(recommend.router, prefix="/recommend", tags=["recommend"])
app.include_router(classify.router, prefix="/classify", tags=["classify"])
app.include_router(optimize.router, prefix="/optimize", tags=["optimize"])
app.include_router(explain.router, prefix="/explain", tags=["explain"])
app.include_router(export_router.router, prefix="/export", tags=["export"])

@app.get("/")
def root():
    return {"status": "ok", "service": "allelopathy-advisor"}


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    run_seed(str((__file__.rsplit("/app/", 1)[0]) + "/data"))

