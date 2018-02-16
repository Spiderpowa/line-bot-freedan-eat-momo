# -*- coding: utf-8 -*-

class HttpClient:
    def __init__(self, timeout=30):
        self.timeout = timeout

    def __call__(self, timeout=30):
        self.timeout = timeout
        return self

    def get(self, url, headers=None, params=None, stream=False, timeout=None):
        pass

    def post(self, url, headers=None, data=None, timeout=None):
        pass