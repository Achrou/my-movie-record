import requests


class GistClient(object):
    BASE_API = "https://api.github.com"

    def __init__(self, token):
        self.headers = {
            'Authorization': 'token ' + token,
            'Accept': 'application/vnd.github.v3+json'
        }

    def create(self, data):
        r = requests.post(GistClient.BASE_API + '/gists', headers=self.headers, json=data)
        return r.status_code == 201

    def update(self, gistId, data):
        r = requests.patch(GistClient.BASE_API + '/gists/' + gistId, headers=self.headers, json=data)
        return r.status_code == 200
