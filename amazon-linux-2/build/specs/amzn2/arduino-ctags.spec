%global         extraver        arduino11
Name:           arduino-ctags
Version:        5.8
Release:        8.%{extraver}%{?dist}
Summary:        A mix of ctags and anjuta-tags for the perfect C++ ctags

License:        GPLv2
URL:            http://arduino.cc
Source0:        https://github.com/arduino/ctags/archive/%{version}-%{extraver}.tar.gz#/ctags-%{version}-%{extraver}.tar.gz

# add support for DESTDIR in make install
Patch0:         ctags-5.7-destdir.patch
# https://github.com/arduino/ctags/issues/14
Patch1:         ctags-CVE-2014-7204.patch

BuildRequires:  gcc
%description
An Arduino fork of exuberant ctags

%prep
%autosetup -n ctags-%{version}-%{extraver}

# rename executable and man page
sed -i 's/^CTAGS_PROG =.*/CTAGS_PROG = arduino-ctags/' Makefile.in
sed -i 's/^MANPAGE =.*/MANPAGE = arduino-ctags.1/' Makefile.in

# remove glibc regex bundled copy to ensure it's not used
rm -r gnu_regex

%build
%configure
%make_build


%install
%make_install DESTDIR=%{buildroot}

%files
%license COPYING
%doc EXTENDING.html FAQ NEWS README
%{_bindir}/arduino-ctags
%{_mandir}/man1/arduino-ctags.1.gz


%changelog
* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-8.arduino11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-7.arduino11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-6.arduino11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.8-5.arduino11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Mon Mar  6 2017 Gianluca Sforna <giallu@gmail.com> 5.8-4.arduino11
- remove gnu_regex source directory

* Thu Mar  2 2017 Gianluca Sforna <giallu@gmail.com> 5.8-3.arduino11
* FHS conformant packaging

* Wed Feb 22 2017 Gianluca Sforna <giallu@gmail.com> 5.8-2.arduino11
- fix directory ownership

* Tue Feb 14 2017 Gianluca Sforna <giallu@gmail.com> 5.8-1.arduino11
- Initial release
