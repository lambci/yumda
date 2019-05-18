# Reflects the values hard-coded in various Makefile.am's in the source tree.
%define dictdir %{_datadir}/cracklib
%define dictpath %{dictdir}/pw_dict

Summary: A password-checking library
Name: cracklib
Version: 2.9.0
Release: 11%{?dist}.0.2
Group: System Environment/Libraries
Source0: http://prdownloads.sourceforge.net/cracklib/cracklib-%{version}.tar.gz

# Retrieved at 20091201191719Z.
Source1: http://iweb.dl.sourceforge.net/project/cracklib/cracklib-words/2008-05-07/cracklib-words-20080507.gz

# For man pages.
Source2: http://ftp.us.debian.org/debian/pool/main/c/cracklib2/cracklib2_2.8.19-1.debian.tar.gz
Source40: http://ftp.us.debian.org/debian/pool/main/c/cracklib2/cracklib2_2.8.19-1.dsc

# From attachment to https://bugzilla.redhat.com/show_bug.cgi?id=627449
Source3: cracklib.default.zh_CN.po

Source10: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Domains.gz
Source11: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Dosref.gz
Source12: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Ftpsites.gz
Source13: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/Jargon.gz
Source14: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/common-passwords.txt.gz
Source15: http://ftp.cerias.purdue.edu/pub/dict/wordlists/computer/etc-hosts.gz
Source16: http://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Movies.gz
Source17: http://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Python.gz
Source18: http://ftp.cerias.purdue.edu/pub/dict/wordlists/movieTV/Trek.gz
Source19: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/LCarrol.gz
Source20: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/Paradise.Lost.gz
Source21: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/cartoon.gz
Source22: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/myths-legends.gz
Source23: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/sf.gz
Source24: http://ftp.cerias.purdue.edu/pub/dict/wordlists/literature/shakespeare.gz
Source25: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/ASSurnames.gz
Source26: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Congress.gz
Source27: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Family-Names.gz
Source28: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/Given-Names.gz
Source29: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/famous.gz
Source30: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/fast-names.gz
Source31: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/female-names.gz
Source32: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/male-names.gz
Source33: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/names.french.gz
Source34: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/names.hp.gz
Source35: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/other-names.gz
Source36: http://ftp.cerias.purdue.edu/pub/dict/wordlists/names/surnames.finnish.gz

# No upstream source for this; it came in as a bugzilla attachment.
Source37: pass_file.gz
# https://bugzilla.redhat.com/show_bug.cgi?id=557592
# https://bugzilla.redhat.com/attachment.cgi?id=386022
Source38: ry-threshold10.txt
Patch1: cracklib-2.9.0-inttypes.patch
Patch2: cracklib-2.9.0-python-gzdicts.patch
Patch3: cracklib-2.9.0-packlib-lookup.patch
Patch4: cracklib-2.9.0-packlib-reentrant.patch
Patch5: cracklib-2.9.0-packlib-gztype.patch
Patch6: cracklib-2.9.0-simplistic.patch
Patch7: cracklib-2.9.0-translation-updates.patch
URL: http://sourceforge.net/projects/cracklib/
License: LGPLv2+
Buildroot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python-devel, words, gettext
BuildRequires: gettext-autopoint
BuildRequires: zlib-devel
Conflicts: cracklib-dicts < 2.8
# The cracklib-format script calls gzip, but without a specific path.
Requires: gzip

%description
CrackLib tests passwords to determine whether they match certain
security-oriented characteristics, with the purpose of stopping users
from choosing passwords that are easy to guess. CrackLib performs
several tests on passwords: it tries to generate words from a username
and gecos entry and checks those words against the password; it checks
for simplistic patterns in passwords; and it checks for the password
in a dictionary.

CrackLib is actually a library containing a particular C function
which is used to check the password, as well as other C
functions. CrackLib is not a replacement for a passwd program; it must
be used in conjunction with an existing passwd program.

Install the cracklib package if you need a program to check users'
passwords to see if they are at least minimally secure. If you install
CrackLib, you will also want to install the cracklib-dicts package.

%package devel
Summary: Development files needed for building applications which use cracklib
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The cracklib-devel package contains the header files and libraries needed
for compiling applications which use cracklib.

