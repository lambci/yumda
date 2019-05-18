Name: trousers
Summary: TCG's Software Stack v1.2
Version: 0.3.14
Release: 2%{?dist}.0.2
License: BSD
Group: System Environment/Libraries
Url: http://trousers.sourceforge.net
Source0: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz
Source1: tcsd.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libtool, openssl-devel
BuildRequires: systemd-units
# submitted upstream https://sourceforge.net/p/trousers/mailman/message/35766729/
Patch0001: unlock-in-err-path.patch

Prefix: %{_prefix}

%description
TrouSerS is an implementation of the Trusted Computing Group's Software Stack
(TSS) specification. You can use TrouSerS to write applications that make use
of your TPM hardware. TPM hardware can create, store and use RSA keys
securely (without ever being exposed in memory), verify a platform's software
state using cryptographic hashes and more.

%prep
%setup -cq
%patch1 -p1

%build
%configure --with-gui=openssl --disable-static
make -k %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_localstatedir}/lib/tpm
make install DESTDIR=${RPM_BUILD_ROOT} INSTALL="install -p"
rm -f ${RPM_BUILD_ROOT}/%{_libdir}/libtspi.la

%files
%defattr(-, root, root, -)
%license LICENSE
%{_sbindir}/tcsd
%{_libdir}/libtspi.so.?
%{_libdir}/libtspi.so.?.?.?
%config(noreplace) %attr(0600, tss, tss) %{_sysconfdir}/tcsd.conf
%attr(0700, tss, tss) %{_localstatedir}/lib/tpm/

%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.so
%exclude %{_includedir}
%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Apr 03 2017 Jerry Snitselaar <jsnitsel@redhat.com> 0.3.14-2
- release mutex in err path for obj_context_set_machine_name

* Thu Mar 30 2017 Jerry Snitselaar <jsnitsel@redhat.com> 0.3.14-1
Resolves: rhbz#1384446 Rebase Trousers to latest version

* Sun May 24 2015 Avesh Agarwal <avagarwa@redhat.com> 0.3.13-1
Resolves: rhbz#1173221 New upstream bug fix release

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.3.11.2-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.3.11.2-2
- Mass rebuild 2013-12-27

* Mon Aug 19 2013 Steve Grubb <sgrubb@redhat.com> 0.3.11.2-1
- New upstream bug fix and license change release

* Sun Jun 02 2013 Steve Grubb <sgrubb@redhat.com> 0.3.10-3
- Remove +x bit from service file (#963916)

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Steve Grubb <sgrubb@redhat.com> 0.3.10-1
- New upstream bug fix release

* Thu Aug 30 2012 Steve Grubb <sgrubb@redhat.com> 0.3.9-4
- Make daemon full RELRO

* Mon Aug 27 2012 Steve Grubb <sgrubb@redhat.com> 0.3.9-3
- bz #836476 - Provide native systemd service

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 21 2012 Steve Grubb <sgrubb@redhat.com> 0.3.9-1
- New upstream bug fix release

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Apr 08 2011 Steve Grubb <sgrubb@redhat.com> 0.3.6-1
- New upstream bug fix release

* Thu Feb 10 2011 Miloš Jakubíček <xjakub@fi.muni.cz> - 0.3.4-5
- Fix paths in man pages, mark them as %%doc -- fix BZ#676394

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat May 01 2010 Miloš Jakubíček <xjakub@fi.muni.cz> - 0.3.4-3
- Fix init script to conform to Fedora guidelines
- Do not overuse macros

* Mon Feb 08 2010 Steve Grubb <sgrubb@redhat.com> 0.3.4-2
- Fix issue freeing a data structure

* Fri Jan 29 2010 Steve Grubb <sgrubb@redhat.com> 0.3.4-1
- New upstream bug fix release
- Upstream requested the tpm-emulator patch be dropped

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.1-19
- rebuilt with new openssl

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 14 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.3.1-17
- Do not overuse macros.
- Removed unnecessary file requirements on chkconfig, ldconfig and service,
  now requiring the initscripts and chkconfig packages.

* Wed May 06 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.3.1-16
- Fix a typo in groupadd causing the %%pre scriptlet to fail (resolves BZ#486155).

* Mon Apr 27 2009 Milos Jakubicek <xjakub@fi.muni.cz> - 0.3.1-15
- Fix FTBFS: added trousers-0.3.1-gcc44.patch

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.1-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 0.3.1-13
- rebuild with new openssl

* Tue Dec 16 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.3.1-12
- Bump release to avoid wrong tag in rawhide

* Tue Dec 16 2008 David Woodhouse <David.Woodhouse@intel.com> - 0.3.1-11
- Work around SELinux namespace pollution (#464037)
- Use SO_REUSEADDR
- Use TPM emulator if it's available and no hardware is

* Fri Aug 08 2008 Emily Ratliff <ratliff@austin.ibm.com> - 0.3.1-10
- Use the uid/gid pair assigned to trousers from BZ#457593

* Fri Aug 01 2008 Emily Ratliff <ratliff@austin.ibm.com> - 0.3.1-9
- Incorporated changes from the RHEL package which were done by Steve Grubb

* Wed Jun 04 2008 Emily Ratliff <ratliff@austin.ibm.com> - 0.3.1-8
- Fix cast issue preventing successful build on ppc64 and x86_64

* Tue Jun 03 2008 Emily Ratliff <ratliff@austin.ibm.com> - 0.3.1-7
- Fix for BZ #434267 and #440733. Patch authored by Debora Velarde

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.3.1-6
- Autorebuild for GCC 4.3

* Mon Dec 17 2007 Kent Yoder <kyoder@users.sf.net> - 0.3.1-5
- Updated static rpm's comment line (too long)

* Thu Dec 13 2007 Kent Yoder <kyoder@users.sf.net> - 0.3.1-4
- Updated specfile for RHBZ#323441 comment #28

* Wed Dec 12 2007 Kent Yoder <kyoder@users.sf.net> - 0.3.1-3
- Updated specfile for RHBZ#323441 comment #22

* Wed Nov 28 2007 Kent Yoder <kyoder@users.sf.net> - 0.3.1-2
- Updated to include the include dirs in the devel package;
added the no-install-hooks patch

* Wed Nov 28 2007 Kent Yoder <kyoder@users.sf.net> - 0.3.1-1
- Updated specfile for RHBZ#323441 comment #13

* Mon Nov 12 2007 Kent Yoder <kyoder@users.sf.net> - 0.3.1
- Updated specfile for comments in RHBZ#323441

* Wed Jun 07 2006 Kent Yoder <kyoder@users.sf.net> - 0.2.6-1
- Updated build section to use smp_mflags
- Removed .la file from installed dest and files section

* Tue Jun 06 2006 Kent Yoder <kyoder@users.sf.net> - 0.2.6-1
- Initial add of changelog tag for trousers CVS
