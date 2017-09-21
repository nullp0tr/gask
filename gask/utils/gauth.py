import requests


class SessionManager(object):

    def __init__(self, url, login_suffix):
        self.url = url
        self.login_url = url + login_suffix
        self.last_referrer = ''
        self.session_client = requests.session()
        self.csrf_token = ''

    def start_connection(self):
        r = self.session_client.get(self.login_url)
        if r.status_code == 200:
            self.last_referrer = self.login_url
            self.update_csrftoken()
        return r

    def update_csrftoken(self):
        self.csrf_token = self.session_client.cookies['csrftoken']

    def login(self, username, password, next_url):
        r = self.session_client.post(
            self.login_url,
            data=dict(
                username=username,
                password=password,
                csrfmiddlewaretoken=self.csrf_token,
                next=next_url),
            headers=dict(Referer=self.last_referrer))
        self.last_referrer = next_url
        return r

    def post(self, data, url_suffix):
        self.update_csrftoken()
        r = self.session_client.post(
            self.url + url_suffix,
            data=data,
            headers={
                'X-CSRFToken': self.csrf_token,
                'Referer': self.last_referrer
            })
        return r

    def patch(self, data, url_suffix):
        self.update_csrftoken()
        r = self.session_client.patch(
            self.url + url_suffix,
            data=data,
            headers={
                'X-CSRFToken': self.csrf_token,
                'Referer': self.last_referrer
            })
        return r

    def delete(self, data, url_suffix):
        self.update_csrftoken()
        r = self.session_client.delete(
            self.url + url_suffix,
            data=data,
            headers={
                'X-CSRFToken': self.csrf_token,
                'Referer': self.last_referrer
            })
        return r
