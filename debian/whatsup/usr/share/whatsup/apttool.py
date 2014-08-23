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


class AptTools:
  ''' This class helps to analyze information about updated packages by apt-get'''

  def __init__(self):
     pass

  def read_apt_pipeline(self):
      version = sys.stdin.readline().rstrip()
      if version != "VERSION 2":
          sys.stderr.write(_('''Wrong or missing VERSION from apt pipeline  '''))
          sys.exit(1)

      while 1:
          line = sys.stdin.readline().rstrip()
          if not line:
              break

      pkgs = []
              
      for pkgline in sys.stdin.readlines():
          if not pkgline:
              break

          (pkgname, oldversion, compare, newversion, filename) = pkgline.split()

          if filename == '**CONFIGURE**':
              pass
          elif filename == '**REMOVE**':
              pass
          else:
              pkgs.append(pkgname) 


      # Sort by configuration order.  THIS IS IMPORTANT.  Sometimes, a
      # situation exists where package X contains changelog.gz (upstream
      # changelog) and depends on package Y which contains
      # changelog.Debian.gz (Debian changelog).  Until we have a more
      # reliable method for determining whether a package is Debian
      # native, this allows things to work, since Y will always be
      # configured first.
      return pkgs

