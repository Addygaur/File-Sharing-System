from typing import List
from fastapi import Request, HTTPException,status

from utils.authentication import validate_jwt


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, request: Request):
        token=(request.headers["authorization"]).split()[1]
        payload=validate_jwt(token)
        if payload['role'] not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Unauthorized",
                headers={"WWW-Authenticate": "Bearer"},
            )

