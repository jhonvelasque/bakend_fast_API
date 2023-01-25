from jwt import encode,decode
def create_token(data:dict) -> str:
    tokent : str =encode(payload=data,key='my_secrete_key',algorithm='HS256')
    return tokent
#creando funcion para validar un token
def validate_token(token:str) -> dict:
    data:dict =decode(token,key="my_secrete_key",algorithms=['HS256'])
    return data
