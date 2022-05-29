import random
import string


def randomname(n: int):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))