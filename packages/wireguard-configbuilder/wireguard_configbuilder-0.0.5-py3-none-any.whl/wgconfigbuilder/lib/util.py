# core
import argparse
import os
import subprocess
import sys

# community
import yaml

# custom
# import src.lib.util as util
import wgconfigbuilder.lib.build as build

KEY_PUBLIC_KEY = 'PublicKey'
KEY_PRIVATE_KEY = 'PrivateKey'
KEY_ADDRESS = 'Address'

KEY_SERVER_LISTEN_PORT = 'ListenPort'
KEY_SERVER_ALLOWED_IPs = 'AllowedIPs'
KEY_SERVER_DNS = 'DNS'
KEY_SERVER_ENDPOINT = 'Endpoint'

KEY_PEER_ALLOWED_IPS = 'AllowedIPs'

def generatePublicPrivateKeys(TempPath):
  if not os.path.exists(TempPath):
    os.mkdir(TempPath)

  PrivateKeyFname = TempPath + '/temp-private.key'
  PublicKeyFname = TempPath + '/temp-public.key'
  child = subprocess.run(['sh','-c',f"wg genkey | tee {PrivateKeyFname} | wg pubkey | tee {PublicKeyFname}"])
  print (f"Child process: {child.stdout}")
  print (f"Child process: {child.returncode}")
  if not child.returncode == 0:
    raise Exception('Unable to generate keys')
  
  # generate keys: success
  infile = open(PublicKeyFname,'r')
  PublicKey = infile.read().strip()
  infile.close()

  infile = open(PrivateKeyFname,'r')
  PrivateKey = infile.read().strip()
  infile.close()

  os.remove(PublicKeyFname)
  os.remove(PrivateKeyFname)

  return PublicKey, PrivateKey

def autoCreateFolders():
  RootPath = os.getcwd()
  # RootPath = os.path.dirname(os.path.abspath(sys.argv[0] + "/../../x"))
  DataPath = RootPath + '/data'

  if not os.path.exists(DataPath):
    os.mkdir(DataPath)
    print (f"Created folder: {DataPath}")

def test(args):
  util.isFileExist(args.filename)
  util.isValidYaml(args.filename)
  print (f'Test successful: {args.filename}')

def isFileExist(filename):
  if not os.path.exists(filename):
    raise Exception(f'Missing filename {filename}')

def isValidYaml(filename):
  infile = open(filename, 'r')
  ret = yaml.load(infile.read(), Loader = yaml.Loader)
  infile.close()

  return ret

def parseArgs():
  parser = argparse.ArgumentParser(
    prog = 'wg-configbuilder.py',
    description = 'Generates config files from YAML config',
    exit_on_error=True
  )
  subparser = parser.add_subparsers(dest = 'cmd', help = 'Commands', required=True)

  # cmd TEST parser
  TestParser = subparser.add_parser('test', help = 'Test parser')
  TestParser.add_argument('filename', help = 'YAML file')
  TestParser.set_defaults(func = test)

  # cmd BUILD parser
  BuildParser = subparser.add_parser('build', help = 'Build config files')
  BuildParser.add_argument('filename', help = 'YAML file')
  BuildParser.set_defaults(func = build.build)

  return parser
