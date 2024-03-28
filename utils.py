from datetime import datetime, timedelta
from typing import Dict, Optional

import jwt
from jwt.exceptions import InvalidSignatureError, InvalidAlgorithmError, InvalidTokenError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from starlette import status

from setting import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_jwt_token(payload: dict, is_refreshed_token: bool):
    encoded_payload = payload.copy()

    if is_refreshed_token:
        expire = datetime.now() + timedelta(days=7)
    else:
        expire = datetime.now() + timedelta(minutes=700)

    encoded_payload.update({"exp": expire})
    encoded_jwt = jwt.encode(encoded_payload, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_jwt_token(token, options: Optional[dict] = None, ) -> dict:
    """decode jwt token"""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], options=options)
    except Exception as e:
        print(e)


def extract_token(token: str = Depends(oauth2_scheme)) -> tuple[int, int]:
    """Extract Token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload: Dict[str, int] = decode_jwt_token(token)
        if (
                isinstance(payload.get("type"), str)
                and isinstance(payload.get("sub"), int)
                and isinstance(payload.get("did"), int)
        ):
            token_type: str = str(payload.get("type"))
            device_id: int = int(payload.get("did"))
            user_id: int = int(payload.get("sub"))
            if token_type == "A":
                if device_id and user_id:
                    return device_id, user_id
        raise credentials_exception
    except InvalidSignatureError as e:
        raise credentials_exception
    except InvalidAlgorithmError as e:
        raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception


def get_refresh_token(
        token: str = Depends(oauth2_scheme),
) -> tuple[int, int]:
    """Extract Refresh Token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    invalid_token_exception = HTTPException(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: Dict[str, int] = decode_jwt_token(token)
        if (
                isinstance(payload.get("type"), str)
                and isinstance(payload.get("did"), int)
                and isinstance(payload.get("sub"), int)
        ):
            token_type: str = str(payload.get("type"))
            user_id: int = int(payload.get("sub"))
            device_id: int = int(payload.get("did"))
            if token_type == "R":
                if user_id and device_id:
                    return device_id, user_id
            raise credentials_exception
    except InvalidSignatureError as e:
        raise credentials_exception
    except InvalidAlgorithmError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception
    raise invalid_token_exception
