from fastapi import FastAPI,HTTPException,Request,status
# FastAPI インスタンスを作成
from api.login import router as login_router
from api.serch import router as serch_router
from api.reranking import router as reranking_router
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
app = FastAPI()

app.include_router(login_router)
app.include_router(serch_router)
app.include_router(reranking_router)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    print(request.body)
    print(exc.body)
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )
# ルートエンドポイント
@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# 他のエンドポイント
@app.get("/items/{item_id}")
def read_item(item_id: int, query_param: str = None):
    return {"item_id": item_id, "query_param": query_param}

origins = [
  "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 実行用のコマンド
if __name__ == "__main__":
    import uvicorn
    # uvicornを使用してサーバーを起動
    # main ファイルの中で直接起動するときに使います
    uvicorn.run("main:app", host="172.0.0.1", port=4500, reload=True)
