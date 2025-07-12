from .config import default_sdk_config, SdkConfig
from .connectionPool import ConnectionPool,set_connection,close_connection_pool
from .auth import sign_in_with_token,load_token_from_file
from .Folder import Folder
from .File import File
from typing import Optional
import os
class Sdk:
    def __init__(self, config: SdkConfig = None):
        self.config = config or default_sdk_config
        self.connection_pool = ConnectionPool(
            url=self.config.ws_url,
            pool_size=self.config.pool_size,
            # reconnect_delay=self.config.reconnect_delay_ms / 1000  # ms to seconds
        )
    @classmethod
    async def create(cls, config: SdkConfig = None):
        instance = cls(config)
        await instance.connect()      
        return instance
    
    async def connect(self):
        await self.connection_pool.connect()
        set_connection(self.connection_pool)

    async def sign_in(self, pin: Optional[str],token_path: Optional[str]):
        if not token_path:
            token_path = os.environ.get("TOKEN_PATH") or None
        if not token_path:
            raise ValueError("Token must be provided either via environment variable IZ_TOKEN or token_path argument.")
        token = await load_token_from_file(token_path)
        if not pin:
            pin = os.environ.get("PIN") or None
        if not pin:
            raise ValueError("PIN must be provided either via environment variable IZ_PIN or pin argument.")
        return await sign_in_with_token(token, pin=pin)
    async def get_root_folder(self):
        return Folder.get_root()
    async def get_file(self,path):
        return File.init_from_path(path)
    async def close(self):
        await close_connection_pool()
