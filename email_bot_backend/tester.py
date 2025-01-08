import pprint

from email_functions import signed_in_user

response = signed_in_user(None)
pprint.pp(response)