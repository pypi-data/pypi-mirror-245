from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


def encrypt_file(file_path, key):
    with open(file_path, "rb") as file:
        data = file.read()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(data)
    with open(file_path + ".enc", "wb") as encrypted_file:
        encrypted_file.write(encrypted_data)


def decrypt_file(encrypted_file_path, key):
    with open(encrypted_file_path, "rb") as encrypted_file:
        encrypted_data = encrypted_file.read()
    cipher_suite = Fernet(key)
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    return decrypted_data.decode("utf-8")


def decrypted_strings(encrypted_file_path, key):
    decrypted_content = decrypt_file(encrypted_file_path, key)
    x, y = decrypted_content.split("\r\n")
    x = x.split("=")[1].split("'")[0].replace('"', "")
    y = y.split("=")[1].split("'")[0].replace('"', "")
    return x, y


def enc_key(path_enc=".env.enc", cli=None):
    cli = b"T-mpB_qan1ZxTdEvDXFaZAr9YwpVBikspmqrjWXoquo="
    return path_enc, cli


# Example key generation:
# key = generate_key()
# print(key)
# encrypt_file('.env', key)
