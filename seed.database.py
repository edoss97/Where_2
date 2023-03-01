import os
import json
from random import choice, randint

import crud
import model
import server
with server.app.app_context():
    os.system("dropdb lists")
    os.system("createdb lists")

    model.connect_to_db(server.app)
    model.db.create_all()

    with open('data/destinations.json') as f:
        destination_data = json.loads(f.read())

    destinations_in_db = []
    for destination in destination_data:
        destination_name,destination_url,destination_description = (
            destination["destination_name"],
            destination["destination_url"],
            destination["destination_description"]
        )
        db_destination = crud.create_dest(destination_name,destination_url,destination_description)
        destinations_in_db.append(db_destination)

    model.db.session.add_all(destinations_in_db)
    model.db.session.commit()
# with server.app.app_context():
    for n in range(10):
        username = f"user{n}"  
        password = "test"

        user = crud.create_user(username, password)
        model.db.session.add(user)
        model.db.session.commit()
        for _ in range(100):
            random_dest = choice(destinations_in_db)
            new_random_dest = random_dest.destination_id
            score = randint(3, 5)
            rating = crud.create_rating(user.user_id, new_random_dest, score)
            model.db.session.add(rating)
            model.db.session.commit()
        for n in range(10):
            list_name = f"list{n}"
            list = crud.create_list(user.user_id,list_name )
            model.db.session.add(list)
            model.db.session.commit()