%package python
Summary: Python bindings for applications which use cracklib
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description python
The cracklib-python package contains a module which permits applications
written in the Python programming language to use cracklib.

%package dicts
Summary: The standard CrackLib dictionaries
Group: System Environment/Libraries
BuildRequires: words >= 2-13
Requires: cracklib = %{version}-%{release}

%description dicts
The cracklib-dicts package includes the CrackLib dictionaries.
CrackLib will need to use the dictionary appropriate to your system,
which is normally put in /usr/share/dict/words. Cracklib-dicts also
contains the utilities necessary for the creation of new dictionaries.

If you are installing CrackLib, you should also install cracklib-dicts.

%prep
%setup -q -a 2

# Replace zn_CN.po with one that wasn't mis-transcoded at some point.
grep '????????????????' po/zh_CN.po
install -p -m 644 %{SOURCE3} po/zh_CN.po

%patch1 -p1 -b .inttypes
%patch2 -p1 -b .gzdicts
%patch3 -p1 -b .lookup
%patch4 -p1 -b .reentrant
%patch5 -p1 -b .gztype
%patch6 -p1 -b .simplistic
%patch7 -p2 -b .translations

mkdir cracklib-dicts
for dict in %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} \
            %{SOURCE15} %{SOURCE16} %{SOURCE17} %{SOURCE18} %{SOURCE19} \
            %{SOURCE20} %{SOURCE21} %{SOURCE22} %{SOURCE23} %{SOURCE24} \
            %{SOURCE25} %{SOURCE26} %{SOURCE27} %{SOURCE28} %{SOURCE29} \
            %{SOURCE30} %{SOURCE31} %{SOURCE32} %{SOURCE33} %{SOURCE34} \
            %{SOURCE35} %{SOURCE36} %{SOURCE37} %{SOURCE38} %{SOURCE1}
do
        cp -fv ${dict} cracklib-dicts/
done
chmod +x util/cracklib-format

%build
%configure --with-pic --with-python --with-default-dict=%{dictpath} --disable-static
make -C po update-gmo
make

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT 'pythondir=${pyexecdir}'
./util/cracklib-format cracklib-dicts/* | \
./util/cracklib-packer $RPM_BUILD_ROOT/%{dictpath}
./util/cracklib-format $RPM_BUILD_ROOT/%{dictdir}/cracklib-small | \
./util/cracklib-packer $RPM_BUILD_ROOT/%{dictdir}/cracklib-small
rm -f $RPM_BUILD_ROOT/%{dictdir}/cracklib-small
sed s,/usr/lib/cracklib_dict,%{dictpath},g lib/crack.h > $RPM_BUILD_ROOT/%{_includedir}/crack.h
ln -s cracklib-format $RPM_BUILD_ROOT/%{_sbindir}/mkdict
ln -s cracklib-packer $RPM_BUILD_ROOT/%{_sbindir}/packer
touch $RPM_BUILD_ROOT/top

toprelpath=..
touch $RPM_BUILD_ROOT/top
while ! test -f $RPM_BUILD_ROOT/%{_libdir}/$toprelpath/top ; do
	toprelpath=../$toprelpath
done
rm -f $RPM_BUILD_ROOT/top
if test %{dictpath} != %{_libdir}/cracklib_dict ; then
ln -s $toprelpath%{dictpath}.hwm $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.hwm
ln -s $toprelpath%{dictpath}.pwd $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.pwd
ln -s $toprelpath%{dictpath}.pwi $RPM_BUILD_ROOT/%{_libdir}/cracklib_dict.pwi
fi
rm -f $RPM_BUILD_ROOT/%{_libdir}/python*/site-packages/_cracklib*.*a
rm -f $RPM_BUILD_ROOT/%{_libdir}/libcrack.la

mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man{3,8}
install -p -m644 debian/*.3 $RPM_BUILD_ROOT/%{_mandir}/man3/
install -p -m644 debian/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8/
if ! test -s $RPM_BUILD_ROOT/%{_mandir}/man8/cracklib-packer.8 ; then
    echo .so man8/cracklib-format.8 > $RPM_BUILD_ROOT/%{_mandir}/man8/cracklib-packer.8
fi
if ! test -s $RPM_BUILD_ROOT/%{_mandir}/man8/cracklib-unpacker.8 ; then
    echo .so man8/cracklib-format.8 > $RPM_BUILD_ROOT/%{_mandir}/man8/cracklib-unpacker.8
fi

%find_lang %{name}

%check
make test
# We want to check that the new library is able to open the new dictionaries,
# using the new python module.
LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir} %{__python} 2>&1 << EOF
import string, sys
# Prepend buildroot-specific variations of the python path to the python path.
syspath2=[]
for element in sys.path:
	syspath2.append("$RPM_BUILD_ROOT/" + element)
syspath2.reverse()
for element in syspath2:
	sys.path.insert(0,element)
# Now actually do the test.  If we get a different result, or throw an
# exception, the script will end with the error.
import cracklib
try:
	s = cracklib.FascistCheck("cracklib", "$RPM_BUILD_ROOT/%{dictpath}")
except ValueError, message:
	expected = "it is based on a dictionary word"
	if message != expected:
		print "Got unexpected result \"%s\"," % messgae,
		print "instead of expected value of \"%s\"." % expected
		sys.exit(1)
	print "Got expected result \"%s\"," % message
	sys.exit(0)
finally:
	sys.exit(0)
EOF

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%triggerpostun -p /sbin/ldconfig -- cracklib < 2.7-24

%files -f %{name}.lang
%defattr(-,root,root)
%doc README README-WORDS NEWS README-LICENSE AUTHORS COPYING.LIB
%{_libdir}/libcrack.so.*
%dir %{_datadir}/cracklib
%{_datadir}/cracklib/cracklib.magic
%{_sbindir}/*cracklib*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/libcrack.so
%{_mandir}/man3/*

%files dicts
%defattr(-,root,root)
%{_datadir}/cracklib/pw_dict.*
%{_datadir}/cracklib/cracklib-small.*
%{_libdir}/cracklib_dict.*
%{_sbindir}/mkdict
%{_sbindir}/packer

%files python
%defattr(-,root,root)
%{_libdir}/python*/site-packages/_cracklib*.so
%{_libdir}/python*/site-packages/*.py*

%changelog
* Thu Feb  6 2014 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-11
- move python files to libdir

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.9.0-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.9.0-9
- Mass rebuild 2013-12-27

* Tue Dec  3 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-8
- updated translations

* Thu Oct 31 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-7
- do not remove any printable characters in cracklib-format

* Thu Oct 31 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-6
- fix the broken zh_CN translation

* Tue Sep  3 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-5
- make the simplistic check and the purging of special characters much
  less aggressive (#1003624, #985378)

* Wed Aug 28 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-4
- revert compression of the dictionaries as the performance penalty is too big

* Wed Aug 21 2013 Tomáš Mráz <tmraz@redhat.com> - 2.9.0-3
- fix the python module to work with compressed dictionaries (#972542)
- fix various dictionary lookup errors (#986400, #986401)
- make the library reentrant and fix compilation warnings

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun  3 2013 Nalin Dahyabhai <nalin@redhat.com> - 2.9.0-1
- update to 2.9.0 (#970065)
  - adds FascistCheckUser()
- go ahead and compress the main dictionary, since we're linking with zlib
  anyway

* Tue Jan 29 2013 Nalin Dahyabhai <nalin@redhat.com> - 2.8.22-3
- point cracklib-packer and cracklib-unpacker man pages to cracklib-format
  (internal tooling)

* Wed Dec 19 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.22-2
- add missing buildrequires: on zlib-devel (#888876)

* Mon Dec 17 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.22-1
- update to 2.8.22 (#887461), which now returns an error instead of exiting
  when there's a failure opening the dictionary in FascistCheck()

* Thu Dec 13 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.21-1
- update to 2.8.21

* Mon Dec 10 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.20-1
- update to 2.8.20 (#885439)

* Tue Nov 20 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.19-3
- update the copy of the debian source package to one that can currently be
  retrieved using the URL we list for it

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.19-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri May 18 2012 Nalin Dahyabhai <nalin@redhat.com> - 2.8.19-1
- update to 2.8.19

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.18-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.18-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Jan 27 2011 Nalin Dahyabhai <nalin@redhat.com> - 2.8.18-1
- update to 2.8.18
- add man pages from Debian (#583932)
- replace zh_CN translation (related to #627449)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.8.16-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Sat Jul  3 2010 Dan Horák <dan[at]danny.cz> - 2.8.16-3
- added gettext-autopoint as BR:

* Thu May 20 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.16-2
- pull in changes to the Hindi translation (#589188)

* Tue Apr 20 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.16-1
- update to 2.8.16

* Fri Jan 22 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.15-3
- add passwords derived from rockyou breach data to the dictionaries (Matthew
  Miller, #557592)

* Thu Jan 21 2010 Nalin Dahyabhai <nalin@redhat.com> - 2.8.15-2
- update license: tag
- include license file

* Tue Dec  1 2009 Nalin Dahyabhai <nalin@redhat.com> - 2.8.15-1
- update to 2.8.15
- update cracklib-words to the current version (2008-05-07)
- fixup URLs for various dictionary sources that we use
- fix freeing-an-uninitialized-pointer in the python module (SF#2907102)
- add a disttag

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 18 2009 Nalin Dahyabhai <nalin@redhat.com> - 2.8.13-5
- add explicit dependency on gzip for the sake of cracklib-format (Daniel
  Mach, #501278)

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Feb 19 2009 Nalin Dahyabhai <nalin@redhat.com> - 2.8.13-3
- drop trailing "." from the package description for the dicts
  subpackage (#225659)

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.8.13-2
- Rebuild for Python 2.6

* Tue Oct 28 2008 Nalin Dahyabhai <nalin@redhat.com> - 2.8.13-1
- update to 2.8.13, which overhauls the python bindings and revises
  FascistCheck()'s behavior:
  2.8.12 success: returns None, fail: returns error text, other: exceptions
  2.8.13 success: returns candidate, fail: throws ValueError, other: exceptions

* Tue Oct 28 2008 Nalin Dahyabhai <nalin@redhat.com> - 2.8.12-3
- fix errors rebuilding with libtool that's newer than the one upstream
  has (#467364)

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.8.12-2
- Autorebuild for GCC 4.3

* Fri Jan 25 2008 Nalin Dahyabhai <nalin@redhat.com> - 2.8.12-1
- update to 2.8.12, which was relicensed to GPLv2
- package the now-bundled cracklib-small dictionary in cracklib-dicts

* Tue Aug 21 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.10-3
- rebuild

* Mon Jul 23 2007 Nalin Dahyabhai <nalin@redhat.com>
- add a %%check script to catch things like #249210

* Mon Jul 23 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.10-2
- work around non-executable util/cracklib-format giving us empty/garbage
  dictionaries (#249210)

* Thu Jul 19 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.10-1
- update to 2.8.10

* Wed Jun 20 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-11
- improve reports of out-of-memory exceptions so that they don't include a
  bogus filename
- improve reports of file-missing exceptions from the python module so that
  they give the right filename (#225858)

* Mon Mar 12 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-10
- explicitly include required headers from <packer.h> (#228698)
- attempt to provide doc strings in the python module

* Mon Feb 12 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-9
- drop final "." from summaries (Jef Spaleta, #225659)
- drop static library from -devel subpackage (Jef Spaleta, #225659)
- note that the most recently-added wordlist came from bugzilla (#225659)
- remove explicit dependency on gzip, as it's implicit (Jef Spaleta, #225659)
- convert %%triggerpostun to not use a shell as an interpreter (#225659)

* Wed Jan 31 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-8
- add word list from attachment #126053 (#185314)

* Thu Jan 25 2007 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-7
- fix check for the existence of dictionaries when the caller specifies a
  location (#224347, upstream #1644628)

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.8.9-6
- rebuild against python 2.5

* Sun Oct 29 2006 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-5
- split out cracklib-python (#203327)

* Sun Oct 29 2006 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-4
- split out cracklib-devel (#203569)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.9-3.1
- rebuild

* Mon Jun 12 2006 Jesse Keating <jkeating@redhat.com> - 2.8.9-3
- Add missing br, automake, libtool (#194738)

* Tue Apr 25 2006 Nalin Dahyabhai <nalin@redhat.com> - 2.8.9-2
- update to 2.8.9
- only create compat symlinks for the dictionaries if we aren't installing
  them into the old locations

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.8.6-1.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.8.6-1.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov  7 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.6-1
- update to 2.8.6
- remove .la file (#172632)

* Wed Sep 28 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.5-2
- update to 2.8.5

* Tue Sep 27 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.4-1
- update to 2.8.4
- build python module

* Fri May 13 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.3-1
- update to 2.8.3

* Thu Mar 17 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.2-1
- update to 2.8.2

* Wed Mar 16 2005 Nalin Dahyabhai <nalin@redhat.com> 2.8.1-1
- update to 2.8.1
  - moves dictionary to new default location under %%{_datadir} -- the
    dictionary format is the same across all architectures
  - renames "packer" to "cracklib-packer"
- conflict with cracklib-dicts < 2.8, where the on-disk format was not
  compatible on 64-bit arches due to now-fixed cleanliness bugs
- move binaries for manipulating and checking words against dictionaries
  from -dicts into the main package

* Mon Jan  3 2005 Nalin Dahyabhai <nalin@redhat.com> 2.7-30
- rebuild

* Mon Jan  3 2005 Nalin Dahyabhai <nalin@redhat.com> 2.7-29
- correctly build on 64-bit systems (part of #143417)
- patch so that 32- and 64-bit libcrack can read dictionaries which were
  incorrectly generated on 64-bit systems of the same endianness (more #143417)
- include a sample cracklib magic file
- stop using /usr/dict/* when building the dictionary
- list words as a build requirement, which it is, instead of a run-time
  requirement
- provide a virtual arch-specific dep in cracklib-dicts, require it in
  cracklib (part of #143417)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb  4 2004 Nalin Dahyabhai <nalin@redhat.com> 2.7-26
- update URL (previous page moved) (#114894)

* Fri Jan 30 2004 Nalin Dahyabhai <nalin@redhat.com> 2.7-25
- fix ldconfig invocation in trigger for older versions which included the
  soname symlink (#114620)

* Mon Dec  1 2003 Nalin Dahyabhai <nalin@redhat.com> 2.7-24
- include packer.h for reading dictionaries directly, since we already include
  packer in the -dicts subpackage (#68339)
- don't include the soname symlink in the package, let ldconfig do its job

* Wed Jun 18 2003 Nalin Dahyabhai <nalin@redhat.com> 2.7-23
- rebuild

* Mon Jun 16 2003 Nalin Dahyabhai <nalin@redhat.com> 2.7-22
- rebuild

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Apr 30 2003 Nalin Dahyabhai <nalin@redhat.com>
- update URL

* Tue Feb 04 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add symlink to shared libs

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Sep 25 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-19
- fix for builds on multilib systems (set DICTPATH properly)

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Sun May 26 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May  9 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-16
- rebuild in new environment

* Fri Feb 22 2002 Nalin Dahyabhai <nalin@redhat.com> 2.7-15
- rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue Oct  2 2001 Nalin Dahyabhai <nalin@redhat.com> 2.7-13
- use getpwuid_r instead of getpwuid

* Fri Aug  3 2001 Nalin Dahyabhai <nalin@redhat.com> 2.7-12
- remove cruft that ldconfig already knows how to manage
- don't explicitly strip anything -- the brp setup decides that
- tweak the header so that it can be used in C++ (#46685)
- buildprereq the words package

* Tue Jun 26 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add link from library major version number

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jun 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- FHS fixes
- fix undeclared function warnings from the new compiler
- fix URL

* Fri Apr 07 2000 Trond Eivind Glomsrød <teg@redhat.com>
- switched to use /usr/share/dict/words

* Tue Apr 06 1999 Preston Brown <pbrown@redhat.com>
- strip binaries

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- build for glibc 2.1

* Sat May 09 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Mar 10 1998 Cristian Gafton <gafton@redhat.com>
- updated to 2.7
- build shared libraries

* Mon Nov 03 1997 Donnie Barnes <djb@redhat.com>
- added -fPIC

* Mon Oct 13 1997 Donnie Barnes <djb@redhat.com>
- basic spec file cleanups

* Mon Jun 02 1997 Erik Troan <ewt@redhat.com>
- built against glibc
