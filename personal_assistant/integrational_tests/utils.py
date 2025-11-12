import random
import string

random_string = lambda :''.join(random.choices(string.ascii_letters + string.digits, k=10))