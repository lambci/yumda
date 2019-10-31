Summary: CMS and X.509 library
Name:    libksba
Version: 1.3.0
Release: 5%{?dist}.0.2

# The library is licensed under LGPLv3+ or GPLv2+,
# the rest of the package under GPLv3+
License: (LGPLv3+ or GPLv2+) and GPLv3+
Group:   System Environment/Libraries
URL:     http://www.gnupg.org/
Source0: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/libksba/libksba-%{version}.tar.bz2.sig
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch1: libksba-1.3.0-multilib.patch

BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8
BuildRequires: libgcrypt-devel >= 1.2.0

Prefix: %{_prefix}

%description
KSBA (pronounced Kasbah) is a library to make X.509 certificates as
well as the CMS easily accessible by other applications.  Both
specifications are building blocks of S/MIME and TLS.

%prep
%setup -q

%patch1 -p1 -b .multilib


%build
%configure \
  --disable-dependency-tracking \
  --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%license COPYING*
%{_libdir}/libksba.so.8*

%exclude %{_bindir}/ksba-config
%exclude %{_libdir}/libksba.so
%exclude %{_includedir}
%exclude %{_datadir}
%exclude %{_infodir}

%changelog
* Thu Oct 31 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.3.0-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.3.0-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Dec  3 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.0-2
- fix multilib conflict in libksba-config

* Wed Nov 21 2012 Tomas Mraz <tmraz@redhat.com> - 1.3.0-1
- new upstream version

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Tomas Mraz <tmraz@redhat.com> - 1.2.0-1
- new upstream version

* Thu Jun 02 2011 Rex Dieter <rdieter@fedoraproject.org> 1.0.8-3
- libksba-devel multilib conflict (#601976)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 23 2010 Rex Dieter <rdieter@fedoraproject.org> - 1.0.8-1
- libksba-1.0.8

* Fri Jan  8 2010 Tomas Mraz <tmraz@redhat.com> - 1.0.7-1
- new upstream version

* Thu Dec 17 2009 Rex Dieter <rdieter@fedoraproject.org> - 1.0.6-4
- better (upstreamable) multilib patch
- tighten %%files a bit

* Mon Aug 10 2009 Ville Skyttä <ville.skytta@iki.fi> - 1.0.6-3
- Convert specfile to UTF-8.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat Jun 20 2009 Rex Dieter <rdieter@fedorproject.org> - 1.0.6-1
- libksba-1.0.6
- -devel: fix info scriptlet

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Jan 09 2009 Rex Dieter <rdieter@fedoraproject.org> 1.0.5-1
- libksba-1.0.5

* Tue Sep 23 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.4-1
- libksba-1.0.4

* Thu Apr 03 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-2
- multiarch conflicts (#342201)

* Tue Feb 12 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.3-1
- libksba-1.0.3

* Fri Feb 08 2008 Rex Dieter <rdieter@fedoraproject.org> 1.0.2-4
- respin (gcc43)

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-3
- BR: gawk

* Sat Aug 25 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-2
- respin (ppc32, BuildID)
- License: GPLv3

* Fri Jul 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 1.0.2-1
- libksba-1.0.2

* Fri Dec 01 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.1-1
- libksba-1.0.1

* Mon Oct 02 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.0-1.1
- respin

* Thu Aug 31 2006 Rex Dieter <rexdieter[AT]users.sf.net> 1.0.0-1
- libksba-1.0.0

* Tue Aug 29 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.15-3
- fc6 respin

* Tue Jun 20 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.15-2
- 0.9.15

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.13-2.1
- fc5: gcc/glibc respin

* Wed Nov 30 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.13-2
- remove hacks
- drop self Obsoletes

* Wed Nov 30 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.13-1
- 0.9.13

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.11-3
- botched Obsoletes good, let's try again.

* Fri Aug 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.11-2
- revert to 0.9.11 (0.9.12 makes gnupg2 fail on x86_64) using Obsoletes
  to avoid Epoch or other ugly means.

* Mon Aug  8 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.12-1
- 0.9.12
- --disable-static

* Thu Apr 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0.9.11-1
- 0.9.11
- drop upstreamed acquote patch

* Thu Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0.9.9-2
- rebuilt

* Tue Feb  1 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 0:0.9.9-1
- Minus BR libtool, add epoch to -devel req, fix underquoted ksba.m4.

* Fri Oct 22 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.9.9-0.fdr.2
- remove hard-coded .gz from %%post/%%postun
- add %%check section

* Tue Oct 19 2004 Rex Dieter <rexdieter[AT]users.sf.net> 0:0.9.9-0.fdr.1
- 0.9.9

* Thu Mar 20 2003 Ville Skyttä <ville.skytta@iki.fi> - 0.4.7-0.fdr.1
- Update to 0.4.7, and to current Fedora guidelines.
- Exclude %%{_libdir}/*.la.

* Wed Feb 12 2003 Warren Togami <warren@togami.com> 0.4.6-1.fedora.3
- temporary workaround to lib/dir conflict problem

* Sat Feb  8 2003 Ville Skyttä <ville.skytta@iki.fi> - 0.4.6-1.fedora.1
- First Fedora release.
