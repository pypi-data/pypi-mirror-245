import base64


def secure_qr(encoded_str):
    encoded_str = encoded_str.split('.')
    for i in range(1, len(encoded_str)-1):
        # print(encoded_str[i])
        base64_bytes = base64.urlsafe_b64decode(encoded_str[i]+'==').decode()
        # print(base64_bytes)
    return base64_bytes
