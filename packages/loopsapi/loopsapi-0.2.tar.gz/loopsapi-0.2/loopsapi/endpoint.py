import requests


class Endpoint:
    api_uri = "https://app.loops.so/api/v1"
    endpoint = None

    def __init__(self, api_key):
        '''init

        :param str api_key: Loops API KEY
        '''
        self.api_key = api_key

    def _craft_url(self, endpoint, params):
        '''make api url

        :param str endpoint: Endpoint to format
        :param list params: Parameters to insert in endpoint
        '''
        return "{}{}".format(
            self.api_uri,
            endpoint.format(*params) if params else endpoint,
        )

    def _create_call_headers(self):
        '''create headers'''
        return {
            "Authorization": "Bearer {}".format(self.api_key),
        }

    def _make_call(self, endpoint_params, params=None, endpoint=None,
                   json=None, method="GET"):
        '''make call api

        :param list endpoint_params: Endpoint params list
        :param dict params: Query params for request
        :param str endpoint: Endpoint for request
        :param dict json: Data for request
        :param str method: Method for request
        '''
        return requests.request(
            method,
            headers=self._create_call_headers(),
            url=self._craft_url(
                self.endpoint if not endpoint else endpoint,
                endpoint_params
            ),
            json=json,
            params=params,
        )
