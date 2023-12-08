# core
from typing import Optional

# community
from pydantic import BaseModel

# custom
import wgconfigbuilder.lib.util as util

class Server(BaseModel):
  Address: str
  DNS: str
  Endpoint: str
  ListenPort: Optional[int] = 51820
  PublicKey: Optional[str] = None
  PrivateKey: Optional[str] = None
  PersistentKeepalive: Optional[int] = 30
  
def getModel(ServerConfig):
  server = Server(
    Address = ServerConfig[util.KEY_ADDRESS],
    DNS = ServerConfig[util.KEY_SERVER_DNS],
    Endpoint = ServerConfig[util.KEY_SERVER_ENDPOINT]
  )
  if util.KEY_SERVER_LISTEN_PORT in ServerConfig:
    server.ListenPort = ServerConfig[util.KEY_SERVER_LISTEN_PORT]
  if util.KEY_PUBLIC_KEY in ServerConfig:
    server.PublicKey = ServerConfig[util.KEY_PUBLIC_KEY]
  if util.KEY_PRIVATE_KEY in ServerConfig:
    server.PrivateKey = ServerConfig[util.KEY_PRIVATE_KEY]

  return server
