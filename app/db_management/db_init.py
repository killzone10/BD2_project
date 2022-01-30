from db_manage import *

db.drop_all()
db.create_all()

# users
insert_city("Warszawa")
insert_city("Lublin")
insert_city("Radom")

insert_user(username="user1", email="user1@email.com", password="qwerty123", first_name="Bryan",
            second_name="Cranston", phone=999)

insert_user(username="user2", email="user2@email.com", password="qwerty123", first_name="Rafal",
            second_name="Wiercioch", phone=997)

insert_user(username="user3", email="user3@email.com", password="qwerty123", first_name="Bartosz",
            second_name="Krajewski", phone=998)

insert_user_with_all_attributes(username="user4", email="user4@email.com", password="qwerty123", first_name="Tom",
                                second_name="Cruise", phone=1234111, city_name="Puławy", street="Bazodanowa",
                                house_nr=2, postal_code="01-234")

# product types
haczyki = insert_product_type("Haczyki")
przynety = insert_product_type("Przynęty")
wedki = insert_product_type("Wędki")

# brands
fishrodex = insert_brand("FishRodex")
fishing_rodeo = insert_brand("Fishing RODeo")
captain_hook = insert_brand("Captain Hook")
hookup = insert_brand("Hookup")
hook_cook = insert_brand("Hook Cook")
rybia_zacheta = insert_brand("Rybia zachęta")
rybie_przysmaki = insert_brand("Rybie Przysmaki")

# products
insert_product("Super Haczyk", 12.34, 100, "Świetny Haczyk do łowienia", type_id=haczyki.id, brand_id=captain_hook.id)
insert_product("Haczyk 300X", 20.00, 10, "Haczyk 300X to coś, co musisz mieć!", type_id=haczyki.id,
               brand_id=hook_cook.id)
insert_product("Hook 200L", 14.00, 20, "Najlepszy haczyk, jaki istnieje.", type_id=haczyki.id, brand_id=hookup.id)

insert_product("HotRod Pro", 153.99, 15, "Najgorętsza wędka na rynku.", type_id=wedki.id, brand_id=fishing_rodeo.id)
insert_product("Wedka X3200", 253.99, 15, "Jak wędka wygląda, każdy widzi.", type_id=wedki.id,
               brand_id=fishing_rodeo.id)
insert_product("Rod Pro", 153.99, 15, "Wędka tylko dla profesjonalistów.", type_id=wedki.id, brand_id=fishrodex.id)

insert_product("Robak Typu S", 1.00, 100, "Robak mały. Dla ryb małych. Cena za kg.", type_id=przynety.id,
               brand_id=rybia_zacheta.id)
insert_product("Robaczanka", 2.30, 100, "Może i drogie, ale za to skuteczne. Cena za kg.", type_id=przynety.id,
               brand_id=rybie_przysmaki.id)
