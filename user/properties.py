import bcrypt

# Original dictionary of username and plain text password key value pairs
user_credentials = {
    'name1': 'password1',
    'name2': 'password2',
    'name3': 'password3'
}


def hash_password(password):
    #Usage: returns hashed version of password parameter.
    if not isinstance(password, str):
        return {"hashed_password": None, "error": "parameter must be a string"}
    
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return {"hashed_password": hashed}

def store_users_with_hashed_passwords(user_credentials):
    #Usage: returns a hashmap/dictionary with username as keys and hashed passwords as values.
    if not isinstance(user_credentials, dict):
        return {"hashed_user_credentials": None, "error": "parameter must be a dictionary"}
    
    users = {}
    for username, password in user_credentials.items():
        users[username] = hash_password(password)["hashed_password"]
    return {"hashed_user_credentials": users}


#Initializing the dictionary of username and hashed password key value pairs.
hashed_user_credentials = store_users_with_hashed_passwords(user_credentials)["hashed_user_credentials"]


def authenticate_user(username, password):
    #Usage: returns whether or not a user is authenticated.
    if not isinstance(username, str) or not isinstance(password, str):
        return {"authenticated": None, "error": "parameters must be a strings"}
    
    stored_hash = hashed_user_credentials.get(username)
    if not stored_hash or not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return {"authenticated": False}
    return {"authenticated": True}

