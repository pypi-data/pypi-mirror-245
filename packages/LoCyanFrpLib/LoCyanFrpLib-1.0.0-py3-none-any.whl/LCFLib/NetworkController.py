from requests import Session


class LCFLibSession(Session):
    def __init__(self, BYPASS_SYSTEM_PROXY=False):
        super().__init__()
        #: Trust environment settings for proxy configuration, default
        #: authentication and similar.
        self.trust_env = BYPASS_SYSTEM_PROXY


post = LCFLibSession().post
get = LCFLibSession().get
delete = LCFLibSession().delete


def BYPASS_SYSTEM_PROXY(STATUS):
    """
    Bypass the system proxy to allow requests to POST OpenFrp OPENAPI normally.
    """
    global post, get, delete
    post = LCFLibSession(not STATUS).post
    get = LCFLibSession(not STATUS).get
    delete = LCFLibSession().delete


APIV2BASEURL = "https://api-v2.locyanfrp.cn"
