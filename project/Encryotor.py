from cryptography.fernet import Fernet


fernet = Fernet(b'E7MsDqg0lrqXVT5o3-CENvJPBCXAdLZ8p_8cn-VuQq8=')

def encrypt(message):
    hm = fernet.encrypt(message.encode())
    return str(fernet.encrypt(message.encode()))

def decrypt(message):
    return str(fernet.decrypt(bytes(message[2:-1], 'utf-8')).decode())