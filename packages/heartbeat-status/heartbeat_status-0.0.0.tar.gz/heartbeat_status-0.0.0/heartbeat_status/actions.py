from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import requests

from .deta import set_deta_base_val
from .fitbit import refresh_credential
from .models import TodayHeartBeatByMin

JST = timezone(timedelta(hours=+9), "JST")


def store_heartbeat_from_fitbit() -> None:
    cred = refresh_credential()
    now = datetime.now(JST)
    yesterday = now - timedelta(days=1)
    for i in (now, yesterday) if now.hour == 0 else (now,):
        url = f"https://api.fitbit.com/1/user/-/activities/heart/date/{i.strftime('%Y-%m-%d')}/1d/1sec.json"
        heart = TodayHeartBeatByMin.model_validate(
            requests.get(
                url,
                headers={"Authorization": f"Bearer {cred.FITBIT_ACCESS_TOKEN}"},
                timeout=10,
            ).json(),
        )
        key = heart.activities_heart[0].date_time
        val = heart.activities_heart_intraday.dataset
        set_deta_base_val(key, json.dumps([d.model_dump() for d in val]))
