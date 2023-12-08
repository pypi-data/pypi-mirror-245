# core
from typing import Optional

# community
from pydantic import BaseModel

# custom
import wgconfigbuilder.lib.util as util

class Peer(BaseModel):
  id: str
  AllowedIPs: str
  Address: str
  PublicKey: Optional[str] = None
  PrivateKey: Optional[str] = None

def getModel(PeerId, config):
  peer = Peer(
    id = PeerId,
    Address = config[util.KEY_ADDRESS],
    AllowedIPs = config[util.KEY_PEER_ALLOWED_IPS],
  )
  if util.KEY_PUBLIC_KEY in config:
    peer.PublicKey = config[util.KEY_PUBLIC_KEY]
  if util.KEY_PRIVATE_KEY in config:
    peer.PrivateKey = config[util.KEY_PRIVATE_KEY]

  return peer