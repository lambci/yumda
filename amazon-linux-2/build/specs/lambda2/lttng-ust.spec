Name:           lttng-ust
Version:        2.4.1
Release:        4%{?dist}
License:        LGPLv2 and GPLv2 and MIT
Group:          Development/Libraries
Summary:        LTTng Userspace Tracer library
URL:            http://lttng.org/ust/
Source0:        http://lttng.org/files/lttng-ust/%{name}-%{version}.tar.bz2
Patch0:         lttng-ust-aarch64-aligned-access.patch

BuildRequires:  libuuid-devel texinfo systemtap-sdt-devel libtool
BuildRequires:  userspace-rcu-devel >= 0.7.2
BuildRequires:  libtool autoconf automake
ExcludeArch:    ppc64le

Prefix: %{_prefix}

%description
This library may be used by user space applications to generate 
tracepoints using LTTng.

%prep
%setup -q
%patch0 -p1 -b .aarch64

%build
%ifarch s390 s390x
# workaround rhbz#837572 (ICE in gcc)
%global optflags %(echo %{optflags} | sed 's/-O2/-O1/')
%endif

#Reinitialize libtool with the fedora version to remove Rpath
libtoolize -cvfi
autoreconf -vif
%configure --disable-static --with-sdt
# --with-java-jdk
# Java support was disabled in lttng-ust's stable-2.0 branch upstream in
# http://git.lttng.org/?p=lttng-ust.git;a=commit;h=655a0d112540df3001f9823cd3b331b8254eb2aa
# We can revisit enabling this when the next major version is released.

make %{?_smp_mflags} V=1

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}%{_libdir}/*.la

%files
%license README
%{_libdir}/*.so.*

%exclude %{_bindir}/lttng-gen-tp
%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_docdir}

%changelog
* Mon Aug 17 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Oct 28 2016 d.marlin <d.marlin@fedoraproject.org> 2.4.1-4
- bump release to avoid conflict with Fedora builds

* Fri Oct 28 2016 d.marlin <d.marlin@fedoraproject.org>
- Backport patch from Fedora lttng-ust-2.5.1-2 to fix aarch64 alignment

* Tue May 20 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.4.1-1
- New upstream bugfix release

* Sat Mar 1 2014 Suchakra Sharma <suchakra@fedoraproject.org> - 2.4.0-1
- New upstream release
- Add new files (man and doc)

* Sat Feb 22 2014 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-2
- Rebuilt for URCU Soname change

* Fri Sep 20 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.3.0-1
- New upstream release (include snapshop feature)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.2.1-1
- New upstream release
- Bump URCU dependency

* Thu May 23 2013 Dan Horák <dan[at]danny.cz> - 2.1.2-2
- add build workaround for s390(x)

* Fri May 17 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.2-1
- New upstream bugfix release
- Remove patches applied upstream

* Wed Feb 27 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-2
- Remove dependency of probes on urcu-bp

* Tue Feb 26 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.1.1-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.5-1
- New upstream release

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-2
- Add dependency on systemtap-sdt-devel for devel package

* Tue Jun 19 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.4-1
- New upstream release
- Updates from review comments
* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 2.0.3-1
- New package, inspired by the one from OpenSuse

