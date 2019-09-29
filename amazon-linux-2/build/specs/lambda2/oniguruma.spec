%define _trivial .0
%define _buildid .1

Name:		oniguruma
Version:	5.9.6
Release:	1%{?dist}%{?_trivial}%{?_buildid}
Summary:	Regular expressions library

Group:		System Environment/Libraries
License:	BSD
URL:		http://www.geocities.jp/kosako3/oniguruma/
Source0:	http://www.geocities.jp/kosako3/oniguruma/archive/onig-%{version}.tar.gz
# FIXME
# Don't know exactly why, however without Patch0 onig_new returns
# NULL reg variable
Patch0:		oniguruma-5.9.2-onig_new-returns-NULL-reg.patch
Patch1:		0011-Fix-CVE-2019-13224-don-t-allow-different-encodings-f.patch
Patch2:		0101-onig_new_deluxe-don-t-free-new-pattern-if-success.patch

BuildRequires:	ruby >= 1.8

Prefix: %{_prefix}

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)


%prep
%setup -q -n onig-%{version}
%patch0 -p1 -b .nullreg
%patch1 -p1 -b .nullreg1
%patch2 -p1 -b .nullreg2
%{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in

%build
%configure \
	--disable-static \
	--with-rubydir=%{_bindir}
%{__make} %{?_smp_mflags}


%install
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -c -p"

%files
%defattr(-,root,root,-)
%license	COPYING
%{_libdir}/libonig.so.*

%exclude %{_bindir}/onig-config
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_includedir}
%exclude %{_libdir}/pkgconfig


%changelog
* Sun Sep 29 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Tue Aug  6 2019 <emmlep@amazon.com> - 5.9.6-1-amzn2.0.1
- Fixes CVE-2019-13224

* Fri Jan  2 2015 <mtasaka@fedoraproject.org> - 5.9.6-1
- 5.9.6

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.3-1
- 5.9.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 5.9.2-3
- F-17: rebuild against gcc47

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.2-1
- 5.9.2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-2
- F-11: Mass rebuild

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Thu Dec 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-1
- 5.9.1

* Wed Dec  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.0-1
- Initial packaging

