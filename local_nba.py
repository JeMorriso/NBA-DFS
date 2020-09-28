from local_pipeline import driver_fn
from model import Model
from localdb import LocalDB
from nba import NBA
from localstorage import LocalStorage

if __name__ == "__main__":
    driver_fn(NBA(), LocalDB(), Model(), LocalStorage())
