import random
import string

random_string = lambda: "".join(
    random.choices(string.ascii_letters + string.digits, k=10)
)
random_email = lambda: f"{random_string()}@{random_string()}.ru"
