import secrets
import string


def random_str(len: int) -> str:
    alphabet = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return "".join(secrets.choice(alphabet) for _ in range(len))


def random_handle(prefix: str = "hdl") -> str:
    return f"{prefix}-{random_str(16 - (len(prefix) + 1))}"  # Adjust length to fit the prefix


# def random_password() -> str:

#     return secrets.token_hex(8)


def random_tr_id() -> str:
    """
    Generate a random transaction ID.

    :return: A random transaction ID as a string.
    """

    return f"tr{secrets.token_hex(8)}"
