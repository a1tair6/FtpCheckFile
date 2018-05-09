import sys
import datetime
from ftplib import FTP

now = datetime.datetime.now()

my_dirs = []  # global
my_files = [] # global
curdir = ''   # global
dicByEms = {}
def recur_dirs(ftp, dirpath, emsName):
  tree_dir = []
  #  try:
  #original_dir = ftp.pwd()
  ftp.cwd(dirpath)
  ftp.retrlines('LIST', tree_dir.append)
  original_dir = ftp.pwd()
  for dir in tree_dir:
    if dir.startswith('d'):
      if "CONDITION" in dir:
        dirInfo = dir.split(' ')
        objname = dirInfo[len(dirInfo)-1]
        emsName = objname
        dicByEms[emsName] = 0
        #print(dirpath + "/" + objname)
        recur_dirs(ftp, dirpath + "/" + objname, emsName)
      elif now.strftime("%Y%m%d") in dir:
        dirInfo = dir.split(' ')
        objname = dirInfo[len(dirInfo)-1]
        #print(dirpath + "/" + objname)
        recur_dirs(ftp, dirpath + "/" + objname, emsName)
    else:
      if "CONDITION" not in dir:
        #print(dir)
        dirInfo = dir.split(' ')
        objsize = dirInfo[len(dirInfo)-5]
        objname = dirInfo[len(dirInfo)-1]
        #print(int(objsize))

        dicByEms[emsName]+=int(objsize)

        print('path : ' + original_dir + ', file : ' + objname + ', size : ' + objsize + ', ems : ' + emsName)
  return 0
#  except:
#    print('recur Except')


def main():
  ftp = FTP(sys.argv[1])
  ftp.login(sys.argv[2], sys.argv[3])

  recur_dirs(ftp, sys.argv[4], '')
  for x in dicByEms:
    print(x, dicByEms[x])
  ftp.cwd('/.') # change to root directory for downloading
  for f in my_files:
    print('getting ' + f)
    #file_name = f.replace('/', '_') # use path as filename prefix, with underscores
    #ftp.retrbinary('RETR ' + f, open(file_name, 'wb').write)
    sleep(1)
  #ftp.quit()
  print('all done!')

if __name__ == '__main__':
  main()
