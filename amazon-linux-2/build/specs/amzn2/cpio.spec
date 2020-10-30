Summary: A GNU archiving program
Name: cpio
Version: 2.11
Release: 28%{?dist}
License: GPLv3+
Group: Applications/Archiving
URL: http://www.gnu.org/software/cpio/
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2
# help2man generated manual page distributed only in RHEL/Fedora
Source1: cpio.1
#We use SVR4 portable format as default .
Patch1: cpio-2.9-rh.patch
#fix warn_if_file_changed() and set exit code to 1 when cpio
# fails to store file > 4GB (#183224)
Patch2: cpio-2.9-exitCode.patch
#Support major/minor device numbers over 127 (bz#450109)
Patch3: cpio-2.9-dev_number.patch
#define default remote shell as /usr/bin/ssh(#452904)
Patch4: cpio-2.9.90-defaultremoteshell.patch
#fix segfault with nonexisting file with patternnames(#567022)
Patch5: cpio-2.10-patternnamesigsegv.patch
#fix rawhide buildfailure by updating gnulib's stdio.in.h
Patch6: cpio-2.11-stdio.in.patch
# fix bad file name splitting while creating ustar archive (#866467)
Patch7: cpio-2.10-longnames-split.patch
# cpio does Sum32 checksum, not CRC
Patch8: cpio-2.11-crc-fips-nit.patch

# use the config.guess/config.sub files from actual automake-1.13
# ~> #925189
Patch9: cpio-2.11-arm-config-sub-guess.patch

# "really" check for read() return value
Patch10: cpio-2.11-treat-read-errors.patch

# Small typo in RU translation
# ~> #1075510
# ~> downstream?
Patch11: cpio-2.11-ru-translation.patch

Patch12: cpio-2.11-CVE-2014-9112.patch
Patch13: cpio-2.11-testsuite-CVE-2014-9112.patch

# Correct crc checksum (rhbz#1415081)
# ~> upstream ccec71ec318f
Patch14: cpio-2.11-crc-big-files.patch

# Reproducible archives (rhbz#1386662)
# ~> upstream 3945f9db4 + small warning patch.
Patch15: cpio-2.11-reproducible.patch

# Don't segfault during recovery
# ~> upstream fd262d116c4564c1796
Patch16: cpio-2.11-recovery.patch

# Improper input validation
# ~> upstream 7554e3e42cd72f6f8304410c47fe6f8918e9bfd7
Patch17: cpio-2.11-CVE-2019-14866.patch

Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info
Provides: bundled(gnulib)
Provides: /bin/cpio
BuildRequires: texinfo, autoconf, automake, gettext, rmt
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%prep
%setup -q
%patch1 -p1 -b .rh
%patch2 -p1 -b .exitCode
%patch3 -p1 -b .dev_number
%patch4 -p1 -b .defaultremote
%patch5 -p1 -b .patternsegv
%patch6 -p1 -b .gnulib %{?_rawbuild}
%patch7 -p1 -b .longnames
%patch8 -p1 -b .sum32-fips
%patch9 -p1 -b .arm-config-guess-sub
%patch10 -p1 -b .safe-read-check
%patch11 -p1 -b .ru-translation
%patch12 -p1 -b .CVE-2014-9112
%patch13 -p1 -b .CVE-2014-9112-test
%patch14 -p1 -b .crc-big-files
%patch15 -p1 -b .reproducible
%patch16 -p1 -b .recovery
%patch17 -p1

autoreconf -v

%build

CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -fno-strict-aliasing -Wall" %configure --with-rmt="%{_sysconfdir}/rmt"
make %{?_smp_mflags}
(cd po && make update-gmo)


%install
rm -rf ${RPM_BUILD_ROOT}

make DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p" install


rm -f $RPM_BUILD_ROOT%{_libexecdir}/rmt
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*.1*
install -c -p -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1

%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%check
rm -f ${RPM_BUILD_ROOT}/test/testsuite
make check


%post
if [ -f %{_infodir}/cpio.info.gz ]; then
	/sbin/install-info %{_infodir}/cpio.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
	if [ -f %{_infodir}/cpio.info.gz ]; then
		/sbin/install-info --delete %{_infodir}/cpio.info.gz %{_infodir}/dir || :
	fi
fi

