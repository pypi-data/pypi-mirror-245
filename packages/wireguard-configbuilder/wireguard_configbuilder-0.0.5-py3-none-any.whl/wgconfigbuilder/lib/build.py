# core
import copy
import json
import os
import subprocess
import sys
from typing import Optional, List

# community
import yaml
from yaml import Dumper

# custom
import wgconfigbuilder.lib.util as util
import wgconfigbuilder.model.Server as ServerModel
from wgconfigbuilder.model.Server import Server
import wgconfigbuilder.model.Peer as PeerModel
from wgconfigbuilder.model.Peer import Peer

KEY_PUBLIC_KEY = 'PublicKey'
KEY_PRIVATE_KEY = 'PrivateKey'
KEY_ADDRESS = 'Address'

KEY_SERVER_LISTEN_PORT = 'ListenPort'
KEY_SERVER_ALLOWED_IPs = 'AllowedIPs'
KEY_SERVER_DNS = 'DNS'
KEY_SERVER_ENDPOINT = 'Endpoint'

KEY_PEER_ALLOWED_IPS = 'AllowedIPs'

def renderServer(server: Server):
  ret = f"""[Interface]
Address = {server.Address}
ListenPort = {server.ListenPort}
PrivateKey = {server.PrivateKey}
"""

  return ret

def renderPeer(peer: Peer):
  ret = f"""[Peer]
AllowedIPs = {peer.AllowedIPs}
PublicKey = {peer.PublicKey}
"""
  return ret

def renderPeerConf(server: Server, peer: Peer):
  return f"""[Interface]
PrivateKey = {peer.PrivateKey}
Address = {peer.Address}
DNS = {server.DNS}

[Peer]
PublicKey = {server.PublicKey}
AllowedIPs = {peer.AllowedIPs}
Endpoint = {server.Endpoint}
PersistentKeepalive = {server.PersistentKeepalive} 
"""

def renderServerConf(server: Server, peers: List[Peer]):
  ret = renderServer(server) + '\n'

  for peer in peers:
    ret += renderPeer(peer) + '\n'

  return ret

def autoPopulateKeys(TempPath, config, server: Server, peers: List[Peer]):
  IsConfigUpdated = False

  if server.PublicKey == None or server.PrivateKey == None:
    PublicKey, PrivateKey = util.generatePublicPrivateKeys(TempPath)
    server.PublicKey = PublicKey
    server.PrivateKey = PrivateKey
    config['server'][KEY_PUBLIC_KEY] = PublicKey
    config['server'][KEY_PRIVATE_KEY] = PrivateKey
    IsConfigUpdated = True

  for peer in peers:
    if peer.PublicKey == None or peer.PrivateKey == None:
      PublicKey, PrivateKey = util.generatePublicPrivateKeys(TempPath)
      peer.PublicKey = PublicKey
      peer.PrivateKey = PrivateKey
      config['peers'][peer.id][KEY_PUBLIC_KEY] = PublicKey
      config['peers'][peer.id][KEY_PRIVATE_KEY] = PrivateKey
      IsConfigUpdated = True

  return IsConfigUpdated, config

def writeConfFiles(DataPath, server: Server, peers: List[Peer]):
  # write wg0.conf
  ServerConf = renderServerConf(server, peers)
  ServerFname = DataPath + '/wg0.conf'
  outfile = open(ServerFname,'w')
  outfile.write(ServerConf)
  outfile.close()
  print (f"Generated: {ServerFname}")

  # write [client].conf
  for peer in peers:
    PeerConf = renderPeerConf(server, peer)
    PeerFname = f"{DataPath}/{peer.id}.conf"
    outfile = open(PeerFname,'w')
    outfile.write(PeerConf)
    outfile.close()
    print (f"Generated: {PeerFname}")

def writeYamlFile(config, ConfigFname):
  ConfigClone = copy.deepcopy(config)
  del ConfigClone['peers']
  ServerLines = yaml.dump(ConfigClone, Dumper=Dumper)

  ConfigClone = copy.deepcopy(config)
  del ConfigClone['server']
  PeerLines = yaml.dump(ConfigClone, Dumper=Dumper)

  outfile = open(ConfigFname,'w')
  outfile.write(f"{ServerLines}\n{PeerLines}")
  outfile.close()


def build(args):
  util.isFileExist(args.filename)
  config = util.isValidYaml(args.filename)
  server = ServerModel.getModel(config['server'])

  peers = []
  for PeerId in config['peers']:
    peer = PeerModel.getModel(PeerId, config['peers'][PeerId])
    peers.append(peer)

  # prepare to write to data/ folder
  RootPath = os.getcwd()
  # RootPath = os.path.dirname(os.path.abspath(sys.argv[0] + "/../../x"))
  DataPath = RootPath + '/data'
  TempPath = RootPath + '/temp'

  # identify which endpoint needs to generate public-private keys
  IsConfigUpdated, config = autoPopulateKeys(TempPath, config, server, peers)
  if IsConfigUpdated:
    # save file
    writeYamlFile(config, args.filename)

  writeConfFiles(DataPath, server, peers)    
  print (f'Build successful: {args.filename}')

