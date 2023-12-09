from loopsapi.endpoint import Endpoint


class CustomFields(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: Loops API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/customFields"

    def list(self):
        '''
        Get a list of your account's custom contact properties.
        '''
        return self._make_call([]).json()
