import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from api import api_router

app = FastAPI(title="Segment Anything Model Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse('/docs')


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
