Summary: User-space access to Linux Kernel SCTP
Name: lksctp-tools
Version: 1.0.17
Release: 2%{?dist}.0.2
# src/apps/bindx_test.C is GPLv2, I've asked upstream for clarification
License: GPLv2 and GPLv2+ and LGPLv2 and MIT
Group: System Environment/Libraries
URL: http://lksctp.sourceforge.net
Source0:  http://downloads.sourceforge.net/lksctp/%{name}-%{version}.tar.gz
Patch0: lksctp-tools-1.0.6-libdir.patch
Patch1: lksctp-tools-1.0.17-sctp_status-fix-hostname-resolution.patch
BuildRequires: libtool, automake, autoconf

%description
This is the lksctp-tools package for Linux Kernel SCTP (Stream Control
Transmission Protocol) Reference Implementation.

This package is intended to supplement the Linux Kernel SCTP Reference
Implementation now available in the Linux kernel source tree in
versions 2.5.36 and following.  For more information on LKSCTP see the
package documentation README file, section titled "LKSCTP - Linux
Kernel SCTP."

This package contains the base run-time library and command-line tools.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
[ ! -x ./configure ] && sh bootstrap
%configure --disable-static
# remove rpath from libtool
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
make install DESTDIR="$RPM_BUILD_ROOT" INSTALL="install -p"

%files
%defattr(-,root,root,-)
%license COPYING*
%{_bindir}/*
%{_libdir}/libsctp.so.*
%dir %{_libdir}/lksctp-tools/
%{_libdir}/lksctp-tools/libwithsctp.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/lksctp-tools/*.la
%exclude %{_libdir}/lksctp-tools/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Jun 27 2016 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.0.17-2
- Added patch fixing issue with sctp_status and DNS with IPv6 addresses.
  [1349497]

* Tue May 10 2016 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.0.17-1
- Update to 1.0.17

* Wed Nov 18 2015 Marcelo Ricardo Leitner <mleitner@redhat.com> - 1.0.16-1
- Update to 1.0.16

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.0.13-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.0.13-2
- Mass rebuild 2013-12-27

* Fri Jan 25 2013 Daniel Borkmann <dborkman@redhat.com> - 1.0.13-1
- Update to 1.0.13

* Mon Jan 21 2013 Jan Safranek <jsafrane@redhat.com> - 1.0.12-1
- Update to 1.0.12

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.11-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Oct 05 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.0.11-2
- Merge-review cleanup (#226100)

* Tue Dec  1 2009 Jan Safranek <jsafrane@redhat.com> 1.0.11-1
- Update to 1.0.11
- Remove rpath from compiled binaries
- Remove static libraries

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Zdenek Prikryl <zprikryl@redhat.com> 1.0.10-1
- added release tag to Requires of devel and doc packages (#492531)
- Update to 1.0.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 06 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.0.9-1
- Update to 1.0.9

* Wed Jul 16 2008 Zdenek Prikryl <zprikryl@redhat.com> 1.0.8-1
- Update to 1.0.8

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.0.7-3
- Autorebuild for GCC 4.3

* Wed Aug 29 2007 Karsten Hopp <karsten@redhat.com> 1.0.7-2
- rebuild for buildid

* Wed Aug 08 2007 Karsten Hopp <karsten@redhat.com> 1.0.7-1
- update to 1.0.7
- update license tag

* Wed Feb 21 2007 Karsten Hopp <karsten@redhat.com> 1.0.6-3
- add post/postun requirements
- review fixes

* Tue Sep 19 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-2
- fix fileconflict (#205225)

* Tue Jul 25 2006 Karsten Hopp <karsten@redhat.de> 1.0.6-1
- update to 1.0.6

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.0.5-1.fc5.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Tue Jan 24 2006 Warren Togami <wtogami@redhat.com> 1.0.5-1
- 1.0.5

* Fri Nov 11 2005 Matthias Saou <http://freshrpms.net/> 1.0.4-1
- Update to 1.0.4.
- Update syntax patch.
- Execute bootstrap if no configure script is found.
- Don't own entire man? directories.
- Own data and lib lksctp-tools directories.
- Move devel libs in _libdir/lksctp-tools/ to devel package.
- Exclude .la files.
- Minor spec file cleanups.

* Wed Mar 02 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-5
- build with gcc-4

* Mon Feb 07 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-4
- initialize variable before use
- fix subscript out of range bug (#147286)

* Mon Jan 24 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-3
- build for FC

* Mon Jan 24 2005 Karsten Hopp <karsten@redhat.de> 1.0.2-2.40E.1
- initial RH version based on sourceforge rpm

* Thu Dec 30 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.2-1
- 1.0.2 Release

* Tue May 11 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.1-1
- 1.0.1 Release

* Thu Feb 26 2004 Sridhar Samudrala <sri@us.ibm.com> 1.0.0-1
- 1.0.0 Release

* Fri Feb  6 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.9.0-1
- package only .txt doc files

* Wed Feb  4 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.7.5-1
- badly placed & undelivered files
- simplified delivery list

* Tue Jan 27 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 0.7.5-1
- Integrate comment from project team

* Sat Jan 10 2004 Francois-Xavier Kowalski <francois-xavier.kowalski@hp.com> 2.6.0_test7_0.7.4-1
- Creation
