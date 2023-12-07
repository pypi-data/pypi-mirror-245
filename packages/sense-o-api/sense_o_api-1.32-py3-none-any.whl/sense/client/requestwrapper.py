import sys

import requests

from sense.client.apiclient import ApiClient

sys.path.insert(0, '..')


class RequestWrapper(ApiClient):
    def __init__(self):
        super(RequestWrapper, self).__init__()

    def _get(self, api_path, params):
        url = self.config['REST_API'] + api_path
        out = requests.get(url,
                           headers=self.config['headers'],
                           verify=self.config['verify'],
                           params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.get(url,
                               headers=self.config['headers'],
                               verify=self.config['verify'],
                               params=params)
        return out

    def _put(self, api_path, data, params):
        url = self.config['REST_API'] + api_path
        out = requests.put(url,
                           headers=self.config['headers'],
                           verify=self.config['verify'],
                           data=data,
                           params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.put(url,
                               headers=self.config['headers'],
                               verify=self.config['verify'],
                               data=data,
                               params=params)
        return out

    def _post(self, api_path, data, params):
        url = self.config['REST_API'] + api_path
        out = requests.post(url,
                            headers=self.config['headers'],
                            verify=self.config['verify'],
                            data=data,
                            params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.post(url,
                                headers=self.config['headers'],
                                verify=self.config['verify'],
                                data=data,
                                params=params)
        return out

    def _delete(self, api_path, params):
        url = self.config['REST_API'] + api_path
        out = requests.delete(url,
                              headers=self.config['headers'],
                              verify=self.config['verify'],
                              params=params)
        if out.status_code == 401:
            self._refreshToken()
            out = requests.delete(url,
                                  headers=self.config['headers'],
                                  verify=self.config['verify'],
                                  params=params)
        return out

    def request(self, call_type, api_path, **kwargs):
        ret = None
        params = None
        if kwargs.get('query_params'):
            params = kwargs.get('query_params')

        if call_type == "GET":
            ret = self._get(api_path, params)
        elif call_type == "PUT":
            ret = self._put(api_path, kwargs.get('body_params'), params)
        elif call_type == "POST":
            if kwargs.get('body_params'):
                ret = self._post(api_path, kwargs.get('body_params'), params)
            else:
                raise ValueError(
                    "Missing the body parameter for POST to '%s'" % api_path)
        elif call_type == "DELETE":
            ret = self._delete(api_path, params)

        if ret is not None and ret.status_code >= 400 and ret.headers.get("content-type") == "application/json":
            json = ret.json()
            error_message = str(json)
            if "exception" in json:
                error_message = json.get("exception")
            raise ValueError(
                    f"Returned code {ret.status_code} with error '{error_message}'")

        return ret.text if ret.text is not None else ret
