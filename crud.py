from model import db, User, Destination, Rating, List, List_Dest, connect_to_db

def create_user(username,password):
    user= User(username=username, password=password)
    return user

def create_dest(destination_name,destination_url,destination_description):
    destination = Destination(destination_name=destination_name, destination_url=destination_url, destination_description=destination_description)
    return destination

def create_rating(user_id,destination_id,rating):
    rating = Rating(user_id=user_id,destination_id=destination_id,rating=rating)
    return rating

def create_list_dest(user_id, destination_id, list_id):
    new_list_dest=List_Dest(user_id=user_id,destination_id=destination_id, list_id=list_id)
    return new_list_dest

def create_list(user_id,list_name):
    list = List(user_id= user_id, list_name=list_name)
    return list

def get_dest_by_id(destination_id):
     return Destination.query.get(destination_id)

def get_all_dest_by_id(list):
    return Destination.query.filter_by(list=list).all()

def get_list_by_id(list_id):
    return List.query.get(list_id)

def get_list_id_by_name(list_name):
    return List.query.filter_by(list_name = list_name).first()

def get_dest_id_by_list_id(list_id):
    return List_Dest.query.filter_by(list_id=list_id).all()

def create_list_dest(list_id,destination_id,user_id):
    list_dest=List_Dest(list_id=list_id, destination_id=destination_id, user_id=user_id)
    return list_dest

def get_user_by_user_id(user_id):

    return User.query.filter_by(user_id = user_id).first()

def get_user_by_username(username):

    return User.query.filter_by(username = username).first()

def get_destinations():

    return Destination.query.all()

def get_list_by_user_id(user_id):
    
    return List.query.filter_by(user_id = user_id).all()

def get_avg_rating(destination_id):
    return Rating.query.filter_by(destination_id=destination_id).all()

def update_list(list_id, new_list_name):
    list=List.query.get(list_id)
    list.name = new_list_name

# def delete_dest(user_id, destination_id):
#     destination=List_Dest.query.filter_by(user_id=user_id, destination_id=destination_id).first()
#     return destination

if __name__ == '__main__':
    from server import app
    connect_to_db(app)

