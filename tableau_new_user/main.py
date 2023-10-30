# email reference: https://code.activestate.com/recipes/473810/
# updating and creating users reference: https://tableau.github.io/server-client-python/docs/api-ref#usersupdate
# pwpush reference: https://github.com/abkierstein/pwpush/blob/master/pwpush

# importing necessary libraries
import pandas as pd
from tabulate import tabulate
from settings import *
from utils import *


def main():
    # asserting to make sure each list in the dictionary are equal
    assert (
        len(TABLEAU_NEW_USERS["first_name"])
        == len(TABLEAU_NEW_USERS["last_name"])
        == len(TABLEAU_NEW_USERS["email_address"])
        == len(TABLEAU_NEW_USERS["group_name"])
    ), "The values in the TABLEAU_NEW_USERS dictionary should be of equal lengths"

    # creating a dictionary to store users and error or success messages
    error_success_dictionary = {"user_name": [], "message": []}

    for index, value in enumerate(TABLEAU_NEW_USERS["first_name"]):
        first_name = TABLEAU_NEW_USERS["first_name"][index].capitalize()
        last_name = TABLEAU_NEW_USERS["last_name"][index].capitalize()
        email_address = TABLEAU_NEW_USERS["email_address"][index].lower()
        group_name = TABLEAU_NEW_USERS["group_name"][index]
        password = generate_password(password_length=15)
        senders_email_address = EMAIL_LOGIN
        bcc_email_address = BCC_EMAIL_ADDRESS

        # saving the pwpush url as a variable
        pwpush_url = get_pwpush_url(password=password)

        # saving the create_user function response as a variable
        user_response = create_user(
            new_user=email_address,
            full_name=first_name + " " + last_name,
            password=password,
            group_name=group_name,
        )

        # if create_user function response is true
        if user_response is True:
            # append values to dictionary
            error_success_dictionary["user_name"].append(email_address)
            error_success_dictionary["message"].append(
                "User created on Tableau and email sent"
            )

            # send email to the user with login information
            send_email(
                from_string=senders_email_address,
                to_string=email_address,
                bcc_string=bcc_email_address,
                first_name=first_name,
                username_string=email_address,
                password_url=pwpush_url,
            )
        else:
            # append values to dictionary
            error_success_dictionary["user_name"].append(email_address)
            error_success_dictionary["message"].append(user_response)

    # converting dictionary to dataframe and saving as a variable
    error_success_dataframe = pd.DataFrame.from_dict(error_success_dictionary)

    # printing the dataframe to screen
    print(
        tabulate(
            error_success_dataframe,
            headers="keys",
            tablefmt="grid",
            maxcolwidths=[None, 30],
            showindex="never",
        )
    )


if __name__ == "__main__":
    main()
