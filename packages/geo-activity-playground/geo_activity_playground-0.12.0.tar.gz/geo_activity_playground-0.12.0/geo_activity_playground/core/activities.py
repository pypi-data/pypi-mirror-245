import dataclasses
import datetime
import functools
import logging
from typing import Iterator
from typing import Optional

import geojson
import matplotlib
import pandas as pd

from geo_activity_playground.core.config import get_config


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class ActivityMeta:
    calories: float
    commute: bool
    distance: float
    elapsed_time: datetime.timedelta
    equipment: str
    id: int
    kind: str
    name: str
    start: datetime.datetime

    def __str__(self) -> str:
        return f"{self.name} ({self.kind}; {self.distance:.1f} km; {self.elapsed_time})"


class ActivityRepository:
    def __init__(self) -> None:
        self.meta = pd.read_parquet("Cache/activities.parquet")
        self.meta.index = self.meta["id"]
        self.meta.index.name = "index"
        self.meta["distance"] /= 1000
        self.meta["kind"].fillna("Unknown", inplace=True)
        self.meta["equipment"].fillna("Unknown", inplace=True)

    def iter_activities(self, new_to_old=True) -> Iterator[ActivityMeta]:
        direction = -1 if new_to_old else 1
        for id, row in self.meta[::direction].iterrows():
            yield ActivityMeta(**row)

    @functools.lru_cache()
    def get_activity_by_id(self, id: int) -> ActivityMeta:
        return ActivityMeta(**self.meta.loc[id])

    def get_time_series(self, id: int) -> pd.DataFrame:
        df = pd.read_parquet(f"Cache/Activity Timeseries/{id}.parquet")
        df.name = id
        if pd.api.types.is_dtype_equal(df["time"].dtype, "int64"):
            start = self.get_activity_by_id(id).start
            time = df["time"]
            del df["time"]
            df["time"] = [start + datetime.timedelta(seconds=t) for t in time]
        assert pd.api.types.is_dtype_equal(df["time"].dtype, "datetime64[ns, UTC]")

        if "distance" in df.columns:
            df["distance/km"] = df["distance"] / 1000

            if "speed" not in df.columns:
                df["speed"] = (
                    df["distance"].diff()
                    / (df["time"].diff().dt.total_seconds() + 1e-3)
                    * 3.6
                )

        return df


def make_geojson_from_time_series(time_series: pd.DataFrame) -> str:
    line = geojson.LineString(
        [
            (lon, lat)
            for lat, lon in zip(time_series["latitude"], time_series["longitude"])
        ]
    )
    return geojson.dumps(line)


def make_geojson_color_line(time_series: pd.DataFrame) -> str:
    cmap = matplotlib.colormaps["viridis"]
    return geojson.dumps(
        geojson.FeatureCollection(
            features=[
                geojson.Feature(
                    geometry=geojson.LineString(
                        coordinates=[
                            [row["longitude"], row["latitude"]],
                            [next["longitude"], next["latitude"]],
                        ]
                    ),
                    properties={
                        "speed": next["speed"],
                        "color": matplotlib.colors.to_hex(
                            cmap(min(next["speed"] / 35, 1.0))
                        ),
                    },
                )
                for (_, row), (_, next) in zip(
                    time_series.iterrows(), time_series.iloc[1:].iterrows()
                )
            ]
        )
    )


def extract_heart_rate_zones(time_series: pd.DataFrame) -> Optional[pd.DataFrame]:
    if "heartrate" not in time_series:
        return None
    config = get_config()
    try:
        heart_config = config["heart"]
    except KeyError:
        logger.warning(
            "Missing config entry `heart`, cannot determine heart rate zones."
        )
        return None

    birthyear = heart_config.get("birthyear", None)
    maximum = heart_config.get("maximum", None)
    resting = heart_config.get("resting", None)

    if not maximum and birthyear:
        age = time_series["time"].iloc[0].year - birthyear
        maximum = 220 - age
    if not resting:
        resting = 0
    if not maximum:
        logger.warning(
            "Missing config entry `heart.maximum` or `heart.birthyear`, cannot determine heart rate zones."
        )
        return None

    zones: pd.Series = (time_series["heartrate"] - resting) * 10 // (
        maximum - resting
    ) - 4
    zones.loc[zones < 0] = 0
    zones.loc[zones > 5] = 5
    df = pd.DataFrame({"heartzone": zones, "step": time_series["time"].diff()}).dropna()
    duration_per_zone = df.groupby("heartzone").sum()["step"].dt.total_seconds() / 60
    duration_per_zone.name = "minutes"
    for i in range(6):
        if i not in duration_per_zone:
            duration_per_zone.loc[i] = 0.0
    result = duration_per_zone.reset_index()
    return result
