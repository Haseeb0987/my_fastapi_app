import random
import string

def generate_user_id():
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    numbers = ''.join(random.choices(string.digits, k=3))
    return f"{letters}{numbers}"