%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README THANKS TODO COPYING
%{_bindir}/*
%{_mandir}/man*/*
%{_infodir}/*.info*

%changelog
* Fri Mar 13 2020 Ondrej Dubaj <odubaj@redhat.com> - 2.11-28
- Improper input validation when writing tar header fields (#1766222)

* Mon Feb 06 2017 Pavel Raiskup <praiskup@redhat.com> - 2.11-27
- don't segfault during recovery (rhbz#1318084)

* Mon Feb 06 2017 Pavel Raiskup <praiskup@redhat.com> - 2.11-26
- reproducible archives (rhbz#1386662)

* Mon Feb 06 2017 Pavel Raiskup <praiskup@redhat.com> - 2.11-25
- fix crc checksum for files ~200M+ (rhbz#1415081)

* Wed Jul 08 2015 Pavel Raiskup <praiskup@redhat.com> - 2.11-24
- fix for CVE-2014-9112

* Wed May 20 2015 Pavel Raiskup <praiskup@redhat.com> - 2.11-23
- better check for read() error (rhbz#1138148)
- fix ru translation (rhbz#1075513)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.11-22
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.11-21
- Mass rebuild 2013-12-27

* Wed Mar 27 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-20
- fix another bogus date in changelog
- update config.guess/config.sub for aarm64 build (#925189)
- run autoreconf instead of autoheader

* Fri Mar 15 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-19
- revert the fix for memory leak (at least for now) #921725

* Tue Mar 12 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-18
- explicitly provide /bin/cpio for packages that are dependant on this file

* Mon Mar 11 2013 Pavel Raiskup <praiskup@redhat.com> - 2.11-17
- fix small memory leak in copyin.c (#919454)
- remove %%defattr and install 'cpio' to real %%{_bindir}
- CovScan: add %%{?_rawbuild}

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Nov 05 2012 Pavel Raiskup <praiskup@redhat.com> - 2.11-15
- disable the temporary O_SYNC fix (glibc is fixed - #872366)

* Fri Nov 02 2012 Pavel Raiskup <praiskup@redhat.com> - 2.11-14
- fix bad changelog entries
- allow to build in Fedora Rawhide (temporarily because of #872336) (the value
  is guessed from from /usr/include/asm-generic/fcntl.h)

* Mon Oct 22 2012 Pavel Raiskup <praiskup@redhat.com> 2.11-13
- move RH-only manual page cpio.1 from look-aside cache into dist-git repository

* Thu Oct 18 2012 Pavel Raiskup <praiskup@redhat.com> 2.11-12
- fix for bad file name splitting while creating ustar archive (#866467)

* Wed Aug 29 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-11
- add missing options to manpage (#852765)

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 04 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-9
- fix build failure in rawhide build system (gets undefined)

* Wed May 30 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-8
- drop unnecessary patches: cpio-2.9-dir_perm.patch and
  cpio-2.9-sys_umask.patch - reported by M.Castellini

* Tue May 15 2012 Ondrej Vasik <ovasik@redhat.com> 2.11-7
- add virtual provides for bundled(gnulib) copylib (#821749)

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Oct 14 2011 Ondrej Vasik <ovasik@redhat.com> 2.11-5
- update manpage to reflect new option, polish the style (#746209)

* Mon Mar 07 2011 Ondrej Vasik <ovasik@redhat.com> 2.11-4
- fix several typos and manpage syntax(Ville Skyttä, #682470)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon May 31 2010 Ondrej Vasik <ovasik@redhat.com> 2.11-2
- built with fno-strict-aliasing(#596153)

* Thu Mar 11 2010 Ondrej Vasik <ovasik@redhat.com> 2.11-1
- new upstream release 2.11
- removed applied patches, run test suite

* Wed Mar 10 2010 Ondrej Vasik <ovasik@redhat.com> 2.10-6
- CVE-2010-0624 fix heap-based buffer overflow by expanding
  a specially-crafted archive(#572150)
- comment patches

* Thu Feb 25 2010 Ondrej Vasik <ovasik@redhat.com> 2.10-5
- remove redundant setLocale patch
- fix segfault with nonexisting file with patternnames
  (#567022)

* Wed Jan 06 2010 Ondrej Vasik <ovasik@redhat.com> 2.10-4
- do not fail with new POSIX 2008 utimens() glibc call
  (#552320)

* Thu Aug 06 2009 Ondrej Vasik <ovasik@redhat.com> 2.10-3
- do process install-info only without --excludedocs(#515924)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 22 2009 Ondrej Vasik <ovasik@redhat.com> 2.10-1
- new upstream release 2.10

* Mon Mar  9 2009 Ondrej Vasik <ovasik@redhat.com> 2.9.90-5
- define default remote shell as /usr/bin/ssh(#452904)
- use /etc/rmt as default rmt command

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9.90-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 11 2009 Ondrej Vasik <ovasik@redhat.com> 2.9.90-3
- make -d honor system umask(#484997)

* Fri Jul 18 2008 Kamil Dudka <kdudka@redhat.com> 2.9.90-2
- Support major/minor device numbers over 127 (bz#450109)

* Tue Jun 03 2008 Ondrej Vasik <ovasik@redhat.com> 2.9.90-1
- new upstream alpha version 2.9.90 + removed applied patches

* Mon Mar 03 2008 Radek Brich <rbrich@redhat.com> 2.9-7
- fix -dir_perm patch to restore permissions correctly even
  in passthrough mode -- revert affected code to cpio 2.8 state
  (bz#430835)

* Thu Feb 14 2008 Radek Brich <rbrich@redhat.com> 2.9-6
- when extracting archive created with 'find -depth',
  restore the permissions of directories properly (bz#430835)
- fix for GCC 4.3

* Thu Nov 01 2007 Radek Brich <rbrich@redhat.com> 2.9-5
- upstream patch for CVE-2007-4476 (stack crashing in safer_name_suffix)

* Tue Sep 04 2007 Radek Brich <rbrich@redhat.com> 2.9-4
- Updated license tag

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 2.9-3
- Rebuild for selinux ppc32 issue.

* Thu Jul 19 2007 Radek Brich <rbrich@redhat.com> 2.9-1.1
- fix spec, rebuild

* Thu Jul 19 2007 Radek Brich <rbrich@redhat.com> 2.9-1
- update to 2.9, GPLv3

* Tue Feb 20 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-27
- fix typo in changelog

* Thu Feb 08 2007 Ruben Kerkhof <ruben@rubenkerkhof.com> 2.6-26
- Preserve timestamps when installing files

* Thu Feb 08 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-25
- set cpio bindir properly

* Wed Feb 07 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-24
- fix spec file to meet Fedora standards (#225656) 

* Mon Jan 22 2007 Peter Vrabec <pvrabec@redhat.com> 2.6-23
- fix non-failsafe install-info use in scriptlets (#223682)

* Sun Dec 10 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-22
- fix rpmlint issue in spec file

* Tue Dec 05 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-21
- fix setlocale (#200478)

* Sat Nov 25 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-20
- cpio man page provided by RedHat

* Tue Jul 18 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-19
- fix cpio --help output (#197597)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6-18.1
- rebuild

* Sat Jun 10 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-18
- autoconf was added to BuildRequires, because autoheader is 
  used in prep phase (#194737)

* Tue Mar 28 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-17
- rebuild

* Sat Mar 25 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-15
- fix (#186339) on ppc and s390

* Thu Mar 23 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-14
- init struct  file_hdr (#186339)

* Wed Mar 15 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-13
- merge toAsciiError.patch with writeOutHeaderBufferOverflow.patch
- merge largeFileGrew.patch with lfs.patch
- fix large file support, cpio is able to store files<8GB 
  in 'old ascii' format (-H odc option)
- adjust warnings.patch

* Tue Mar 14 2006 Peter Vrabec <pvrabec@redhat.com> 2.6-12
- fix warn_if_file_changed() and set exit code to #1 when 
  cpio fails to store file > 4GB (#183224)

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 2.6-11.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 2.6-11.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Nov 23 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-11
- fix previous patch(writeOutHeaderBufferOverflow)

* Wed Nov 23 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-10
- write_out_header rewritten to fix buffer overflow(#172669)

* Mon Oct 31 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-9
- fix checksum error on 64-bit machines (#171649)

* Fri Jul 01 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-8
- fix large file support, archive >4GiB, archive members <4GiB (#160056)
- fix race condition holes, use mode 0700 for dir creation

* Tue May 17 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-7
- fix #156314 (CAN-2005-1229) cpio directory traversal issue
- fix some gcc warnings

* Mon Apr 25 2005 Peter Vrabec <pvrabec@redhat.com> 2.6-6
- fix race condition (#155749)
- use find_lang macro

* Thu Mar 17 2005 Peter Vrabec <pvrabec@redhat.com>
- rebuild 2.6-5

* Mon Jan 24 2005 Peter Vrabec <pvrabec@redhat.com>
- insecure file creation (#145721)

* Mon Jan 17 2005 Peter Vrabec <pvrabec@redhat.com>
- fix symlinks pack (#145225)

* Fri Jan 14 2005 Peter Vrabec <pvrabec@redhat.com>
- new fixed version of lfs patch (#144688)

* Thu Jan 13 2005 Peter Vrabec <pvrabec@redhat.com>
- upgrade to cpio-2.6

* Tue Nov 09 2004 Peter Vrabec <pvrabec@redhat.com>
- fixed "cpio -oH ustar (or tar) saves bad mtime date after Jan 10 2004" (#114580)

* Mon Nov 01 2004 Peter Vrabec <pvrabec@redhat.com>
- support large files > 2GB (#105617)

* Thu Oct 21 2004 Peter Vrabec <pvrabec@redhat.com>
- fix dependencies in spec

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- do not link against -lnsl

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 14 2003 Jeff Johnson <jbj@redhat.com> 2.5-3
- setlocale for i18n compliance (#79136).

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Mon Nov 18 2002 Jeff Johnson <jbj@redhat.com> 2.5-1
- update 2.5, restack and consolidate patches.
- don't apply (but include for now) freebsd and #56346 patches.
- add url (#54598).

* Thu Nov  7 2002 Jeff Johnson <jbj@redhat.com> 2.4.2-30
- rebuild from CVS.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Nov 22 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-25
- Fix up extraction of multiply linked files when the first link is
  excluded (Bug #56346)

* Mon Oct  1 2001 Bernhard Rosenkraenzer <bero@redhat.com> 2.4.2-24
- Merge and adapt patches from FreeBSD, this should fix FIFO handling

* Tue Jun 26 2001 Bernhard Rosenkraenzer <bero@redhat.com>
- Add and adapt Debian patch (pl36), fixes #45285 and a couple of other issues

* Sun Jun 24 2001 Elliot Lee <sopwith@redhat.com>
- Bump release + rebuild.

* Tue Aug  8 2000 Jeff Johnson <jbj@redhat.com>
- update man page with decription of -c behavior (#10581).

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Thu Jun 29 2000 Preston Brown <pbrown@redhat.com>
- patch from HJ Lu for better error codes upon exit

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- missing defattr.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 17 1999 Jeff Johnson <jbj@redhat.com>
- revert the stdout patch (#3358), restoring original GNU cpio behavior
  (#6376, #7538), the patch was dumb.

* Tue Aug 31 1999 Jeff Johnson <jbj@redhat.com>
- fix infinite loop unpacking empty files with hard links (#4208).
- stdout should contain progress information (#3358).

* Sun Mar 21 1999 Crstian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 12)

* Sat Dec  5 1998 Jeff Johnson <jbj@redhat.com>
- longlong dev wrong with "-o -H odc" headers (formerly "-oc").

* Thu Dec 03 1998 Cristian Gafton <gafton@redhat.com>
- patch to compile on glibc 2.1, where strdup is a macro

* Tue Jul 14 1998 Jeff Johnson <jbj@redhat.com>
- Fiddle bindir/libexecdir to get RH install correct.
- Don't include /sbin/rmt -- use the rmt from dump package.
- Don't include /bin/mt -- use the mt from mt-st package.
- Add prereq's

* Tue Jun 30 1998 Jeff Johnson <jbj@redhat.com>
- fix '-c' to duplicate svr4 behavior (problem #438)
- install support programs & info pages

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Fri Oct 17 1997 Donnie Barnes <djb@redhat.com>
- added BuildRoot
- removed "(used by RPM)" comment in Summary

* Thu Jun 19 1997 Erik Troan <ewt@redhat.com>
- built against glibc
- no longer statically linked as RPM doesn't use cpio for unpacking packages
