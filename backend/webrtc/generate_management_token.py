import jwt
import uuid
from datetime import datetime, timedelta


def generateManagementToken(app_access_key, app_secret):
    expires = 25 * 3600
    now = datetime.utcnow()
    exp = now + timedelta(seconds=expires)
    return jwt.encode(payload={
        'access_key': app_access_key,
        'type': 'management',
        'version': 2,
        'jti': str(uuid.uuid4()),
        'iat': now,
        'exp': exp,
        'nbf': now
        }, key=app_secret)