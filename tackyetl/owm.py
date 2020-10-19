import json
import os
from datetime import datetime
from typing import Any, Dict

import pandas as pd
import requests
import tenacity

API_ = "OWM_API_KEY"


def flatten_dict(in_dict: Dict[str, Any], keystring="") -> Dict[str, Any]:
    if type(in_dict) == dict:
        keystring = keystring + "_" if keystring else keystring
        for k in in_dict:
            yield from flatten_dict(in_dict[k], keystring + str(k))
    else:
        yield keystring, in_dict


def set_api_key():
    key = input("Please enter API KEY: ")
    os.environ[API_] = key
    return key


@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=4, min=4, max=30),
    stop=tenacity.stop_after_attempt(10),
)
def retrieve(location_id: str = "Denver,CO,USA") -> str:
    api_key = os.environ.get(API_, set_api_key())
    response = requests.get(
        "http://api.openweathermap.org/data/2.5/forecast",
        params={"q": location_id, "appid": api_key},
    )
    if response.status_code == 401:
        del os.environ[API_]
        raise ValueError(f"Invalid API Key")
    return response.content


def postproc(data: str) -> pd.DataFrame:
    data = json.loads(data)
    df = pd.DataFrame()
    assert data["cod"] == "200"
    for datum in data["list"]:
        index = datum.pop("dt")
        datum = dict(flatten_dict(datum))
        # (TODO) Parse through weather
        del datum["weather"]
        df = df.append(pd.DataFrame(datum, index=[index]))
    df.index = df.index.values.astype("datetime64[s]")
    df.attrs.update(
        {
            "location": data["city"]["name"],
            "lat": data["city"]["coord"]["lat"],
            "lon": data["city"]["coord"]["lon"],
            "loc_id": data["city"]["id"],
            "min_time": df.index.min(),
            "max_time": df.index.max(),
            "avail_variables": str(list(df.columns)),
            "process_time": datetime.now(),
        }
    )
    return df
