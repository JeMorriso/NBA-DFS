# AWS SDK
import boto3

from nflsportsreference import NFLSportsReference
from db import AuroraDB
from model import Model
from storage import S3Storage
from utils import TimeInterval
import pipeline


def pipeline_handler(event, context):
    """
    This function runs only on Lambda, delegating to pipeline functions depending on
    event keys
    """

    if "time_interval" in event and event["time_interval"] == "day":
        srwrapper = NFLSportsReference(time_interval=TimeInterval.DAY)
    else:
        srwrapper = NFLSportsReference()
    db = AuroraDB("nfl_dfs")
    # On lambda boto3 is using the role assigned to the Lambda function to get
    # permissions necessary to access s3 bucket from lambda.
    storage = S3Storage(boto3.session.Session())
    model = Model()

    start_date = event["start_date"] if "start_date" in event else None
    end_date = event["end_date"] if "end_date" in event else None

    input_path = event["input_path"] if "input_path" in event else None
    output_path = event["output_path"] if "output_path" in event else None

    if "scrape" not in event and "model" not in event:
        # default to scrape and model
        pipeline.scrape_and_model(
            srwrapper,
            db,
            model,
            storage,
            input_path,
            output_path,
            start_date,
            end_date,
        )

    elif "scrape" in event:
        pipeline.scrape(srwrapper, db, start_date=start_date, end_date=end_date)

    elif "model" in event:
        if "input_path" not in event or "output_path" not in event:
            raise ValueError(
                """
                Input path and output path must be specified in order to model.
                """
            )
        pipeline.model(srwrapper, db, model, storage, input_path, output_path)
