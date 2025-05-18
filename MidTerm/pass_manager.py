import os
import json
import getpass
import secrets
import string
from cryptography.fernet import Fernet

Key_file = "key.key"
Password_file = "passwords.txt"

def load_key():
    if not os.path.exists(Key_file):
        key = Fernet.generate_key()
        with open(Key_file, "wb") as kf:
            kf.write(key)
    else:
        with open(Key_file, "rb") as kf:
            key = kf.read()
    return key

key = load_key()
fernet = Fernet(key)

def load_passwords():
    try:
        with open(Password_file, "r") as file:
            encrypted_data = json.load(file)
            for entry in encrypted_data.values():
                encrypted_pw = entry["password"].encode()
                decrypted_pw = fernet.decrypt(encrypted_pw).decode()
                entry["password"] = decrypted_pw
            return encrypted_data
    except FileNotFoundError:
        return {}

def save_passwords(passwords):
    data_to_store = {}
    for name, creds in passwords.items():
        encrypted_pw = fernet.encrypt(creds["password"].encode()).decode()
        data_to_store[name] = {
            "username": creds["username"],
            "password": encrypted_pw
        }
    with open(Password_file, "w") as file:
        json.dump(data_to_store, file)
        
def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for x in range(length))

passwords = load_passwords()

Master_username = "admin"
Master_password = "1234"

print("Welcome to the Password Manager!")
username = input("Enter master username: ")
password = getpass.getpass("Enter master password: ")

if username != Master_username or password != Master_password:
    print("Access denied.")
    exit()


while True:
    print("What do you want to do?")
    print("1. Find password")
    print("2. Add password")
    print("3. Change password")
    print("4. Exit")
    choice = input("Choose (1-4): ")

    if choice == "1":
        name = input("Enter the site or app name: ")
        if name in passwords:
            print("Username:", passwords[name]["username"])
            print("Password:", passwords[name]["password"])
        else:
            print("No password found for that name.")

    elif choice == "2":
        name = input("Enter the site or app name: ")
        if name in passwords:
            print("That name already exists.")
        else:
            username = input("Enter the username: ")
            pass_gen = input("Do you want to generate a secure password? (y/n): ")
            if pass_gen.lower() == 'y':
                password = generate_password()
                print("Generated password:", password)
            else:
                password = getpass.getpass("Enter your password: ")
            passwords[name] = {"username": username, "password": password}
            save_passwords(passwords)
            print("Password added.")

    elif choice == "3":
        name = input("Enter the site or app name: ")
        if name in passwords:
            use_generated = input("Do you want to generate a secure password? (y/n): ")
            if use_generated.lower() == 'y':
                password = generate_password()
                print("Generated password:", password)
            else:
                password = getpass.getpass("Enter the new password: ")
            passwords[name]["password"] = password
            save_passwords(passwords)
            print("Password changed.")
        else:
            print("No password found for that name.")

    elif choice == "4":
        print("Goodbye!")
        break

    else:
        print("Invalid choice.")
