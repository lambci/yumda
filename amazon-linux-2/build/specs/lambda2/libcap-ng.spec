%define _trivial .0
%define _buildid .4

%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: An alternate posix capabilities library
Name: libcap-ng
Version: 0.7.5
Release: 4%{?dist}%{?_trivial}%{?_buildid}
License: LGPLv2+
Group: System Environment/Libraries
URL: http://people.redhat.com/sgrubb/libcap-ng
Source0: http://people.redhat.com/sgrubb/libcap-ng/%{name}-%{version}.tar.gz
Patch1: libcap-ng-test-fixup.patch
Patch2: libcap-ng-leak.patch
Patch3: libcap-ng-thread-test.patch
Patch4: libcap-ng-pacct-typo.patch

# Amazon's patches 
Patch10001: 0001-Detect-and-output-a-couple-errors-in-filecap.patch 
Patch10002: 0002-fixup-makefile.in.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: kernel-headers >= 2.6.11

Prefix: %{_prefix}

%description
Libcap-ng is a library that makes using posix capabilities easier

%package python
Summary: Python bindings for libcap-ng library
License: LGPLv2+
Group: Development/Libraries
BuildRequires: python-devel swig
Requires: %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description python
The libcap-ng-python package contains the bindings so that libcap-ng
and can be used by python applications.

%package utils
Summary: Utilities for analyzing and setting file capabilities
License: GPLv2+
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Prefix: %{_prefix}

%description utils
The libcap-ng-utils package contains applications to analyze the
posix capabilities of all the program running on a system. It also
lets you set the file system based capabilities.

%prep
%setup -q
%patch1 -p0
%patch2 -p0
%patch3 -p2
%patch4 -p2
%patch10001 -p1
%patch10002 -p1

%build
%configure \
  --libdir=%{_libdir} \
  --disable-static \
  am_cv_python_pythondir=%{python_sitelib} \
  am_cv_python_pyexecdir=%{python_sitearch}
make %{?_smp_mflags}

%install
make DESTDIR="${RPM_BUILD_ROOT}" install

%files
%defattr(-,root,root,-)
%license COPYING.LIB
%attr(0755,root,root) %{_libdir}/libcap-ng.so.*

%files python
%defattr(-,root,root,-)
%attr(755,root,root) %{python_sitearch}/_capng.so
%{python_sitearch}/capng.py*
%{python_sitearch}/__pycache__/*

%files utils
%defattr(-,root,root,-)
%license COPYING
%attr(0755,root,root) %{_bindir}/*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_datadir}
%exclude %{_libdir}
%exclude %{python_sitearch}

%changelog
* Tue Jul 9 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Jun 06 2019 Jeremiah Mahler <jmmahler@amazon.com> 0.7.5-4.amzn2.0.4
- Fixup Makefile.in so it works with automake 1.13
- Fix pthread_atfork causing segfaults

* Fri Aug 14 2015 Steve Grubb <sgrubb@redhat.com> 0.7.5-4
- resolves: #1253220 - captest list sys_psacct instead of sys_pacct

* Tue Aug 11 2015 Steve Grubb <sgrubb@redhat.com> 0.7.5-3
- resolves: #1185610 - libcap-ng: update caps table for newer kernels
- Fix thread test

* Wed May 13 2015 Steve Grubb <sgrubb@redhat.com> 0.7.5-2
- resolves: #1185610 - libcap-ng: update caps table for newer kernels
- Fix a leaked FD in upstream code

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.7.3-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.7.3-4
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 19 2012 Steve Grubb <sgrubb@redhat.com> 0.7.3-2
- Remove useless code in pscap causing EBADFD

* Fri Nov 09 2012 Steve Grubb <sgrubb@redhat.com> 0.7.3-1
- New upstream release

* Wed Oct 24 2012 Steve Grubb <sgrubb@redhat.com> 0.7.1-1
- New upstream release

* Tue Jul 24 2012 Steve Grubb <sgrubb@redhat.com> 0.7-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> 0.6.6-1
- New upstream release

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Nov 03 2010 Steve Grubb <sgrubb@redhat.com> 0.6.5-1
- New upstream release fixing 2.6.36 kernel header issue

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 0.6.4-4
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu Jun 17 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-3
- Only open regular files in filecap

* Mon May 24 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-2
- In utils subpackage added a requires statement.

* Thu May 06 2010 Steve Grubb <sgrubb@redhat.com> 0.6.4-1
- New upstream release fixing multi-threading issue

* Wed Apr 28 2010 Steve Grubb <sgrubb@redhat.com> 0.6.3-2
- filecap shows full capabilities if a file has any

* Thu Mar 11 2010 Steve Grubb <sgrubb@redhat.com> 0.6.3-1
- New upstream release

* Tue Feb 16 2010 Steve Grubb <sgrubb@redhat.com> 0.6.2-4
- Use global macro and require pkgconfig for devel subpackage

* Fri Oct 09 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-3
- Apply patch to retain setpcap only if clearing bounding set

* Sat Oct 03 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-2
- Apply patch correcting pscap and netcap acct detection

* Mon Sep 28 2009 Steve Grubb <sgrubb@redhat.com> 0.6.2-1
- New upstream release

* Sun Jul 26 2009 Steve Grubb <sgrubb@redhat.com> 0.6.1-1
- New upstream release

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Jun 29 2009 Steve Grubb <sgrubb@redhat.com> 0.6-1
- New upstream release

* Sun Jun 21 2009 Steve Grubb <sgrubb@redhat.com> 0.5.1-1
- New upstream release

* Fri Jun 19 2009 Steve Grubb <sgrubb@redhat.com> 0.5-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.2-1
- New upstream release

* Fri Jun 12 2009 Steve Grubb <sgrubb@redhat.com> 0.4.1-1
- Initial build.

