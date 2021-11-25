import logging

import requests

from .base import PushwooshBaseClient


log = logging.getLogger('pypushwoosh.client.log')


class PushwooshClient(PushwooshBaseClient):
    """
    Implementation of the Pushwoosh API Client.
    """
    headers = {'User-Agent': 'PyPushwooshClient',
               'Content-Type': 'application/json',
               'Accept': 'application/json'}

    def __init__(self, timeout=None):
        PushwooshBaseClient.__init__(self)
        self.timeout = timeout

    def path(self, command):
        return '{}://{}/'.format(self.scheme, self.hostname) + '/'.join((self.endpoint, self.version,
                                                                         command.command_name))

    def invoke(self, command):
        PushwooshBaseClient.invoke(self, command)
        url = self.path(command)
        payload = command.render()

        r = requests.post(url, data=payload, headers=self.headers, timeout=self.timeout)

        if r.status_code != 200:
            msg = u'PushWoosh error: %s %s' % (r.status_code, r.text)
            if self.debug:
                log.debug(msg)
                log.debug('Command: %s' % payload)
            raise Exception(msg)

        try:
            result = r.json()
        except:
            msg = u"PushWoosh JSON error: %s" % r.text
            if self.debug:
                log.debug(msg)
                log.debug('Command: %s' % payload)
            raise Exception(msg)

        return result
