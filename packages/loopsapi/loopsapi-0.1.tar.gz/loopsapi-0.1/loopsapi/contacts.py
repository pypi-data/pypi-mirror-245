from loopsapi.endpoint import Endpoint


class Contacts(Endpoint):

    def __init__(self, api_key):
        '''init

        :param str api_key: Loops API KEY
        '''
        super().__init__(api_key)
        self.endpoint = "/contacts"

    def find(self, email):
        '''
        Find contact

        :param str email: The contact’s email address.
                          Make sure it is URI-encoded.
        '''
        return self._make_call(
            [],
            endpoint="/contacts/find",
            params={
                "email": email,
            }
        ).json()

    def create(self, email, firstName=None, lastName=None, source=None,
               subscribed=False, userGroup=None, userId=None):
        '''
        Create contact

        :param str email: The contact’s email address.
        :param str firstName: The contact’s first name.
        :param str lastName: The contact’s last name.
        :param str source: A custom source value to replace the default “API”.
        :param bool subscribed: Whether the contact will receive campaign
                                and loops emails.
        :param str userGroup: You can use groups to segemnt users when sending
                              emails. Currently a contact can only be in one
                              user group.
        :param str userId: A unique user ID
                          (for example, from an external application).
        '''
        return self._make_call(
            [],
            method="POST",
            endpoint="/contacts/create",
            json={
                "email": email,
                "firstName": firstName,
                "lastName": lastName,
                "source": source,
                "subscribed": subscribed,
                "userGroup": userGroup,
                "userId": userId,
            }
        ).json()

    def update(self, email, firstName=None, lastName=None, source=None,
               subscribed=False, userGroup=None, userId=None):
        '''
        Update contact

        :param str email: The contact’s email address.
        :param str firstName: The contact’s first name.
        :param str lastName: The contact’s last name.
        :param str source: A custom source value to replace the default “API”.
        :param bool subscribed: Whether the contact will receive campaign
                                and loops emails.
        :param str userGroup: You can use groups to segemnt users when sending
                              emails. Currently a contact can only be in one
                              user group.
        :param str userId: A unique user ID
                          (for example, from an external application).
        '''
        local = vars()
        return self._make_call(
            [],
            method="PUT",
            endpoint="/contacts/update",
            json={
                key: local[key] for key in local
                if local[key] is not None and key != 'self'
            }
        ).json()

    def delete(self, email=None, userId=None):
        '''
        Delete contact

        :param str email: The contact’s email address.
        :param str userId: The contact’s userId value.
        '''
        local = vars()
        return self._make_call(
            [],
            method="POST",
            endpoint="/contacts/delete",
            json={
                key: local[key] for key in local
                if local[key] is not None and key != 'self'
            }
        ).json()
