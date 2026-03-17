import re

gmail_regex = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", re.IGNORECASE)
phone_regex = re.compile(r"^(?:\+998|998)?(90|91|93|94|95|97|98|99)\d{7}$")

def check_gmail_or_phone(data):
    # Ensure the data is a string
    if not isinstance(data, str):
        raise TypeError(f"Expected a string or bytes-like object, got {type(data).__name__}")

    sanitized_data = re.sub(r"\s+|-", "", data)

    if re.match(gmail_regex, data):
        return "gmail"
    
    elif re.match(phone_regex, sanitized_data):
        return "phone"
    else:
        data = {
            "success": False,
            "message": "Gmail or Phone is not True"
        }
        raise ValueError(data)
    

def check_phone(data):
    sanitized_data = re.sub(r"\s+|-", "", data)
    if re.match(phone_regex, sanitized_data):
        return True
    else:
        raise False
