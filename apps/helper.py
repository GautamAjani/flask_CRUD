import jwt
from datetime import datetime
KEY = "gasdfdhdgjhdghhsj"

def generate_token(user_id):
    """It is user for genrating token."""

    payload = {
        'id': str(user_id),
        'iat':datetime.utcnow()
    }
    jwt_token = {'token': jwt.encode(payload, KEY)}
    token = jwt_token['token'].decode('utf-8')
    return token

# def decode_token(token):
#     """It is used for token decoding."""
#     try:
#         jwt_token_decode = {'token':jwt.decode(token, KEY)}
#         user_id = jwt_token_decode['token']['id']
#         return user_id
#     except jwt.exceptions.ExpiredSignatureError:
#         message = responses['EXPIRE_TOKEN']
#         code = response_codes['BAD_REQUEST']
#     except:
#         message = responses['INVALID_TOKEN']
#         code = response_codes['BAD_REQUEST']
#     return jsonify({'message': message}), code