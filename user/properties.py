import bcrypt

# Original user credentials with plaintext passwords
user_credentials = {
    'name1': 'password1',
    'name2': 'password2',
    'name3': 'password3'
}

# Function to hash a password
def hash_password(password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed

# Function to store users with hashed passwords in a dictionary
def store_users_with_hashed_passwords(user_credentials):
    users = {}
    for username, password in user_credentials.items():
        users[username] = hash_password(password)
    return users

# Store the hashed user credentials
hashed_user_credentials = store_users_with_hashed_passwords(user_credentials)

# Function to authenticate a user
def authenticate_user(username, password):
    stored_hash = hashed_user_credentials.get(username)
    if not stored_hash or not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return False
    return True

