from passlib.hash import pbkdf2_sha256

stored_hash = "$pbkdf2-sha256$29000$nhOCcE4p5XwPYWwtpZTyfg$QbX0ibwgVx9nrwbpxe570tuDcukzQJKfC2WczSjJRFA"
user_input = "test"  # Change this to test different passwords

if pbkdf2_sha256.verify(user_input, stored_hash):
    print("Login successful!")
else:
    print("Invalid password.")