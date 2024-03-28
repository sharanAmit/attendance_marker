import bcrypt
raw = input("Enter normal password")
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(bytes(raw, 'utf-8'), salt)
print(str(hashed, 'utf-8'))