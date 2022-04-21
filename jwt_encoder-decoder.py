#pip install pyjwt

import jwt
key = "secretnyanih"
encoded = jwt.encode({"a": 1, "b": 4}, key, algorithm="HS256")
print(encoded)
#eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhIjoxLCJiIjo0fQ.jPdaQ0bMOE3xaMZwrsZVpfscQBOK1IP3CN_ENxS42Nk
decoded = jwt.decode(encoded, key, algorithms="HS256")
print(decoded)
# {"a": 1, "b": 4}