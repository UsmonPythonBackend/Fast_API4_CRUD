from fastapi import APIRouter, status
from fastapi.encoders import jsonable_encoder

from database import Session, ENGINE
from models import Order, User, Product
from schemas import OrderCreateModel, OrderUpdateModel, ProductUpdateModel
from fastapi.exceptions import HTTPException


order_router = APIRouter(prefix="/orders", tags=["Orders"])
session = Session(bind=ENGINE)


@order_router.get("/")
async def get_orders():
    orders = session.query(Order).all()
    return orders


@order_router.post("/")
async def create_order(order: OrderCreateModel):
    check_order = session.query(Order).filter(Order.id == order.id).first()
    if check_order is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order id already exists")
    check_user = session.query(User).filter(User.id == order.user_id).first()
    if check_user is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User id not exists")

    check_product = session.query(Product).filter(Product.id == order.product_id).first()
    if check_product is None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Product id not exists")

    new_order = Order(
        id=order.id,
        quantity=order.quantity,
        price=order.price,
        address=order.adress,
        user_id=order.user_id,
        product_id=order.product_id,
    )

    session.add(new_order)
    session.commit()

    return {"message": "Order created successfully", "order": {
        "id": new_order.id,
        "quantity": new_order.quantity,
        "price": new_order.price,
        "address": new_order.address,
        "order_id": new_order.id,
        "product_id": new_order.product,
    }}



@order_router.get("/{id}")
async def order_detail(id: int):
    orders = session.query(Order).filter(Order.id == id).first()
    if orders is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

    data = {
        "id": orders.id,
        "quantity": orders.quantity,
        "price": orders.price,
        "address": orders.address,
        "order_id": orders.id,
        "user_id": orders.user_id,
        "product_id": orders.product_id,

    }



    return jsonable_encoder(data)




# Userga tegishli buyurtmalar ro'yxatini ko'rsatuvchi API router
@order_router.get("/user/{id}")
async def get_user(id: int):
    user = session.query(User).filter(User.id == id).first()
    if user:
        orders = session.query(Order).filter(Order.id == id).all()
        order_data = [
            {
                "id": orders.id,
                "quantity": orders.quantity,
                "price": orders.price,
                "address": orders.address,
                "order_id": orders.id,
                "user_id": orders.user_id,
                "product_id": orders.product_id,
            }
            for order in orders
        ]

        data = {
            "username": user.username,
            "email": user.email,
            "orders": order_data
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")



# Bitta productni qaysi userlar buyurtma qilganini aniqlovchi api router
@order_router.get("/product/{id}")
async def get_product(id: int):
    product = session.query(Product).filter(Product.id == id).first()
    if product:
        orders = session.query(Order).filter(Order.id == id).all()
        order_data = [
            {
                "id": orders.id,
                "quantity": orders.quantity,
                "price": orders.price,
                "address": orders.address,
                "order_id": orders.id,
                "user_id": orders.user_id,
                "product_id": orders.product_id,
            }
            for order in orders
        ]

        data = {
            "product": product.id,
            "product_name": product.name,
            "product_price": product.price,
            "orders": order_data
        }

        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")


@order_router.put("/{id}")
async def order_update(id: int, order: OrderUpdateModel):
    check_order = session.query(Order).filter(Order.id == id).first()
    if check_order:
        for key, value in order.dict().items():
            setattr(check_order, key, value)

        data = {
            "code": 200,
            "message": "Order updated successfully",
            "object": {
                "product": order.product_id,
                "quantity": order.quantity,
                "user_id": order.user_id
            }
        }
        session.commit()
        return jsonable_encoder(data)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")



@order_router.delete("/{id}")
async def order_delete(id: int):
    order = session.query(Order).filter(Order.id == id).first()
    if order:
        session.delete(order)
        session.commit()

        data = {
            "code": 200,
            "message": "Order deleted successfully"
        }
        return jsonable_encoder(data)

    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")