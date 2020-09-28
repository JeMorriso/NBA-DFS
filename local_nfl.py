from local_pipeline import driver_fn
from model import Model
from localdb import LocalDB
from nfl import NFL
from localstorage import LocalStorage

if __name__ == "__main__":
    driver_fn(NFL(), LocalDB(), Model(), LocalStorage())
