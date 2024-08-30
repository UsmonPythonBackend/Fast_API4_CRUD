from fastapi import FastAPI
from routers.user_router import user_router
from routers.cargo_router import cargo_router
from routers.order_router import order_router
from routers.product_router import product_router


app = FastAPI()
app.include_router(user_router)
app.include_router(cargo_router)
app.include_router(order_router)
app.include_router(product_router)



@app.get("/")
async def root():
    return {"message": "Home page"}










