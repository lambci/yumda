%if 0%{?python3_other_pkgversion}
%bcond_without python3_other
%else
%bcond_with python3_other
%endif

%global major                   28
%global cppmajor                12

Name:           libprelude
Version:        5.2.0
Release:        2%{?dist}
Summary:        Secure Connections between all Sensors and the Prelude Manager
License:        LGPL-2.1+
Group:          System Environment/Libraries
URL:            https://www.prelude-siem.org/
Source0:        https://www.prelude-siem.org/pkg/src/%{version}/%{name}-%{version}.tar.gz
# https://www.prelude-siem.org/issues/859
Patch0:         libprelude-5.2.0-linking.patch
# https://www.prelude-siem.org/issues/860
Patch1:         libprelude-5.2.0-ruby_vendorarchdir.patch
# https://www.prelude-siem.org/issues/863
Patch2:         libprelude-5.2.0-fsf_address.patch
# https://www.prelude-siem.org/issues/865
Patch3:         libprelude-5.2.0-fix_timegm.patch
# https://www.prelude-siem.org/issues/885
Patch4:         libprelude-5.2.0-fix_pthread_atfork.patch
# https://www.prelude-siem.org/issues/887
Patch5:         libprelude-5.2.0-fix_prelude_tests_timer.patch
Patch6:         libprelude-5.2.0-fix_gtkdoc_1.32.patch
Patch7:         libprelude-5.2.0-clean_libprelude-config.patch
BuildRequires:  bison
BuildRequires:  chrpath
BuildRequires:  flex
BuildRequires:  gtk-doc
BuildRequires:  swig
BuildRequires:  libgpg-error-devel
BuildRequires:  libtool-ltdl-devel
BuildRequires:  perl-devel
BuildRequires:  perl-generators
BuildRequires:  python2-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  pkgconfig(gnutls)
BuildRequires:  pkgconfig(lua) >= 5.1
BuildRequires:  ruby-devel
BuildRequires:  pkgconfig(zlib)

%ifnarch s390 ppc64 ppc64le
BuildRequires:  valgrind
%endif

# Upstream do not use explicit version of gnulib, just checkout
# and update files. In libprelude 5.2.0, the checkout has been done
# on 2018-09-03
Provides:       bundled(gnulib) = 20180903

%description
Libprelude is a collection of generic functions providing communication
between all Sensors, like IDS (Intrusion Detection System), and the Prelude
Manager. It provides a convenient interface for sending and receiving IDMEF
(Information and Event Message Exchange Format) alerts to Prelude Manager with
transparent SSL, fail-over and replication support, asynchronous events and
timer interfaces, an abstracted configuration API (hooking at the command-line,
the configuration line, or wide configuration, available from the Manager), and
a generic plugin API. It allows you to easily turn your favorite security
program into a Prelude sensor.

%package devel
Summary:        Libraries and headers for developing Prelude sensors
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       libtool-ltdl-devel
Provides:       %{name}%{?_isa}-devel = %{version}-%{release}
Provides:       prelude-devel = %{version}-%{release}

%description devel
Libraries and headers you can use to develop Prelude sensors using the Prelude
Library. Libprelude is a collection of generic functions providing
communication between all Sensors, like IDS (Intrusion Detection System),
and the Prelude Manager. It provides a convenient interface for sending and
receiving IDMEF (Information and Event Message Exchange Format) alerts to
Prelude Manager with transparent SSL, fail-over and replication support,
asynchronous events and timer interfaces, an abstracted configuration API
(hooking at the command-line, the configuration line, or wide configuration,
available from the Manager), and a generic plugin API. It allows you to easily
turn your favorite security program into a Prelude sensor.

%package -n prelude-tools
Summary:        Command-line tools for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n prelude-tools
Provides a convenient interface for sending alerts to Prelude
Manager.

%package -n python2-prelude
Summary:        Python 2 bindings for prelude
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python2-prelude}

%description -n python2-prelude
Provides python 2 bindings for prelude.

%package -n python%{python3_pkgversion}-prelude
Summary:        Python 3 bindings for prelude
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_pkgversion}-prelude}

%description -n python%{python3_pkgversion}-prelude
Provides python 3 bindings for prelude.

