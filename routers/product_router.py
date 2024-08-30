from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder

from database import Session, ENGINE
from models import Product, Order
from schemas import ProductCreateModel, ProductUpdateModel
from fastapi.exceptions import HTTPException

product_router = APIRouter(prefix="/products", tags=["Products"])
session = Session(bind=ENGINE)


@product_router.get("/")
async def get_products():
    products = session.query(Product).all()
    return products



@product_router.post("/")
async def create_product(product: ProductCreateModel):
    check_id = session.query(Product).filter(Product.id == product.id).first()
    if check_id is not None:
        return {'message': 'Product id already exists'}

    new_product = Product(
        id=product.id,
        title=product.name,
        rating=product.rating,
        price=product.price,
        color=product.color
    )

    session.add(new_product)
    session.commit()

    return HTTPException(status_code=status.HTTP_200_OK, detail='Product created')



@product_router.get("/{id}")
async def product_detail(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product is None:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Product not found')


    data = {
            "id": product.id,
            "title": product.title,
            "rating": product.rating,
            "price": product.price,
            "color": product.color
        }
    return jsonable_encoder(data)



@product_router.put("/{id}")
async def product_update(id: int, product: ProductUpdateModel):
    check_product = session.query(Product).filter(Product.id == id).first()
    if check_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(check_product, key, value)
        data = {
            "code": 200,
            "message": "Update product",
            "object": {
                "title": product.title,
                "rating": product.rating,
                "price": product.price,
                "color": product.color
            }
        }
        session.commit()
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")



@product_router.delete("/{id}")
async def product_delete(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        session.delete(product)
        session.commit()
        data = {
            "code": 200,
            "message": "Product deleted"
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="product not found")


# Birorta ham user buyurtma qilmagan productlar ro'yxatini ko'rsatuvchi API router
@product_router.get("/not_ordered")
def not_ordered_products():
    orders = session.query(Order).all()
    for order in orders:
        if order.user_id:
            products = session.query(Product).all()
            data = [
                {
                    "id": product.id,
                    "name": product.name,
                    "price": product.price
                }
                for product in products
            ]
            return jsonable_encoder(data)
