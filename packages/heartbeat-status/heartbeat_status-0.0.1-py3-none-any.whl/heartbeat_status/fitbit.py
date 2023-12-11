from __future__ import annotations

import os

import requests
from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel

from .deta import get_deta_base_val, set_deta_base_val


class FitbitAPIRefreshedResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_token: str
    scope: str
    token_type: str
    user_id: str


class FitbitAPICredential(BaseModel):
    FITBIT_CLIENT_ID: str
    FITBIT_CLIENT_SECRET: str
    FITBIT_ACCESS_TOKEN: str
    FITBIT_REFRESH_TOKEN: str


def refresh_credential() -> FitbitAPICredential:
    cred = __get_fitbit_credential()
    res = requests.post(
        "https://api.fitbit.com/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "client_id": cred.FITBIT_CLIENT_ID,
            "refresh_token": cred.FITBIT_REFRESH_TOKEN,
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        timeout=10,
    )
    token = FitbitAPIRefreshedResponse.model_validate(res.json())
    access_token, refresh_token = token.access_token, token.refresh_token
    set_deta_base_val("FITBIT_ACCESS_TOKEN", access_token)
    set_deta_base_val("FITBIT_REFRESH_TOKEN", refresh_token)
    return __get_fitbit_credential()


def __get_fitbit_credential() -> FitbitAPICredential:
    def _get_val(key: str, *, is_deta_base: bool = False) -> str:
        val = get_deta_base_val(key) if is_deta_base else None
        if not is_deta_base or not val:
            val = os.environ.get(key)
        if isinstance(val, str) and len(val) > 0:
            return val

        msg = f"Failed to fetch item -- {key}"
        raise ValueError(msg)

    load_dotenv(find_dotenv(), verbose=True)
    return FitbitAPICredential(
        FITBIT_CLIENT_ID=_get_val("FITBIT_CLIENT_ID"),
        FITBIT_CLIENT_SECRET=_get_val("FITBIT_CLIENT_SECRET"),
        FITBIT_ACCESS_TOKEN=_get_val("FITBIT_ACCESS_TOKEN", is_deta_base=True),
        FITBIT_REFRESH_TOKEN=_get_val("FITBIT_REFRESH_TOKEN", is_deta_base=True),
    )
