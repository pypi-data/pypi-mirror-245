from loopsapi.endpoint import Endpoint


class TransactionalEmails(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: Loops API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/transactional"

    def send(self, email, transactionalId, dataVariables={}):
        '''index
        Send a transactional email to a contact.

        :param str email: The contact’s email address. If there is no contact
                          with this email, one will be created.
        :param str transactionalId: The ID of the transactional email to send.
        :param str dataVariables: An object containing contact data as defined
                                  by the data variables added to the
                                  transactional email template.
        '''
        return self._make_call(
            [],
            method="POST",
            json={
                "email": email,
                "transactionalId": transactionalId,
                "dataVariables": dataVariables,
            }
        ).json()
