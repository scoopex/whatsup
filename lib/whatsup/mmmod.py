#########################################################
###
### Marc Schoechlin [ms-debiantools@256bit.org]
###

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import glob,sys,re,os,getopt

re_whitespaces      = re.compile(r'\s+')
re_whitespacescolon = re.compile(r':\s*')
re_filename         = re.compile(r'^/.+/.+$')
re_device           = re.compile(r'^/dev/')

class MemoryMappedFiles:
  ''' This class helps to analyze information about
      memory-mapped files provided over the linux /proc-filesystem '''

  def __init__(self):
    self.mapped_files = {}
    self.installed_files = {}
    self.refreshMappedFiles()

  def refreshMappedFiles(self):
    
    map_files = glob.glob('/proc/[0-9]*/maps')

    mapped_files = {}

    for file in map_files:
     pid = file.split("/")[2]

     # skip finished processes
     if (not os.path.isfile(file)):
       print "skipped file '%s' - it seems that this process does not exist anymore" % file
       continue

     for line in open(file, 'r').readlines():
      words = re_whitespaces.split(line)
      if ((len(words) == 7) and 
          (re_filename.match(words[5])) and not
          (re_device.match(words[5]))
          ):
        mappedfile = words[5]
        if mapped_files.has_key(mappedfile):
          if (mapped_files[mappedfile]["pids"].count(pid) == 0):
             mapped_files[mappedfile]["pids"].append(pid)
        else:
          mapped_files[mappedfile] = {} 
          mapped_files[mappedfile]["pids"] = [ pid ]

    self.mapped_files = mapped_files 

  def getAllFiles(self):
    ret = self.mapped_files
    #for file in self.mapped_files.keys():
    #   if self.mapped_files[file].has_key("pids"):
       # for pid in self.mapped_files[file]["pids"]:
       #    res = self.getPackageByPid(pid)
       #    res.setdefault("pkg",())
    return ret

  def refreshPackageCache(self):

    # get all packages
    packages = []
    phandle = os.popen("dpkg --get-selections 2>/dev/null", 'r')
    for line in phandle:
     words = re_whitespaces.split(line) 
     if ((len(words) == 3) and (words[1] == "install")):
       packages.append(words[0])
    phandle.close()
   
    # fill package cache
    self.installed_files = {}
    for package in packages:
       print package
       phandle = os.popen("dpkg -L %s 2>/dev/null" % package)
       for file in phandle:
         self.installed_files[file] = package
       phandle.close()

  def getPackagesByPid(self,pid):

    ret = []
    if not os.path.isfile("/proc/%s/maps" % (pid)):
      print "it seems that process with pid '%s' does not exist anymore" % pid
      return ret

    files = {}
    # find all files
    for line in open("/proc/%s/maps" % (pid) , 'r').readlines():
      words = re_whitespaces.split(line)
      if (len(words) == 7) and (re_filename.match(words[5])):
         files[words[5]] = 1

    for filename in files.iterkeys():
      phandle = os.popen("dpkg -S '%s' 2>/dev/null" % filename, 'r')
      for line in phandle:
          line = line.rstrip("\n")
          words = re_whitespaces.split(line)
          if (len(words) == 2):
            retitem = {}
            retitem["pkg"] = words[0]
            retitem["file"] = words[1]
            retitem["pid"] = pid
            ret.append(retitem)
      phandle.close()
    return ret

  def queryPackages(self,packages):
    ret = {}
    for package in packages:
       phandle = os.popen("dpkg -L '%s' 2>/dev/null" % package)
       for file in phandle:
         file = file.rstrip('\n')
         if (file == "/."): continue
         self.installed_files[file] = package
         if self.mapped_files.has_key(file):
            if ret.has_key(package):
               ret[package].extend(self.mapped_files[file]["pids"])
            else:
               ret[package] = self.mapped_files[file]["pids"]
       phandle.close()
       if ret.has_key(package):
         ret[package] = list(set(ret[package])) 
    return ret

  def listInitScripts(self,packages):
    ret = {}
    for package in packages:
       phandle = os.popen("dpkg -L '%s' 2>/dev/null" % package)
       for file in phandle:
         file = file.rstrip('\n')
         if file.startswith("/etc/init.d/"):
           ret.setdefault(package,[])
           ret[package].append(file)
    return ret

  def resolveRunningPackages(self,packages): 
     running = {}
     pids = self.queryPackages(packages)
     for pkg,pids in pids.items():
       for pid in pids:
         ppkg = self.getPackageByPid(pid)
         if ppkg.has_key("pkg"):
           running.setdefault(ppkg["pkg"],{})
           running[ppkg["pkg"]].setdefault("pkgs",[])
           running[ppkg["pkg"]].setdefault("pids",[])
           if pkg not in running[ppkg["pkg"]]["pkgs"]:
             running[ppkg["pkg"]]["pkgs"].append(pkg)
           if pid not in running[ppkg["pkg"]]["pids"]:
             running[ppkg["pkg"]]["pids"].append(pid)
     return running

