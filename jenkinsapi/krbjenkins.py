"""
Wrapper class for Jenkins with Kerberos authentication
"""
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.utils.krb_requester import KrbRequester
from requests_kerberos import OPTIONAL


class KerberosJenkins(Jenkins):
    def __init__(
            self, baseurl,
            lazy=False, ssl_verify=True, mutual_auth=OPTIONAL):
        """
        Creates KrbRequester and initializes Jenkins object with it

        :param str baseurl: baseurl for jenkins instance including port
        :param str username: username for jenkins auth
        :param str password: password for jenkins auth
        :return: a Jenkins obj
        """
        requester = KrbRequester(
            baseurl=baseurl,
            ssl_verify=ssl_verify,
            mutual_auth=mutual_auth
        )

        super(KerberosJenkins, self).__init__(
            baseurl=baseurl, requester=requester,
            lazy=lazy, ssl_verify=ssl_verify
        )
