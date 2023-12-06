import uvicorn
from fastapi import FastAPI

from api import api_router

app = FastAPI(title="SA")

app.include_router(api_router)


@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)
