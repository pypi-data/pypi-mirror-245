from __future__ import annotations

from datetime import datetime, timedelta, timezone

import pandas as pd
import plotly.express as px  # type: ignore[import-untyped]

from .deta import get_deta_base_val
from .models import HeartBeatDataByMin

JST = timezone(timedelta(hours=+9), "JST")


def get_heartbeat_graph() -> str:
    l_data: list[tuple[datetime, int]] = []
    now = datetime.now(JST)
    date_keys = [(now + timedelta(hours=-i)).strftime("%Y-%m-%d") for i in range(7)]
    for date_key in date_keys:
        val = get_deta_base_val(date_key)
        if not val:
            continue
        data = HeartBeatDataByMin.model_validate_json(val).root
        l_data.extend(
            (
                datetime.fromisoformat(f"{date_key}T{dataset.time}"),
                dataset.value,
            )
            for dataset in data
        )
    data_frame = pd.DataFrame(l_data, columns=["Datetime", "BPM"]).set_index("Datetime")
    return str(px.line(data_frame=data_frame).to_html())
