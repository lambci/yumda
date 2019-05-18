Summary: A library for password generation and password quality checking
Name: libpwquality
Version: 1.2.3
Release: 5%{?dist}
# The package is BSD licensed with option to relicense as GPLv2+
# - this option is redundant as the BSD license allows that anyway.
License: BSD or GPLv2+
Group: System Environment/Base
Source0: https://github.com/libpwquality/libpwquality/releases/download/libpwquality-%{version}/libpwquality-%{version}.tar.bz2
Patch1: libpwquality-1.2.3-translation-updates.patch
Patch2: libpwquality-1.2.3-generate-buf.patch
Patch3: libpwquality-1.2.3-settings.patch

Requires: cracklib-dicts >= 2.8
Requires: pam%{?_isa}
BuildRequires: cracklib-devel
BuildRequires: gettext
BuildRequires: pam-devel
BuildRequires: python2-devel

URL: https://github.com/libpwquality/libpwquality/

# we don't want to provide private python extension libs
%define __provides_exclude_from ^%{python_sitearch}/.*\.so$.

Prefix: %{_prefix}

%description
This is a library for password quality checks and generation
of random passwords that pass the checks.
This library uses the cracklib and cracklib dictionaries
to perform some of the checks.

%prep
%setup -q
%patch1 -p2 -b .translations
%patch2 -p1 -b .generate-buf
%patch3 -p1 -b .settings

%build
%configure \
	--with-securedir=%{_libdir}/security \
  --disable-python-bindings \
	--disable-static

make -C po update-gmo
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%files
%defattr(-,root,root,-)
%license COPYING
%{_bindir}/pwmake
%{_bindir}/pwscore
%{_libdir}/security/pam_pwquality.so
%{_libdir}/libpwquality.so.*
%config(noreplace) %{_sysconfdir}/security/pwquality.conf

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/security/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Nov 15 2017 Tomáš Mráz <tmraz@redhat.com> 1.2.3-5
- fix brittle configuration settings (#1259633)
- fix abort when generating large passwords on some architectures

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.2.3-4
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.2.3-3
- Mass rebuild 2013-12-27

* Fri Nov 29 2013 Tomáš Mráz <tmraz@redhat.com> 1.2.3-2
- translation updates

* Thu Sep 12 2013 Tomáš Mráz <tmraz@redhat.com> 1.2.3-1
- fix problem with parsing the pam_pwquality options
  patch by Vladimir Sorokin.
- updated translations from Transifex
- treat empty user or password as NULL
- move the library to /usr

* Wed Jun 19 2013 Tomas Mraz <tmraz@redhat.com> 1.2.2-1
- manual page fixes
- make it possible to set the maxsequence configuration value
- updated translations from Transifex

* Thu Dec 20 2012 Tomas Mraz <tmraz@redhat.com> 1.2.1-1
- properly free pwquality settings
- add extern "C" to public header
- updated translations from Transifex

* Thu Aug 16 2012 Tomas Mraz <tmraz@redhat.com> 1.2.0-1
- add maxsequence check for too long monotonic character sequence.
- clarified alternative licensing to GPLv2+.
- add local_users_only option to skip the pwquality checks for
  non-locals. (thanks to Stef Walter)

* Wed Jun 13 2012 Tomas Mraz <tmraz@redhat.com> 1.1.1-1
- use rpm built-in filtering of provides (rhbz#830153)
- remove strain debug fprintf() (rhbz#831567)

* Thu May 24 2012 Tomas Mraz <tmraz@redhat.com> 1.1.0-1
- fix leak when throwing PWQError exception
- added pkgconfig file
- call the simplicity checks before the cracklib check
- add enforce_for_root option to the PAM module
- updated translations from Transifex

* Thu Dec  8 2011 Tomas Mraz <tmraz@redhat.com> 1.0.0-1
- added a few additional password quality checks
- bugfix in configuration file parsing

* Fri Nov 11 2011 Tomas Mraz <tmraz@redhat.com> 0.9.9-1
- added python bindings and documentation

* Mon Oct 10 2011 Tomas Mraz <tmraz@redhat.com> 0.9-2
- fixes for problems found in review (missing BR on pam-devel,
  License field, Source URL, Require pam, other cleanups)

* Mon Oct  3 2011 Tomas Mraz <tmraz@redhat.com> 0.9-1
- first spec file for libpwquality
