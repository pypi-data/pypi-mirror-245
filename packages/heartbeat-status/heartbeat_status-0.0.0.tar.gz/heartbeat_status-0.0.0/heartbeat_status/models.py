from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, RootModel


# activities_heart
class _Value__HeartRateZone(BaseModel):  # noqa: N801
    calories_out: float = Field(alias="caloriesOut")
    rate_max: int = Field(alias="max")
    rate_min: int = Field(alias="min")
    minutes: int
    name: str


class _ActivitiesHeart__Value(BaseModel):  # noqa: N801
    custom_heart_rate_zones: list[Any] = Field(alias="customHeartRateZones")  # unconfirmed
    heart_rate_zones: list[_Value__HeartRateZone] = Field(alias="heartRateZones")
    resting_heart_rate: int = Field(alias="restingHeartRate")


class _TodayHeartBeatByMin__ActivitiesHeart(BaseModel):  # noqa: N801
    date_time: str = Field(alias="dateTime")
    value: _ActivitiesHeart__Value


# activities_heart_intraday
class _ActivitiesHeartIntraday__Dataset(BaseModel):  # noqa: N801
    time: str
    value: int


_ActivitiesHeartIntraday__Datasets = list[_ActivitiesHeartIntraday__Dataset]


class _TodayHeartBeatByMin__ActivitiesHeartIntraday(BaseModel):  # noqa: N801
    dataset: _ActivitiesHeartIntraday__Datasets
    dataset_interval: int = Field(alias="datasetInterval")
    dataset_type: str = Field(alias="datasetType")


# root
class TodayHeartBeatByMin(BaseModel):
    activities_heart: list[_TodayHeartBeatByMin__ActivitiesHeart] = Field(alias="activities-heart")
    activities_heart_intraday: _TodayHeartBeatByMin__ActivitiesHeartIntraday = Field(alias="activities-heart-intraday")


HeartBeatDataByMin = RootModel[_ActivitiesHeartIntraday__Datasets]
