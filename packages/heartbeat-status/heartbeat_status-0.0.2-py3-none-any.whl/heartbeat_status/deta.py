from __future__ import annotations

from deta import Deta  # type: ignore[import-untyped]
from pydantic import BaseModel

__DETA_BASE_CREDENTIAL_DB_KEY = "fitbit_credential_db"


class DetaBaseItem(BaseModel):
    key: str
    value: str


def get_deta_base_val(key: str) -> str | None:
    res = Deta().Base(__DETA_BASE_CREDENTIAL_DB_KEY).get(key)
    if not res:
        return None
    item = DetaBaseItem.model_validate(res)
    if isinstance(item.value, str) and len(item.value) > 0:
        return item.value
    return None


def set_deta_base_val(key: str, val: str) -> None:
    item = DetaBaseItem.model_validate(
        Deta().Base(__DETA_BASE_CREDENTIAL_DB_KEY).put({"value": val}, key),
    )
    if item.key == key and item.value == val:
        return

    msg = f"sent <{key}: {val}> to Deta Base, but got <{item.key}: {item.value}>"
    raise ValueError(msg)
