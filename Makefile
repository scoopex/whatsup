
DESTDIR=$(PWD)/debian/whatsup/
TESTPKG=init

all:
	 true
	 @echo -- DESTDIR CONFIGURED TO$(DESTDIR)--
	 @echo
	 @echo ' usage => make DESTDIR=<dir> test|doctest|install|pkg'

clean:
	 find  doc/ -name "*.1*" -exec rm -rvf {} \;
	 find  doc/ -name "*.pyc" -exec rm -rvf {} \;

test: doc install
	 @echo "-- running testcases --"
	 $(DESTDIR)/usr/sbin/whatsup -p 1|awk '{print $$3}'|grep "/sbin/init"
	 $(DESTDIR)/usr/sbin/whatsup -P "$(TESTPKG)" |awk '{print $$3}'|grep "1"
	 $(DESTDIR)/usr/sbin/whatsup -r "$(TESTPKG)" |awk '{print $$5}'|grep "$(TESTPKG)"
	 $(DESTDIR)/usr/sbin/whatsup -r -e "$(TESTPKG)_2.86.ds1-38_i386.deb" |awk '{print $$5}'|grep "$(TESTPKG)"
	 cat examples/apt-mode-testcase.txt|$(DESTDIR)/usr/sbin/whatsup -r -a -i|awk '{print $$5}'|grep "$(TESTPKG)"
	 @echo "-- all testcases sucessfully executed --"


doctest: doc
	 man doc/whatsup.1

doc: clean
	 docbook-to-man doc/whatsup.sgml > doc/whatsup.1

install: doc
	 @echo "--- installing to $(DESTDIR) ---"
	 mkdir -p $(DESTDIR)/usr/sbin
	 mkdir -p $(DESTDIR)/usr/share/whatsup/
	 cp sbin/whatsup $(DESTDIR)/usr/sbin/ 
	 cp lib/whatsup/*.py $(DESTDIR)/usr/share/whatsup/
	 mkdir -p $(DESTDIR)/etc/apt/apt.conf.d/
	 cat examples/etc/apt/apt.conf.d/99whatsup|\
	 sed "s/\"\/.*whatsup/\"\/usr\/sbin\/whatsup/;s/Options::.*whatsup::/Options::\/usr\/sbin\/whatsup::/" \
	 > $(DESTDIR)/etc/apt/apt.conf.d/99whatsup
	 find $(DESTDIR) -type d -exec chmod 755 {} \;
	 find $(DESTDIR) -type f -exec chmod 644 {} \;
	 find $(DESTDIR) -type f -path "*bin*" -exec chmod 755 {} \;
	 @echo "--- install to $(DESTDIR) finished ---"

pkg:
	 dpkg-buildpackage -rfakeroot -I.svn -us -uc
	 #dpkg-buildpackage -rfakeroot -I.svn 
	 @echo "*** contents of the package"
	 dpkg --contents ../`basename $(PWD)|tr '-' '_'`*.deb
	 @echo "*** contents of the source-package"
	 tar ztvf ../`basename $(PWD)|tr '-' '_'`*.tar.gz 

distclean:
	@echo no need to do that
