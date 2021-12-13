import random, string


def generate_process_code():
    x = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
    return x

def generate_mail(user_name="user"):

    process_code = generate_process_code()
    SUBJECT = "[ALERT] DeepCon upload process code."
    TEXT = f"Hello {user_name}, We're glad that you've chosen DeepCon. Here is your process code: {process_code}"

    return SUBJECT, TEXT

if __name__ == "__main__":
    print(generate_mail("nidbhavsar989@gmail.com", "nidbhavsar4959@gmail.com"))

    

