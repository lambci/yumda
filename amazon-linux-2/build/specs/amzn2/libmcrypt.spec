Name:		libmcrypt
Version:	2.5.8
Release: 24%{?dist}.0.2
License:	LGPLv2+
Group:		System Environment/Libraries
Summary:	Encryption algorithms library
URL:		http://mcrypt.sourceforge.net/
Source0:	http://downloads.sourceforge.net/mcrypt/libmcrypt-%{version}.tar.gz
Patch0:		libmcrypt-2.5.8-nolibltdl.patch
# Upstream:
# http://sourceforge.net/tracker/index.php?func=detail&aid=1872801&group_id=87941&atid=584895
Patch1:		libmcrypt-2.5.8-uninitialized.patch
# Upstream:
# http://sourceforge.net/tracker/index.php?func=detail&aid=1872799&group_id=87941&atid=584895
Patch2:		libmcrypt-2.5.8-prototypes.patch
BuildRequires:	libtool-ltdl-devel
BuildRequires:	gcc-c++

%description
Libmcrypt is a thread-safe library providing a uniform interface
to access several block and stream encryption algorithms.

%package devel
Group:		Development/Libraries
Summary:	Development libraries and headers for libmcrypt
Requires:	%{name} = %{version}-%{release}

%description devel
Development libraries and headers for use in building applications that
use libmcrypt.

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .uninitialized
%patch2 -p1 -b .prototypes

%build
%configure
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT -type f -name '*.la' -exec rm -f {} \;

# Multilib fix
sed -i 's|-L%{_libdir}||g' $RPM_BUILD_ROOT%{_bindir}/libmcrypt-config
touch -r NEWS $RPM_BUILD_ROOT%{_bindir}/libmcrypt-config

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%doc AUTHORS COPYING.LIB ChangeLog KNOWN-BUGS README NEWS THANKS TODO
%{_libdir}/*.so.*
%{_mandir}/man3/*

%files devel
%doc doc/README.key doc/README.xtea doc/example.c
%{_bindir}/libmcrypt-config
%{_includedir}/mutils/
%{_includedir}/mcrypt.h
%{_libdir}/*.so
%{_datadir}/aclocal/libmcrypt.m4

%changelog
* Mon Jul 23 2018 Tom Callaway <spot@fedoraproject.org> - 2.5.8-24
- add BuildRequires: gcc-c++

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-22
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-21
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.8-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.8-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jan  5 2009 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.8-7
- fix multilib conflict (bz 478879)

* Tue Aug 26 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.5.8-6
- apply minor cleanups from upstream

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.5.8-5
- Autorebuild for GCC 4.3

* Mon Oct 29 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.8-4
- multilib fix (bz 342221)

* Tue Oct  9 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.8-3
- get rid of the static lib, causes failures (bz 278671)

* Thu Aug 23 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.8-2
- fix license tag (v2+), rebuild for ppc32

* Thu Jul 19 2007 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.8-1
- bump to 2.5.8
- proper quoting fixed upstream, patch1 obsolete

* Sun Oct  8 2006 Ed Hill <ed@eh3.com> 2.5.7-5
- bz 209913 : libmcrypt.m4 in -devel and properly quote it

* Tue Sep 12 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-4
- bump for FC-6

* Tue Feb 28 2006 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-3
- bump for FC-5

* Wed Sep 28 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-2
- fix for FC-3

* Thu Sep 22 2005 Tom "spot" Callaway <tcallawa@redhat.com> 2.5.7-1
- initial package for Fedora Extras
