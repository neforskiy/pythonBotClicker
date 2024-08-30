import base64
from db import *

def Delete1stAndLastAndPreLastSymbolFromDBsQuery(string):
    string = str(string)
    str_new = string[:-1]
    str_middle = str_new[:-1]
    str_end = str_middle[1:]
    string = str(str_end)
    return string

def extract_unique_code(text):
    # Extracts the unique_code from the sent /start command.
    return text.split()[1] if len(text.split()) > 1 else None

def decode_base64(base64_string):
    try:
        # Add padding if necessary
        padding = len(base64_string) % 4
        if padding != 0:
            base64_string += '=' * (4 - padding)

        # Decode the Base64 string
        decoded_bytes = base64.b64decode(base64_string)
        # Convert the decoded bytes to a string
        decoded_string = decoded_bytes.decode('utf-8')
        return decoded_string
    except Exception as e:
        print(f"Error decoding Base64: {str(e)}")
        return None
class Database:
    def user_exists(user_id):
        Query = f"""
SELECT * from `users` 
WHERE `users`.`user_id` = {user_id}
"""
        result = db_connect(Query)
        if result == None:
            return False
        else:
            return True
    
    def add_user(user_id, referrer_id=None):
        if referrer_id != None:
            Query1 = f"""
INSERT INTO `users` (`user_id`, `referrer_id`)
VALUES
({user_id}, {referrer_id})
"""
            return db_connect(Query1)
        else:
            Query2 = f"""
INSERT INTO `users` (`user_id`)
VALUES
({user_id})
"""
            return db_connect(Query2)
        
    def count_referals(user_id):
        Query = f"""
SELECT COUNT(`id`) as count FROM `users` WHERE `referrer_id` = {user_id}
"""
        return db_connect(Query)