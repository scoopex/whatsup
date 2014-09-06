whatsup
=======

resolve package dependencies of running packages 

This tool helps to find out, which service/Program needs not be restarted after a package update.

You love this project? Send a donation to the following bitcoin wallet: 1EGoDhAmaZbLazNmdZ9vDu2zYgFCKsNur5 

# Build

```
sudo apt-get install docbook-to-man
sudo make DESTDIR=/tmp/foo/ test 
sudo make DESTDIR=/tmp/foo/ pkg
ls ../whatsup*.deb
dpkg -i ../whatsup*.deb
```

# Usage

```
WHATSUP(1)                                                                                                               General Commands Manual                                                                                                              WHATSUP(1)

NAME
       whatsup — program to analyze package dependencies of running processes

SYNOPSIS
       whatsup {-f  | -h  | -p pid...  | -P pkg...  | -r pkg...  | -e file... }  [-a  | -d  | -i ]

DESCRIPTION
       This manual page documents briefly the whatsup command.

       This  tool  provides  information  about  package  and  file  dependencies  of  currently  running  processes.   Information  about  the files which are currently associated with a certain process is provided by ia file in the proc-filesystem.  Each line in
       /proc/$pid/maps represents a mapped region of the process. An entry in /proc/$pid/maps looks like this:

       08048000-08051000 r-xp 00000000 fe:08 76910      /sbin/init
       08051000-08052000 rwxp 00008000 fe:08 76910      /sbin/init
       08052000-08073000 rwxp 08052000 00:00 0          [heap]
       b7d4a000-b7d4b000 rwxp b7d4a000 00:00 0
       b7d4b000-b7d4d000 r-xp 00000000 fe:08 231672     /lib/tls/i686/cmov/libdl-2.5.so
       b7d4d000-b7d4f000 rwxp 00001000 fe:08 231672     /lib/tls/i686/cmov/libdl-2.5.so
       b7d4f000-b7e8a000 r-xp 00000000 fe:08 231662     /lib/tls/i686/cmov/libc-2.5.so

       Especially on server systems this is useful after security- and bugfix-updates to find out which processes have to be restarted.  The whatsup tool is automatically called after every apt-operation.

OPTIONS
       A summary of options is included below :

       -h        Show summary of options.

       -f        Display all files which are in use by currently running processes. Every filename is followed by a list of process ids which are using this file.

       -p        Resolve the names of the debian packages of the given proccess ids. This option displays a list of the given pids, the package name and the name of the running binary.

       -P        Display all process ids which use files which are part the given debian packages

       -r        Same as "-P", but also display the name of the debian-package the process-binary belongs to.

       -i        Display names of init scripts contained in the resulted packages. This option can be used with the "-r" switch.

       -e        Extract package names of given packagefiles - i.e. a package name like "foobar_2.86.ds1-38_i386.deb" is interpreted as "foobar". This option can be used with the "-r" and "-P" switch.

       -a        This option can be used to pass package-names over stdin by apt-get - i.e. calls over /etc/apt/apt.conf.d/99whatsup.

       -d        Debug mode

SEE ALSO
       n/a

AUTHOR
       This manual page was written by Marc Schoechlin ms-debian@256bit.org.  Permission is granted to copy, distribute and/or modify this document under the terms of the GNU General Public License, Version 2 any later version published by the Free Software  Foun‐
       dation.

       On Debian systems, the complete text of the GNU General Public License can be found in /usr/share/common-licenses/GPL.

```

