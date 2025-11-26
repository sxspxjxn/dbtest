import hashlib
def hashed(text : str):
    return hashlib.sha256(text.encode()).hexdigest()




    