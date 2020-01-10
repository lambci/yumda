%define _trivial .0
%define _buildid .3

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
#Patch2:		0101-onig_new_deluxe-don-t-free-new-pattern-if-success.patch

BuildRequires:	ruby >= 1.8
BuildRequires:	gcc

# upstream patches
# #1728966 CVE-2019-13225
#Patch10:	0010-Fix-CVE-2019-13225-problem-in-converting-if-then-els.patch
# #1768997 CVE-2019-16163
Patch12:	oniguruma-CVE-2019-16163.patch
# #1728971 d3e402928b6eb3327f8f7d59a9edfa622fec557b
Patch13:	oniguruma-d3e4029-bz1755880.patch
# #1728971 15c4228aa2ffa02140a99912dd3177df0b1841c6
Patch14:	oniguruma-15c4228-bz1755880_2.patch
# #1755880 CVE-2019-13224
#Patch11:	0011-Fix-CVE-2019-13224-don-t-allow-different-encodings-f.patch
# Not use Patch11 for F-30 and below, this is almost API change (deprecation of API) in 
# onig_new_deluxe() and this change should be avoided (if possible) in stable
# branch
# Instead use another fix
Patch101:	0101-onig_new_deluxe-don-t-free-new-pattern-if-success.patch

Patch1001: 1001-CVE-2019-19012.patch
Patch1002: 1002-CVE-2019-19204.patch

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
#%patch2 -p1 -b .nullreg2
%{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in

#%patch10 -p1 -b .CVE-2019-13225
#%%patch11 -p1 -b .CVE-2019-13224
%patch101 -p1 -b .CVE-2019-13224
%patch12 -p1 -b .CVE-2019-16163
%patch13 -p1 -b .bz1755880_1
%patch14 -p1 -b .bz1755880_2

%patch1001 -p1 -b .CVE-2019-19012
%patch1002 -p1 -b .CVE-2019-19204

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
* Fri Jan 10 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Dec 5 2019 <emmlep@amazon.com> - 5.9.6-1-amzn2.0.3
- Fix CVE-2019-19204 and CVE-2019-19012
 * Fri Nov 29 2019 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.6-2
- 6.9.4 rc3 (CVE-2019-19204 CVE-2019-19203 CVE-2019-19012)
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

