from ..models.users import CurrentUser
from ..utils import _from_data
from .core import BackendAdapter


class AuthBackend(BackendAdapter):
    async def _login(
        self,
        email: str,
        password: str,
        device_id: str,
    ):
        url = "/auth/signin"
        data = {
            "auth_type": "header",
            "email": email,
            "password": password,
            "device_id": device_id,
        }
        response = await self._backend._request(url, json=data, method="post")
        return _from_data(CurrentUser, response["payload"]["user"])

    async def _register(
        self, email: str, password: str, region: str, device_id: str, recaptcha: str
    ):
        url = "/auth/registration"
        data = {
            "auth_type": "header",
            "email": email,
            "password": password,
            "region": region,
            "device_id": device_id,
            "recaptcha": recaptcha,
        }
        response = await self._backend._request(url, json=data, method="post")
        return _from_data(CurrentUser, response)

    async def _restore(self, email: str):
        url = "/auth/restore"
        data = {
            "email": email,
        }
        await self._backend._request(url, json=data, method="post")
        return None
