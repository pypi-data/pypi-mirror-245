# core
import sys
import os

# custom
import wgconfigbuilder.lib.util as util
import wgconfigbuilder.lib.build as build

  

def main():
  print (f"cwd: {os.getcwd()}")

  util.autoCreateFolders()
  parser = util.parseArgs()

  args = parser.parse_args()
  args.func(args)
  
  try:
    # os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))
    # print (f'Script path: {os.path.dirname(os.path.abspath(sys.argv[0]))}')
    True
  except Exception as err:
    parser.print_help()
    print ('\n')
    print ('[ERROR] ' + str(err))

  # print (json.dumps(yaml.load('hello: world', Loader=yaml.Loader), indent=2))
  # print (sys.argv)
  # print (f"Working dir: {os.getcwd()}")

  # # SrcPath = os.path.dirname(os.path.abspath(sys.argv[0] + "/../x"))
  # # sys.path.append(SrcPath)
  # # print (f"SrcPath: {SrcPath}")
  # import configbuilder.lib.mymodule as mymodule
  # mymodule.say()

print (f"__name__: {__name__}")
if __name__ == '__main__':
  main()