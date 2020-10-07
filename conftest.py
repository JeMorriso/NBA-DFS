import pytest
import boto3

import local_pipeline
from model import Model
from db import LocalDB, AuroraDB
from nflsportsreference import NFLSportsReference
from storage import LocalStorage, S3Storage
from utils import TimeInterval, Utils


@pytest.fixture
def utils():
    return Utils()


@pytest.fixture
def nfl_default():
    return NFLSportsReference()


@pytest.fixture
def nfl(request):
    if request.param == "day":
        return NFLSportsReference(time_interval=TimeInterval.DAY)
    else:
        return NFLSportsReference()


@pytest.fixture
def nfl_day():
    return NFLSportsReference(time_interval=TimeInterval.DAY)


@pytest.fixture
def localdb_nfl():
    return LocalDB("nfl_dfs")


@pytest.fixture
def model():
    return Model()


@pytest.fixture
def localstorage():
    return LocalStorage()


@pytest.fixture
def db(request):
    if request.param == "local":
        return LocalDB("nfl_dfs")
    else:
        return AuroraDB("nfl_dfs")


@pytest.fixture
def storage(req):
    if req.param == "local":
        return LocalStorage()
    else:
        return S3Storage(session=boto3.session.Session(profile_name="default"))
