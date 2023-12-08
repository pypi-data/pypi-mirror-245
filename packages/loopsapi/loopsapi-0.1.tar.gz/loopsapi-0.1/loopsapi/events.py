from loopsapi.endpoint import Endpoint


class Events(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: Loops API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/events/send"

    def send(self, email, eventName):
        '''
        Send events to trigger emails in Loops.

        :param str email: The contact’s email address. If there is no contact
                          with this email, one will be created.
        :param str eventName: The name of the event.
        '''
        return self._make_call(
            [],
            method="POST",
            json={
                "email": email,
                "eventName": eventName,
            }
        ).json()
