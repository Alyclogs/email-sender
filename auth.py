from conn import coleccion

def validate_token(token: str):
    sessionToken = coleccion.find_one({ 'token': token })
    return sessionToken