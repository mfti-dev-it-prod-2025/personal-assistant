import random
import string


def random_string():
    return "".join(random.choices(string.ascii_letters, k=10))


def random_email():
    return f"{random_string()}@{random_string()}.ru"