%if 0%{?with_python3_other}
%package -n python%{python3_other_pkgversion}-prelude
Summary:        Python 3 bindings for prelude
BuildRequires:  python%{python3_other_pkgversion}-devel
BuildRequires:  python%{python3_other_pkgversion}-setuptools
Requires:       %{name}%{?_isa} = %{version}-%{release}
%{?python_provide:%python_provide python%{python3_other_pkgversion}-prelude}
 
%description -n python%{python3_other_pkgversion}-prelude
Provides python 3 bindings for prelude.
# with_python3_other
%endif

%package -n perl-prelude
Summary:        Perl bindings for prelude
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-prelude
Provides perl bindings for prelude.

%package -n ruby-prelude
Summary:        Ruby bindings for prelude
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description -n ruby-prelude
Provides ruby bindings for prelude.

%package -n lua-prelude
Summary:        Lua bindings for prelude
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       lua

%description -n lua-prelude
Provides Lua bindings for prelude generated by SWIG.

%package doc
Summary:        Documentation for prelude
BuildArch:      noarch

%description doc
Provides documentation for prelude generated by gtk-doc.

%prep
%autosetup -p1

%build
%configure \
    --without-included-ltdl \
    --disable-static \
    --enable-shared \
    --with-swig \
    --with-python2 \
    --with-python3 \
    --with-ruby \
    --with-lua \
    --with-perl-installdirs=vendor \
    --without-included-regex \
    --includedir=%{_includedir}/%{name} \
    --enable-gtk-doc \
    --with-html-dir=%{_docdir}/%{name}-devel
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
%make_build
cd %{_builddir}/%{name}-%{version}/bindings/python
%{?with_python3_other: %py3_other_build}

%install
%make_install
cd %{_builddir}/%{name}-%{version}/bindings/python
%{?with_python3_other: %py3_other_install}

chrpath -d %{buildroot}%{_libdir}/*.so.*

find %{buildroot} -name '*.la' -delete
find %{buildroot} -name 'perllocal.pod' -delete
find %{buildroot} -name '.packlist' -delete

%check
make check

%post -n %{name} -p /sbin/ldconfig
%postun -n %{name} -p /sbin/ldconfig

%files
%{_libdir}/%{name}.so.%{major}
%{_libdir}/%{name}.so.%{major}.*
%{_libdir}/%{name}cpp.so.%{cppmajor}
%{_libdir}/%{name}cpp.so.%{cppmajor}.*
%license COPYING LICENSE.README HACKING.README
%doc AUTHORS README NEWS

%files devel
%{_datadir}/%{name}
%{_bindir}/%{name}-config
%{_libdir}/%{name}.so
%{_libdir}/%{name}cpp.so
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/%{name}
%{_datadir}/aclocal/%{name}.m4
%{_mandir}/man1/%{name}-config.1.gz

%files -n prelude-tools
# Force default attrs because libprelude force others
%defattr(- , root, root, 755)
%{_bindir}/prelude-adduser
%{_bindir}/prelude-admin
%{_mandir}/man1/prelude-admin.1.gz
%dir %{_sysconfdir}/prelude
%dir %{_sysconfdir}/prelude/default
%dir %{_sysconfdir}/prelude/profile
%config(noreplace) %{_sysconfdir}/prelude/default/client.conf
%config(noreplace) %{_sysconfdir}/prelude/default/global.conf
%config(noreplace) %{_sysconfdir}/prelude/default/idmef-client.conf
%config(noreplace) %{_sysconfdir}/prelude/default/tls.conf
%dir %{_var}/spool/prelude

%files -n python2-prelude
%{python2_sitearch}/_prelude.*so
%{python2_sitearch}/prelude-%{version}-py?.?.egg-info
%{python2_sitearch}/prelude.py
%{python2_sitearch}/prelude.pyc
%{python2_sitearch}/prelude.pyo

%files -n python%{python3_pkgversion}-prelude
%{python3_sitearch}/_prelude.*so
%{python3_sitearch}/__pycache__/prelude.cpython-??.*pyc
%{python3_sitearch}/prelude-%{version}-py?.?.egg-info
%{python3_sitearch}/prelude.py

%if 0%{?with_python3_other}
%files -n python%{python3_other_pkgversion}-prelude
%{python3_other_sitearch}/_prelude.*so
%{python3_other_sitearch}/__pycache__/prelude.cpython-??.*pyc
%{python3_other_sitearch}/__pycache__/prelude.cpython-??.*pyo
%{python3_other_sitearch}/prelude-%{version}-py?.?.egg-info
%{python3_other_sitearch}/prelude.py
# with_python3_other
%endif

%files -n perl-prelude
%{perl_vendorarch}/Prelude.pm
%dir %{perl_vendorarch}/auto/Prelude
# Force attrs because libprelude set it to 555
%attr(755, root, root) %{perl_vendorarch}/auto/Prelude/Prelude.so
%attr(755, root, root) %{perl_vendorarch}/auto/Prelude/Prelude.bs

%files -n ruby-prelude
%{ruby_vendorarchdir}/Prelude.so

%files -n lua-prelude
%{_libdir}/lua/*/prelude.so

