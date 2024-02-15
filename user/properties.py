import bcrypt

# Original dictionary of username and plain text password key value pairs
user_credentials = {
    'name1': 'password1',
    'name2': 'password2',
    'name3': 'password3'
}


def hash_password(password):
    #Usage: returns hashed version of password parameter.
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

def store_users_with_hashed_passwords(user_credentials):
    #Usage: returns a hashmap/dictionary with username as keys and hashed passwords as values.
    users = {}
    for username, password in user_credentials.items():
        users[username] = hash_password(password)
    return users


#Initializing the dictionary of username and hashed password key value pairs.
hashed_user_credentials = store_users_with_hashed_passwords(user_credentials)


def authenticate_user(username, password):
    #Usage: returns whether or not a user is authenticated.
    stored_hash = hashed_user_credentials.get(username)
    if not stored_hash or not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return False
    return True

