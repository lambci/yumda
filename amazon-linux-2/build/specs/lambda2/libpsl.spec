Name:           libpsl
Version:        0.7.0
Release:        1%{?dist}
Summary:        C library for the Publix Suffix List
License:        MIT
URL:            https://rockdaboot.github.io/libpsl
Source0:        https://github.com/rockdaboot/libpsl/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel
BuildRequires:  gtk-doc
BuildRequires:  libicu-devel
BuildRequires:  libtool
BuildRequires:  libxslt

Prefix: %{_prefix}

%description
libpsl is a C library to handle the Public Suffix List. A "public suffix" is a
domain name under which Internet users can directly register own names.

Browsers and other web clients can use it to

- Avoid privacy-leaking "supercookies";
- Avoid privacy-leaking "super domain" certificates;
- Domain highlighting parts of the domain in a user interface;
- Sorting domain lists by site;

Libpsl...

- has built-in PSL data for fast access;
- allows to load PSL data from files;
- checks if a given domain is a "public suffix";
- provides immediate cookie domain verification;
- finds the longest public part of a given domain;
- finds the shortest private part of a given domain;
- works with international domains (UTF-8 and IDNA2008 Punycode);
- is thread-safe;
- handles IDNA2008 UTS#46;

%package -n     psl
Summary:        Commandline utility to explore the Public Suffix List

%description -n psl
This package contains a commandline utility to explore the Public Suffix List,
for example it checks if domains are public suffixes, checks if cookie-domain
is acceptable for domains and so on.

%prep
%setup -q

%build
[ -f configure ] || autoreconf -fiv
%configure --disable-silent-rules \
           --disable-static       \
           --disable-man           \
           --disable-gtk-doc

make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name '*.la' -delete -print

%files
%license COPYING
%{_libdir}/libpsl.so.*

%files -n psl
%license COPYING
%{_bindir}/psl

%exclude %{_datadir}
%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Thu Oct 31 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Feb 02 2015 Christopher Meng <rpm@cicku.me> - 0.7.0-1
- Update to 0.7.0

* Thu Nov 20 2014 Christopher Meng <rpm@cicku.me> - 0.6.2-1
- Update to 0.6.2

* Tue Aug 26 2014 David Tardon <dtardon@redhat.com> - 0.5.1-3
- rebuild for ICU 53.1

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Aug 04 2014 Christopher Meng <rpm@cicku.me> - 0.5.1-1
- Update to 0.5.1
- Drop patch merged upstream

* Sat Aug 02 2014 Christopher Meng <rpm@cicku.me> - 0.5.0-3
- Add a patch from Jakub Čajka to complete the tests on non-x86 arch.

* Thu Jul 24 2014 Christopher Meng <rpm@cicku.me> - 0.5.0-2
- Drop useless test data
- Add missing gettext-devel
- psl is now separately packaged recommended by the upstream

* Fri Jul 04 2014 Christopher Meng <rpm@cicku.me> - 0.5.0-1
- Update to 0.5.0

* Tue Jul 01 2014 Christopher Meng <rpm@cicku.me> - 0.4.0-1
- Update to 0.4.0

* Tue Apr 08 2014 Christopher Meng <rpm@cicku.me> - 0.2-1
- Initial Package.
