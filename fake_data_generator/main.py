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
    final_list = []

    # for each iteration, create a list of generated values and append to empty list
    for _ in range(numer_of_rows):
        # for function in list of functions, call function
        function_list = [func() for func in list(data_structure.values())]
        final_list.append(function_list)

    # writing each list in list of lists as a row in csv
    with open(file_path, mode="w") as file:
        file_writer = csv.writer(file)
        file_writer.writerow(
            list(data_structure.keys())
        )  # first row should be column headers
        file_writer.writerows(final_list)


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
        "first_name": faker.first_name,
        "last_name": faker.last_name,
        "phone_number": faker.phone_number,
    }

    # generating the data
    generate_data(
        "./python/fake_data_generator/sample_file.csv",
        1000,
        data_structure,
    )
