import csv
from fake_data_generator import FakeDataGenerator
from functools import partial
import pandas as pd


def generate_data(file_path: str, numer_of_rows: int, data_structure: dict) -> None:
    """
    Generates fake data

    Args:
        file_path (str): The file path to save the generated csv
        numer_of_rows (int): The number of rows of data that should be generated
        data_structure (dict): A dcitionary with the data columns and their corresponding FakeDataGenerator types
    """
    # converting number of rows to an integer and creating empty list
    numer_of_rows = int(numer_of_rows)

    # opens file and writes first row which is the header
    with open(file_path, mode="w") as file:
        file_writer = csv.writer(file)
        file_writer.writerow(
            list(data_structure.keys())
        )  # first row should be column headers

    # opens file and streams data into file
    with open(file_path, mode="a") as file:
        file_writer = csv.writer(file)
        for _ in range(numer_of_rows):
            # for function in list of functions, call function
            function_list = [func() for func in list(data_structure.values())]
            file_writer.writerow(function_list)


def get_list_of_values(file_path: str, column: str) -> list:
    """
    Gets list of unique values in a column in a csv

    Args:
        file_path (str): The file path to save the generated csv
        column (str): The column to check for unique values

    Returns:
        list: A list of unique values in the column
    """
    # reading the csv
    df = pd.read_csv(file_path)

    # returning a list of unique values in the column
    return list(df[column].unique())


if __name__ == "__main__":
    # initializing class
    faker = FakeDataGenerator()

    # creating dictionary of
    data_structure = {
        "date": partial(faker.date, start_date="2021-01-01", end_date="2023-10-26"),
        "campaign_name": partial(
            faker.campaign_name,
            country_list=["us", "ca"],
            funnel_list=["awe", "cvr", "con"],
            promo_list=["50off", "30off", "25off", "10off"],
        ),
        "placement_name": partial(
            faker.placement_name,
            platform_list=["fb"],
            placement_format_list=["email", "video", "app", "display", "audio"],
        ),
        "ad_name": partial(
            faker.ad_name,
            message_list=["valday", "halloween", "blackfriday"],
            division_list=["sem-pla", "sem-brand", "sem-nonbrand"],
        ),
        "impressions": partial(faker.float_value, min=0, max=100000, decimal=0),
        "clicks": partial(faker.float_value, min=0, max=5000, decimal=0),
        "cost": partial(faker.float_value, min=0, max=500, decimal=2),
        "conversions_7day_click": partial(faker.float_value, min=0, max=500, decimal=0),
        "revenue_7day_click": partial(faker.float_value, min=0, max=10000, decimal=2),
        "video_views": partial(faker.float_value, min=0, max=1000, decimal=0),
        "post_reactions": partial(faker.float_value, min=0, max=1000, decimal=0),
        "engagements": partial(faker.float_value, min=0, max=1000, decimal=0),
        "comments": partial(faker.float_value, min=0, max=1000, decimal=0),
    }

    # generating the data
    generate_data(
        "./dbt/marketing_performance/seeds/raw_facebook_performance.csv",
        1_000_000,
        data_structure,
    )