%files doc
%{_docdir}/%{name}-devel
%license COPYING LICENSE.README HACKING.README
%doc AUTHORS ChangeLog README NEWS

%changelog
* Fri Sep 18 2020 Thomas Andrejak <thomas.andrejak@gmail.com> - 5.2.0-2
- Clean libprelude-config

* Thu Sep 17 2020 Thomas Andrejak <thomas.andrejak@gmail.com> - 5.2.0-1
- Bump version 5.2.0

* Mon Apr 06 2020 Thomas Andrejak <thomas.andrejak@gmail.com> - 5.1.1-1
- Bump version 5.1.1

* Sun Jul 14 2019 Thomas Andrejak <thomas.andrejak@gmail.com> - 5.0.0-1
- Bump version 5.0.0

* Thu Mar 07 2019 Troy Dawson <tdawson@redhat.com> - 4.1.0-3
- Rebuilt to change main python from 3.4 to 3.6

* Fri May 11 2018 Thomas Andrejak <thomas.andrejak@gmail.com> - 4.1.0-2
- Rebuild with right sources

* Sat Mar 10 2018 Thomas Andrejak <thomas.andrejak@gmail.com> - 4.1.0-1
- Bump version 4.1.0

* Sat Sep 16 2017 Thomas Andrejak <thomas.andrejak@gmail.com> - 4.0.0-1
- Bump version 4.0.0

* Thu Feb 02 2017 Thomas Andrejak <thomas.andrejak@gmail.com> - 3.1.0-27
- Fix GnuTLS patch

* Wed Oct 19 2016 Thomas Andrejak <thomas.andrejak@gmail.com> - 3.1.0-26
- Bump version

* Sun Mar 10 2013 Steve Grubb <sgrubb@redhat.com> - 1:1.0.0-17
- Rebuild with new gnutls

* Thu Sep 06 2012 Steve Grubb <sgrubb@redhat.com> - 1:1.0.0-16
- Add provides bundled gnulib

* Wed Aug 08 2012 Petr Pisar <ppisar@redhat.com> - 1:1.0.0-15
- Fix building with glibc-2.16.6 (bug #839602)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.0-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 07 2012 Petr Pisar <ppisar@redhat.com> - 1:1.0.0-13
- Perl 5.16 rebuild

* Tue Mar 13 2012 Steve Grubb <sgrubb@redhat.com> - 1:1.0.0-12
- Drop support for ruby

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.0-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Jul 19 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.0.0-10
- Perl mass rebuild

* Fri Jun 24 2011 Steve Grubb <sgrubb@redhat.com> - 1:1.0.0-9
- Fix gcc 4.6 C++ bug (#715983)

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.0.0-8
- Perl mass rebuild

* Thu Jun 09 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1:1.0.0-7
- Perl 5.14 mass rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1:1.0.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1:1.0.0-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Tue Jun 01 2010 Marcela Maslanova <mmaslano@redhat.com> - 1:1.0.0-4
- Mass rebuild with perl-5.12.0

* Sun May 02 2010 Steve Grubb <sgrubb@redhat.com> - 1.0.0-3
- Fix requires statements

* Fri Apr 30 2010 Steve Grubb <sgrubb@redhat.com> - 1.0.0-2
- New upstream release

* Sat Jan 30 2010 Steve Grubb <sgrubb@redhat.com> - 1.0.0rc1-1
- New upstream release
