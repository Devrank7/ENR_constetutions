import uvicorn
from fastapi import FastAPI

from fastapi_app.router.hook_router import router

app = FastAPI()
app.include_router(router=router, prefix="/api", tags=["api"])
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
