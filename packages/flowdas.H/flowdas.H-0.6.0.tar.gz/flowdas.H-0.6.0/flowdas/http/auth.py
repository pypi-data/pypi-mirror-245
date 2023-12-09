import typing

from typeable import Object, field

from flowdas.boot import Config


class User(Object):
    id: int

    async def get_scopes(self) -> frozenset[str]:
        return frozenset()


class InMemoryUser(User):
    scopes: list[str]

    async def get_scopes(self) -> frozenset[str]:
        return frozenset(self.scopes)


class UserService(Object):
    type: str = field(kind=True)

    async def findUserById(self, id: int) -> User:
        raise AuthError


class UserConfigService(UserService, kind='config'):
    map: dict[int, list[str]] = field(default_factory=dict)

    async def findUserById(self, id: int) -> User:
        try:
            return InMemoryUser({'id': id, 'scopes': self.map[id]})
        except KeyError:
            raise AuthError


class AuthError(Exception):
    pass


class AuthOutcome:
    def __init__(self, user: User = None, scopes: list[str] = None):
        self.user = user
        self._scopes = scopes

    async def get_scopes(self) -> list[str]:
        if self._scopes is None:
            if self.user is None:
                self._scopes = frozenset(Config.get_instance().anonymous or [])
            else:
                self._scopes = await self.user.get_scopes()
        return self._scopes


class Authenticator(Object):
    type: str = field(kind=True)

    async def authenticate(self, req, resp) -> typing.Optional[AuthOutcome]:
        return None

    def challenge(self) -> typing.Optional[str]:
        return None


class ApiKeyService(Object):
    type: str = field(kind=True)

    async def findUserIdByApiKey(self, apikey: str) -> int:
        raise AuthError


class ApiKeyConfigService(ApiKeyService, kind='config'):
    map: dict[str, int] = field(default_factory=dict)

    async def findUserIdByApiKey(self, apikey: str) -> int:
        try:
            return self.map[apikey]
        except KeyError:
            raise AuthError


class ApiKeyAuthenticator(Authenticator, kind='apiKey'):
    name: str = 'X-Api-Key'

    async def authenticate(self, req, resp) -> typing.Optional[AuthOutcome]:
        value = req.get_header(self.name)
        if value is not None:
            cfg = Config.get_instance()
            id = await cfg.apikey.findUserIdByApiKey(value)
            return AuthOutcome(await cfg.user.findUserById(id))
        return None
