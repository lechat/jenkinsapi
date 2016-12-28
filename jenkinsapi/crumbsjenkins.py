"""
Wrapper class for Jenkins with enabled CSRF protection
"""
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.crumb_requester import CrumbRequester


class CrumbsJenkins(Jenkins):
    def __init__(
            self, baseurl,
            username=None, password=None,
            lazy=False, ssl_verify=True):
        """
        Creates CrumbsRequester and initializes Jenkins object with it

        :param str baseurl: baseurl for jenkins instance including port
        :param str username: username for jenkins auth
        :param str password: password for jenkins auth
        :return: a Jenkins obj
        """
        requester = CrumbRequester(
            username,
            password,
            baseurl=baseurl,
            ssl_verify=ssl_verify
        )
        super(CrumbsJenkins, self).__init__(
            baseurl=baseurl, username=username, password=password,
            requester=requester, lazy=lazy, ssl_verify=ssl_verify
        )
