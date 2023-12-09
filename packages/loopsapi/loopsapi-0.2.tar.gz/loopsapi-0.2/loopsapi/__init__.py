from loopsapi.apikey import ApiKey
from loopsapi.custom_fields import CustomFields
from loopsapi.transactional_emails import TransactionalEmails
from loopsapi.events import Events
from loopsapi.contacts import Contacts


class Loops:

    def __init__(self, api_key):
        self.apikey = ApiKey(api_key)
        self.custom_fields = CustomFields(api_key)
        self.transactional_emails = TransactionalEmails(api_key)
        self.events = Events(api_key)
        self.contacts = Contacts(api_key)
