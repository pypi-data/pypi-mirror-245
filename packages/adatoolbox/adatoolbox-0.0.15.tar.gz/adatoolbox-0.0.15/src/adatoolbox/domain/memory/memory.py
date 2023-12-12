from redis import Redis
from django.conf import settings
from dataclasses import dataclass


@dataclass
class Memory:
    con: Redis = any

    @classmethod
    def __init_connection(self: "Memory") -> None:
        self.con = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            username=settings.REDIS_USER,
            password=settings.REDIS_PASSWORD)
    
    @classmethod
    def set(self: "Memory", key: str, value: str) -> None:
        self.__init_connection()
        self.con.set(key, value)
    
    @classmethod
    def get(self: "Memory", key: str) -> str:
        self.__init_connection()
        return self.con.get(key)
