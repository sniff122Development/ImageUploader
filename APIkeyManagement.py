import secrets

def genkey(name, apikeys):
    newkey = secrets.token_hex(30)
    while newkey in apikeys:
        newkey = secrets.token_hex(30)
    apikeys[newkey] = {
        "name": name,
        "file-names": []
    }
    return {"apikeys": apikeys, "newkey": newkey}

def revokekey(key, apikeys):
    del apikeys[key]
    return apikeys