import hashlib

def hashPassword(password, algorithm):
    return hashlib.new(algorithm, bytes(password, "utf-8")).hexdigest()