import boxsdk
import webbrowser
import os
import getpass

MAX_INPUT_LENGTH = 50  # limit length of input

not_found_emails = []


def valid_pathfile(file_path):
    return os.path.exists(file_path)


auth = boxsdk.OAuth2(
    client_id=input("Enter Client ID: "),
    client_secret=getpass.getpass("Enter Client Secret: ")
)

# Working loop
authenticated = False
while not authenticated:
    stderr = os.dup(2)
    os.close(2)
    os.open(os.devnull, os.O_RDWR)

    auth_url, csrf_token = auth.get_authorization_url('https://app.box.com/') #need to add your Box URL for the app

    webbrowser.open(auth_url)

    os.dup2(stderr, 2)
    os.close(stderr)

    while True:
        auth_code = getpass.getpass("Enter your authorization code: ")
        if len(auth_code) <= MAX_INPUT_LENGTH:
            break
        print("Input too long. Please try again.")

    try:
        access_token, refresh_token = auth.authenticate(auth_code)
        authenticated = True
    except boxsdk.exception.BoxOAuthException as error:
        if error.message == "The authorization code has expired" or error.message == "Auth code doesn't exist or is invalid for the client":
            print("Authorization code has expired or is invalid.")

client = boxsdk.Client(auth)

# Enter new policy name to create legal hold.
while True:
    while True:
        new_policy_name = input(
            "Enter the case name to create a new legal hold policy: ".format(MAX_INPUT_LENGTH))
        if len(new_policy_name) <= MAX_INPUT_LENGTH:
            break
        print("Input too long. Please try again.")

    new_policy = client.create_legal_hold_policy(
        new_policy_name, is_ongoing=True)
    print(f'Created legal hold policy with ID {new_policy.id}')

    # Get user input for path and create a list of emails
    while True:
        file_path = input("Enter a file path without quotation marks: ")
        if valid_pathfile(file_path):
            emails = open(file_path).readlines()
            break
        else:
            print('Invalid file path')

    # loop to iterate through email list
    if all(email.endswith("\n") for email in emails):
        # Example 2: emails are separated by space and ended with \n
        # Convert to example 1 format
        new_emails = []
        for email in emails:
            new_emails.extend(email.split())
        emails = new_emails
        # Now run through example 1 processing
        not_found_emails = []
        for email in emails:
            email = email.strip()
            users = client.users(filter_term=email)
            found = False
            for user in users:
                if user.login == email:
                    found = True
                    print(user.id, user.name)
                    user_to_assign = client.user(user_id=user.id)
                    assignment = client.legal_hold_policy(
                        new_policy.id).assign(user_to_assign)
                    print(
                        f'Applied policy "{assignment.legal_hold_policy.policy_name}" to {assignment.assigned_to.type} {assignment.assigned_to.id}')
            if not found:
                not_found_emails.append(email)
        if not_found_emails:
            print("The following emails were not found in Box:",
                  ', '.join(not_found_emails))
    else:
        not_found_emails = []
        for email in emails:
            email = email.strip()
            users = client.users(filter_term=email)
            found = False
            for user in users:
                if user.login == email:
                    found = True
                    print(user.id, user.name)
                    user_to_assign = client.user(user_id=user.id)
                    assignment = client.legal_hold_policy(
                        new_policy.id).assign(user_to_assign)
                    print(
                        f'Applied policy "{assignment.legal_hold_policy.policy_name}" to {assignment.assigned_to.type} {assignment.assigned_to.id}')
            if not found:
                not_found_emails.append(email)
        if not_found_emails:
            print("The following emails were not found in Box:",
                  ', '.join(not_found_emails))

    while True:
        create_another_policy = input(
            'Do you need to create another policy? (y/n): ')
        if create_another_policy == 'n':
            break
        elif create_another_policy != 'y':
            print('Invalid input. Please try again.')
        else:
            break
    if create_another_policy == 'n':
        break

# Revoke authentication
try:
    auth.revoke()
except boxsdk.exception.BoxOAuthException as e:
    if e.status == 200:
        print("Session has been terminated and your session revoked.")
    else:
        raise

while True:
    user_input = input("Enter 'q' to quit: ")
    if user_input == 'q':
        break
    else:
        print("Invalid input. Please try again.")
