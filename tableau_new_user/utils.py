# importing libraries
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from random import sample
from settings import *
import json
import requests
import smtplib
import string
import tableauserverclient as TSC


def generate_password(password_length: int = 20):
    """
    Generates a random password based on password length desired.

    Args:
        password_length (int, optional): The desired length of the password. Defaults to 20.
    """

    # adding all the different strings and saving them into one variable
    all = string.ascii_letters + string.digits + string.punctuation

    # picking characters at random and saving to variable
    password = "".join(sample(population=all, k=password_length))

    return password


def send_email(
    from_string: str,
    to_string: str,
    bcc_string: str,
    first_name: str,
    username_string: str,
    password_url: str,
):
    """
    Sending an email with login details for a user to their email address.

    Args:
        from_string (str): The email address email will be sent from.
        to_string (str): The user's email address that email will be sent to.
        bcc_string (str): The email address that will be bcc'd when email is sent.
        first_name (str): The first name of the user.
        username_string (str): The username of the user.
        password_url (str): The pwpush url that contains password for the user.
    """

    # saving function arguements as variables
    message_string = f"""
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">Hello {first_name},</span>
    <br>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">You have been granted access to Analytics by PMG portal.</span>
    <br>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">Please change your password once you log in. You can change it by clicking your initials in the top right corner and then clicking on "My Account Settings".</span>
    <br>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">Please see below for login information:</span>
    <br>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">URL: <a href="https://analytics.pmg.com/" target="_blank">https://analytics.pmg.com/</a></span>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">Username: {username_string}</span>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">Password: <a href="{password_url}" target="_blank">{password_url}</a></span>
    <br>
    <br>
    <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">Best,</span>
    <br>
    --
    <br>

    <p style="color: rgb(34,34,34);line-height:1.38;margin-top:0pt;margin-bottom:0pt">
        <span style="font-size:9pt;font-family:Arial;background-color:transparent;font-weight:700;vertical-align:baseline;white-space:pre-wrap">{SENDERS_FULL_NAME}</span>
    </p>

    <p style="color: rgb(34,34,34);line-height:1.38;margin-top:0pt;margin-bottom:0pt">
        <span style="font-size:9pt;font-family:Arial;color:rgb(0,0,0);background-color:transparent;vertical-align:baseline;white-space:pre-wrap">{SENDERS_POSITION}</span>
    </p>

    <p style="color: rgb(34,34,34);line-height:1.38;margin-top:0pt;margin-bottom:0pt">
        <img src="https://ci5.googleusercontent.com/proxy/6j_XHdl678B6WLBwiXQY_YvWFZiMi8IfqMkkU6QcXSJnpT2SWEnLOrSjy2Q9CYaxKD6Z0x0iiz6cZnsJG59xN1PYELWnrdN4AOfGTrG2NBD3fBCmy__rbmGS_2OdUj2zrC269z5JK8uc_WeY9pI8zj-5TWayAUXlax9Xhtx1PamjBJfmkfDlS7KlF-NS9AH-a8prSF0ooUE1pSXMk_4G9OhaWvw1BOtgUvv0bMntnuSbHFaOKG45zOIb2wbgKuOcUA=s0-d-e1-ft#https://hs-7578490.f.hubspotemail.net/hub/7578490/hubfs/PMG_LogoTaglineLockup_RGB_FullColor_RLSD.png?width=450&upscale=true&name=PMG_LogoTaglineLockup_RGB_FullColor_RLSD.png" width="200" height="74" class="CToWUd" data-bit="iit">
        <br>
    </p>

    <p style="color: rgb(34,34,34);line-height:1.38;margin-top:0pt;margin-bottom:0pt">
        <span style="font-size: 9pt;font-family:Arial;color: rgb(0, 0, 0); background-color:transparent;vertical-align: baseline;white-space: pre-wrap;">{SENDERS_PHONE_NUMBER} | </span>
        <a href="www.pmg.com" style="color:rgb(17,85,204)" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://www.pmg.com/&source=gmail&ust=1668117647895000&usg=AOvVaw2K15_mZqxsYHALDL1k-AQi">
            <span style="font-size:9pt;font-family:Arial;background-color:transparent;vertical-align:baseline;white-space:pre-wrap">www.pmg.com</span>
        </a>
    </p>
    <br>
    <br>
    """  # the html string for the email. use this in any html IDE to see what the email looks like

    # creating the root message and filling in the from, to, bcc and subject headers
    msgRoot = MIMEMultipart("related")
    msgRoot["Subject"] = EMAIL_SUBJECT
    msgRoot["From"] = from_string
    msgRoot["To"] = to_string
    msgRoot["Bcc"] = bcc_string
    msgRoot.preamble = "This is a multi-part message in MIME format."

    # encapsulate the plain and HTML versions of the message body in an
    # 'alternative' part, so message agents can decide which they want to display.
    msgAlternative = MIMEMultipart("alternative")
    msgRoot.attach(msgAlternative)

    # we reference the image in the IMG SRC attribute by the ID we give it below
    msgText = MIMEText(message_string, "html")
    msgAlternative.attach(msgText)

    # creates SMTP session
    s = smtplib.SMTP("smtp.gmail.com", 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(EMAIL_LOGIN, EMAIL_PASSWORD)

    # sending the mail
    s.sendmail(from_string, to_string, msgRoot.as_string())

    # terminating the session
    return s.quit()


def get_pwpush_url(password: str, number_of_days: int = 90, number_of_views: int = 100):
    """
    Uploading password to pwpush and returning a url for sharing the password.

    Args:
        password (str): The password to be pushed using pwpush.
        number_of_days (int): The number of days the password should be available for. Defaults to 90.
        number_of_views (int): The number of views the password should be available for. Defaults to 100.
    """

    # creating a dictionary with arguements used in the post request
    payload = {
        "password[payload]": password,
        "password[expire_after_days]": number_of_days,
        "password[expire_after_views]": number_of_views,
    }

    # using post to send a request to pwpush
    r = requests.post("https://pwpush.com/p.json", data=payload)

    # loading the response form the post request into  a variable
    r_response = json.loads(r.content)["url_token"]

    # returning the final url for pwpush
    return f"https://pwpush.com/p/{r_response}"


def create_user(
    new_user: str,
    full_name: str,
    password: str,
    group_name: str = "",
    user_role: str = "Viewer",
):
    """
    Using Tableau API to make a connection to server, create a user and update the user with
    full name and password.

    Args:
        new_user (str): The users email (same as the user\'s email).
        full_name (str): The full name (first and last) of the user.
        password (str): The password to the user\'s account.
        group_name (str): The group the user belongs to. Defaults to "".
        user_role (str): The role the user should be assigned. Defaults to "Viewer".
    """

    # create an auth object
    tableau_auth = TSC.TableauAuth(
        TABLEAU_ADMIN_USERNAME, TABLEAU_ADMIN_PASSWORD, TABLEAU_SITE_NAME
    )

    # create an instance for your server
    server = TSC.Server(TABLEAU_URL, use_server_version=True)

    # opening the connection
    with server.auth.sign_in(tableau_auth):
        # create a new user_item
        user1 = TSC.UserItem(new_user, user_role)

        try:
            # add new user
            user1 = server.users.add(user1)

            # modify user info using function arguements
            user1.fullname = full_name
            user1.email = new_user

            # update user
            user1 = server.users.update(user1, password)

            # getting list of all groups
            all_groups, pagination_item = server.groups.get()

            # assigning 0 as a variable
            group_number = 0

            # for loop to go through all groups
            for i in all_groups:
                # if the group in the loop equals to the group given in the function arguement
                if all_groups[group_number].name == group_name:
                    # then add user to that group
                    server.groups.add_user(all_groups[group_number], user1.id)
                    break
                else:
                    # else just add number to variable and keep going
                    group_number += 1
                    continue

            # return true
            return True

        except TSC.ServerResponseError as e:
            # return message of the error
            return e
