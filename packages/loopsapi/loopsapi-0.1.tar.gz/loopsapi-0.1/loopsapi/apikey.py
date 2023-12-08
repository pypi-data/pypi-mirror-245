from loopsapi.endpoint import Endpoint


class ApiKey(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: Loops API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/api-key"

    def test(self):
        '''index
        Check if API KEY is working
        '''
        return self._make_call([]).json()
