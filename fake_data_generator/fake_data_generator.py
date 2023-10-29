import names
from random import randint, choice, random, uniform
import datetime


class FakeDataGenerator:
    """
    A class that genertes fake date
    """

    def __init__(self) -> None:
        """
        Initializes the FakeDateGenerator Class
        """
        self.id_number = None
        self.date_value = None

    def first_name(self) -> str:
        """
        Generates random first name

        Returns:
            str: A first name
        """
        return names.get_first_name()

    def last_name(self) -> str:
        """
        Generates random last name

        Returns:
            str: A last name
        """
        return names.get_last_name()

    def phone_number(self) -> str:
        """
        Generates random phone number

        Returns:
            str: A phone number
        """
        return f"{randint(1,9)}{randint(0,9)}{randint(0,9)}-{randint(0,9)}{randint(0,9)}{randint(0,9)}-{randint(0,9)}{randint(0,9)}{randint(0,9)}{randint(0,9)}"

    def id(self, start_number: int, step: int) -> str:
        """
        Returns an id

        Args:
            start_number (int): The number ids start from
            step (int): The step of the increase

        Returns:
            str: An id
        """
        # if there is no id_number as an attribute of the class, take the one from arguement
        # i.e. if it is the first iteration, take the  start_number as id_number
        if self.id_number is None:
            self.id_number = start_number

        current_id = self.id_number
        self.id_number += step
        return str(current_id)

    def date(self, start_date: str, end_date: str) -> datetime.date:
        """
        Returns a random date

        Args:
            start_date (str): The lower limit of the date range. eg 2023-01-01
            end_date (str): The upper limit of the date range. eg 2023-01-31

        Returns:
            datetime.date:  random date
        """
        # spliting the dates by "-" to turn it into a datetime object
        list_start_date = start_date.split("-")
        list_end_date = end_date.split("-")

        # using the split date values to create datetime objects
        start = datetime.date(
            int(list_start_date[0]), int(list_start_date[1]), int(list_start_date[2])
        )
        end = datetime.date(
            int(list_end_date[0]), int(list_end_date[1]), int(list_end_date[2])
        )

        # return random date between start and end
        # multiplying my random float gives a random date value
        self.date_value = start + (end - start) * random()
        return self.date_value

    def value_from_list(self, values: list) -> str:
        """
        Returns random value from list

        Args:
            values (list): A list of values

        Returns:
            str: A random value from list
        """
        return choice(values)

    def float_value(self, min: float, max: float, decimal: int) -> float:
        """
        Returns a random float within a range

        Args:
            min (float): The lower limit of the float range
            max (float): The upper limit of the float range
            decimal (int): The decimal place for returned number

        Returns:
            float: A random float
        """
        random_number = round(uniform(min, max), decimal)

        # if decimal is 0 return float as an integer
        if decimal == 0:
            return int(random_number)
        else:
            return random_number

    def campaign_name(
        self, country_list: list, funnel_list: list, promo_list: list
    ) -> str:
        """
        Returns a campaign name

        Args:
            country_list (list): A list of countries
            funnel_list (list): A list of funnels
            promo_list (list): A list of promos

        Returns:
            str: A campaign name
        """
        self.country_value = choice(country_list)
        self.funnel_value = choice(funnel_list)
        return f"{self.country_value}_{self.date_value.year}_{self.funnel_value}_{choice(promo_list)}"

    def placement_name(
        self,
        platform_list: list,
        placement_format_list: list,
    ) -> str:
        """
        Returns a placement name

        Args:
            platform_list (list): A list of funnels
            placement_format_list (list): A list of funnels

        Returns:
            str: A placement name
        """
        return f"{self.country_value}_{self.date_value.year}_{self.funnel_value}_{choice(platform_list)}_{choice(placement_format_list)}"

    def ad_name(self, message_list: list, division_list: list) -> str:
        """
        Returns an ad name

        Args:
            message_list (list): A list of messages
            division_list (list): A list of division

        Returns:
            str: An ad name
        """
        return f"{self.date_value.month}.{self.date_value.day}_{choice(message_list)}_{choice(division_list)}"
