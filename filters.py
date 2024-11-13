import re



def check_email(email):
    valid_email = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)
    if valid_email:
        return True
    else:
        return False




def check_num(num: str) -> bool:
    if not num[1:].isdigit() or len(num) < 9:
        return False
    else:
        return True



