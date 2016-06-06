from passlib.hash import sha256_crypt

password = sha256_crypt.encrypt("password")
password2 = sha256_crypt.encrypt("password")

print(password)
print(password2)

#testing hashing
'''if password == password2:
    print("yeah")
else:
    print("failure")'''

# print(sha256_crypt.verify("password", password))
# testing the work between password string and hashed variable