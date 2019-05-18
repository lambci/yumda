%global library_version 1.0.6

Summary: A file compression utility
Name: bzip2
Version: 1.0.6
Release: 13%{?dist}.0.2
License: BSD
Group: Applications/File
URL: http://www.bzip.org/
Source: http://www.bzip.org/%{version}/%{name}-%{version}.tar.gz

Requires: bzip2-libs = %{version}-%{release}

Patch0: bzip2-1.0.4-saneso.patch
Patch1: bzip2-1.0.4-cflags.patch
# resolves: #226979
Patch2: bzip2-1.0.4-bzip2recover.patch

%description
Bzip2 is a freely available, patent-free, high quality data compressor.
Bzip2 compresses files to within 10 to 15 percent of the capabilities
of the best techniques available.  However, bzip2 has the added benefit
of being approximately two times faster at compression and six times
faster at decompression than those techniques.  Bzip2 is not the
fastest compression utility, but it does strike a balance between speed
and compression capability.

Install bzip2 if you need a compression utility.

%package devel
Summary: Libraries and header files for apps which will use bzip2
Group: Development/Libraries
Requires: bzip2-libs = %{version}-%{release}

%description devel

Header files and a library of bzip2 functions, for developing apps
which will use the library.

%package libs
Summary: Libraries for applications using bzip2
Group: System Environment/Libraries

%description libs

Libraries for applications using the bzip2 compression format.

%prep
%setup -q
%patch0 -p1 -b .saneso
%patch1 -p1 -b .cflags
%patch2 -p1 -b .bz2recover

%build
%ifarch ppc64 ppc64le
export O3="-O3"
%else
export O3=""
%endif

make -f Makefile-libbz2_so CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
    CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 -fpic -fPIC $O3" \
    %{?_smp_mflags} all

rm -f *.o
make CC="%{__cc}" AR="%{__ar}" RANLIB="%{__ranlib}" \
    CFLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64 $O3" \
    %{?_smp_mflags} all

%install
chmod 644 bzlib.h
mkdir -p $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1,%{_libdir},%{_includedir}}
cp -p bzlib.h $RPM_BUILD_ROOT%{_includedir}
install -m 755 libbz2.so.%{library_version} $RPM_BUILD_ROOT%{_libdir}
install -m 755 bzip2-shared  $RPM_BUILD_ROOT%{_bindir}/bzip2
install -m 755 bzip2recover bzgrep bzdiff bzmore  $RPM_BUILD_ROOT%{_bindir}/
cp -p bzip2.1 bzdiff.1 bzgrep.1 bzmore.1  $RPM_BUILD_ROOT%{_mandir}/man1/
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bunzip2
ln -s bzip2 $RPM_BUILD_ROOT%{_bindir}/bzcat
ln -s bzdiff $RPM_BUILD_ROOT%{_bindir}/bzcmp
ln -s bzmore $RPM_BUILD_ROOT%{_bindir}/bzless
ln -s libbz2.so.%{library_version} $RPM_BUILD_ROOT%{_libdir}/libbz2.so.1
ln -s libbz2.so.1 $RPM_BUILD_ROOT%{_libdir}/libbz2.so
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzip2recover.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bunzip2.1
ln -s bzip2.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcat.1
ln -s bzdiff.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzcmp.1
ln -s bzmore.1 $RPM_BUILD_ROOT%{_mandir}/man1/bzless.1

%post libs -p /sbin/ldconfig

%postun libs  -p /sbin/ldconfig

%files
%doc LICENSE CHANGES README
%{_bindir}/*
%{_mandir}/*/*

%files libs
%doc LICENSE
%{_libdir}/libbz2.so.1*

