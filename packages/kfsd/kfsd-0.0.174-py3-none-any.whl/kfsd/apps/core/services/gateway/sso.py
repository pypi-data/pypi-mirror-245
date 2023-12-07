from rest_framework import status
from kfsd.apps.core.auth.api.gateway import APIGateway
from kfsd.apps.core.common.logger import Logger, LogLevel
from kfsd.apps.core.common.cache import cache

logger = Logger.getSingleton(__name__, LogLevel.DEBUG)


class SSO(APIGateway):
    def __init__(self, request=None):
        APIGateway.__init__(self, request)

    def getTokenPublicKeyUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.gateway_api.sso.public_key_uri",
            ]
        )

    def getRefreshAccessTokenUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.gateway_api.sso.refresh_access_token_uri",
            ]
        )

    def getLogoutUrl(self):
        return self.constructUrl(
            [
                "services.context.gateway_api.host",
                "services.context.gateway_api.sso.logout_uri",
            ]
        )

    @cache("kfsd.token.publickey")
    def tokenPublicKey(self):
        return self.httpGet(self.getTokenPublicKeyUrl(), status.HTTP_200_OK)

    def logout(self):
        return self.httpGet(self.getLogoutUrl(), status.HTTP_200_OK)

    def refreshAccessToken(self, payload):
        return self.httpPost(
            self.getRefreshAccessTokenUrl(), payload, status.HTTP_200_OK
        )

    def isAuthEnabled(self):
        isAuth = self.getDjangoRequest().findConfigs(
            ["services.features_enabled.auth"]
        )[0]
        return isAuth if isAuth else False
