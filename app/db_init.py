from sqlalchemy import null

from app import bcrypt
from app.models import *

db.drop_all()
db.create_all()


def create_user_with_cart(username, email, password, first_name=null, second_name=null, phone=null):
    cart = Cart()
    db.session.add(cart)
    db.session.commit()

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    user = User(username=username, email=email, password=hashed_password, first_name=first_name,
                second_name=second_name, phone=phone, cart=cart)

    db.session.add(user)
    db.session.commit()


create_user_with_cart(username="user1", email="user1@email.com", password="qwerty123", first_name="Bryan",
                second_name="Cranston", phone=999)

create_user_with_cart(username="user2", email="user2@email.com", password="qwerty123", first_name="Rafal",
                second_name="Wiercioch", phone=997)

create_user_with_cart(username="user3", email="user3@email.com", password="qwerty123", first_name="Bartosz",
                second_name="Krajewski", phone=998)