%files devel
%doc manual.html manual.pdf
%{_includedir}/*
%{_libdir}/*.so

%changelog
* Thu Jul 31 2014 jchaloup <jchaloup@redhat.com> - 1.0.6-13
- resolves: #1123489
  recompiled with -O3 flag for ppc64le arch

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.6-12
- Mass rebuild 2014-01-24

* Fri Jan 10 2014 Peter Schiffer <pschiffe@redhat.com> - 1.0.6-11
- related: #1051062
  added explicit requires on bzip2-libs subpackage from main package

* Fri Jan 10 2014 Peter Schiffer <pschiffe@redhat.com> - 1.0.6-10
- resolves: #1051062
  recompiled with -O3 flag for ppc64 arch

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.6-9
- Mass rebuild 2013-12-27

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Oct 26 2012 Peter Schiffer <pschiffe@redhat.com> - 1.0.6-7
- moved libraries from /lib to /usr/lib

* Fri Oct 26 2012 Peter Schiffer <pschiffe@redhat.com> - 1.0.6-6
- .spec file cleanup

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Sep 29 2010 jkeating - 1.0.6-2
- Rebuilt for gcc bug 634757

* Wed Sep 22 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.0.6-1
- update to 1.0.6

* Mon Jul 12 2010 Ivana Hutarova Varekova <varekova@redhat.com> - 1.0.5-7
- add LICENSE to bzip2-libs

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Mar 17 2009 Ivana Varekova <varekova@redhat.com> 1.0.5-5
- remove static library

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Sep  1 2008 Ivana Varekova <varekova@redhat.com> 1.0.5-3
- minor spec file changew

* Thu Apr 10 2008 Ivana Varekova <varekova@redhat.com> 1.0.5-2
- Resolves: #441775
  fix libs link

* Tue Mar 25 2008 Ivana Varekova <varekova@redhat.com> 1.0.5-1
- update to 1.0.5

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.4-14
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Ivana Varekova <varekova@redhat.com> 1.0.4-13
- rebuild

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-12
- fix *.so,*.a directory

* Mon May 21 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-11
- remove libbz2.* from /usr/lib* to /lib*

* Wed Apr  4 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-10
- change libz.a permissions

* Wed Apr  4 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-9
- remove useless -p 

* Thu Mar 15 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-8
- remove unnecessary "/" after RPM_BUILD_ROOT macro

* Mon Feb 19 2007 Jesse Keating <jkeating@redhat.com> 1.0.4-7
- Temporarily add static lib back in for rpm

* Fri Feb 16 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-6
- incorporate the next review feedback

* Thu Feb 15 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-5
- incorporate package review feedback

* Tue Feb  6 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-4
- fix bzip2recover patch

* Mon Feb  5 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-3
- Resolves: 226979 
  Buffer overflow in bzip2's bzip2recover

* Mon Jan  8 2007 Ivana Varekova <varekova@redhat.com> 1.0.4-1
- update to 1.0.4
- spec file cleanup

* Mon Jul 17 2006 Ivana Varekova <varekova@redhat.com> 1.0.3-3
- add cflags (#198926)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.3-2.2.2
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.3-2.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.3-2.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Nov 25 2005 Ivana Varekova <varekova@redhat.com> 1.0.3-2
- fix bug 174172 - CAN-2005-0758 bzgrep has security issue in sed usage

* Mon Aug 29 2005 Ivana Varekova <varekova@redhat.com> 1.0.3-1
- 1.0.3
- add NULL-ptr-check patch 
  (patch author: Mihai Limbasan <mihailim@gmail.com)

* Thu May 19 2005 Jiri Ryska <jryska@redhat.com>
- fixed permission setting for decompressed files #155742
- fixed decompression bomb (DoS) #157548

* Fri Mar 04 2005 Jiri Ryska <jryska@redhat.com>
- rebuilt

* Thu Dec 09 2004 Jiri Ryska <jryska@redhat.com>
- changed temp file creation in bzdiff #92444

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jun 17 2003 Jeff Johnson <jbj@redhat.com> 1.0.2-11
- rebuilt because of crt breakage on ppc64.

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Mar 31 2003 Jeff Johnson <jbj@redhat.com> 1.0.2-9
- rebuild to get rid of undefined __ctype_b in libbz2.a.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Nov 21 2002 Elliot Lee <sopwith@redhat.com>
- Pass __cc/__ar/__ranlib to makefiles
- Use _smp_mflags

* Tue Nov 19 2002 Tim Powers <timp@redhat.com>
- rebuild on all arches
- fix %%doc file list

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Apr 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0.2-3
- Rebuild in new environment

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0.2-2
- Rebuild

* Wed Jan 30 2002 Trond Eivind Glomsrød <teg@redhat.com> 1.0.2-1
- 1.0.2
- Total overhaul of build precedure
- Add many small helper programs added to 1.0.2
- drop old patches

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Nov 26 2001 Trond Eivind Glomsrød <teg@redhat.com> 1.0.1-5
- Don't segfault when infile is a directory and "-f" is used (#56623)
- Automake is evil. Add workaround

* Fri Mar 30 2001 Trond Eivind Glomsrød <teg@redhat.com>
- use "License" instead of "Copyright"
- split out libs

* Fri Jul 21 2000 Trond Eivind Glomsrød <teg@redhat.com>
- new URL and source location

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sat Jul 01 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 1.0.1
- ported my patch

* Tue Jun 13 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging to build on solaris2.5.1.
- remove config.cache from autoconf patch.
- sparc: use %%configure, but not the m4 macros.

* Tue Jun 06 2000 Trond Eivind Glomsrød <teg@redhat.com>
- Use %%configure, %%makeinstall, %%{_manpath} and %%{_tmpdir}

* Wed May 17 2000 Trond Eivind Glomsrød <teg@redhat.com>
- 1.0.0 - ported my 1.0pre8 libtoolizedautoconf patch

* Tue May 16 2000 Trond Eivind Glomsrød <teg@redhat.com>
- use soft links, not hardlinks, for binaries
- mv .so to devel

* Mon May 15 2000 Trond Eivind Glomsrød <teg@redhat.com>
- autoconfed and libtoolized package 
- fixed Copyright (it's BSD, not GPL)
- dumped bzless (less works fine with bz2-files)
- rewrote build and install parts
- separated main package and devel package

* Mon May  8 2000 Bernhard Rosenkränzer <bero@redhat.com>
- 1.0pre8

* Fri Apr 14 2000 Bernhard Rosenkränzer <bero@redhat.com>
- Add bzgrep (a version of zgrep hacked to do bzip2)

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Fri Dec 31 1999 Bernhard Rosenkränzer <bero@redhat.com>
- 0.9.5d
- Update download URL, add URL: tag in header

* Tue Aug 10 1999 Jeff Johnson <jbj@redhat.com>
- upgrade to 0.9.5c.

* Mon Aug  9 1999 Bill Nottingham <notting@redhat.com>
- install actual bzip2 binary, not libtool cruft.

* Sun Aug  8 1999 Jeff Johnson <jbj@redhat.com>
- run ldconfig to get shared library.

* Mon Aug  2 1999 Jeff Johnson <jbj@redhat.com>
- create shared libbz1.so.* library.

* Sun Apr  4 1999 Jeff Johnson <jbj@redhat.com>
- update to bzip2-0.9.0c.

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 4)

* Thu Dec 17 1998 Cristian Gafton <gafton@redhat.com>
- build against glibc 2.1

* Wed Sep 30 1998 Cristian Gafton <gafton@redhat.com>
- force compilation with egcs to avoid gcc optimization bug (thank God 
  we haven't been beaten by it)

* Wed Sep 09 1998 Cristian Gafton <gafton@redhat.com>
- version 0.9.0b

* Tue Sep 08 1998 Cristian Gafton <gafton@redhat.com>
- updated to 0.9.0

* Thu Apr 09 1998 Cristian Gafton <gafton@redhat.com>
- first build for Manhattan
