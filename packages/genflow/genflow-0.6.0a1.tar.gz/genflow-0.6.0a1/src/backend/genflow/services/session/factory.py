from typing import TYPE_CHECKING
from genflow.services.session.manager import SessionService
from genflow.services.factory import ServiceFactory

if TYPE_CHECKING:
    from genflow.services.cache.manager import BaseCacheService


class SessionServiceFactory(ServiceFactory):
    def __init__(self):
        super().__init__(SessionService)

    def create(self, cache_service: "BaseCacheService"):
        return SessionService(cache_service)
