Name:           graphite2
Version:        1.3.10
Release: 1%{?dist}.0.2
Summary:        Font rendering capabilities for complex non-Roman writing systems
Group:          Development/Tools

License:        (LGPLv2+ or GPLv2+ or MPL) and (Netscape or GPLv2+ or LGPLv2+)
URL:            https://sourceforge.net/projects/silgraphite/
Source0:        https://downloads.sourceforge.net/project/silgraphite/graphite2//%{name}-%{version}.tgz
Patch0:         graphite-arm-nodefaultlibs.patch
Patch1:         graphite2-1.2.0-cmakepath.patch

BuildRequires:  cmake
BuildRequires:  freetype-devel
BuildRequires:  doxygen asciidoc
BuildRequires:  texlive-helvetic texlive-sectsty texlive-tocloft texlive-xtab texlive-multirow fonttools

Obsoletes:      silgraphite < 2.3.1-5

Prefix: %{_prefix}

%description
Graphite2 is a project within SIL’s Non-Roman Script Initiative and Language
Software Development groups to provide rendering capabilities for complex
non-Roman writing systems. Graphite can be used to create “smart fonts” capable
of displaying writing systems with various complex behaviors. With respect to
the Text Encoding Model, Graphite handles the "Rendering" aspect of writing
system implementation.

%prep
%setup -q
%patch0 -p1 -b .arm
%patch1 -p1 -b .cmake

%build
%cmake -DGRAPHITE2_COMPARE_RENDERER=OFF  .
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%license LICENSE COPYING
%{_bindir}/gr2fonttest
%{_libdir}/libgraphite2.so.3
%{_libdir}/libgraphite2.so.3.0.1

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%exclude %{_libdir}/%{name}
%exclude %{_libdir}/pkgconfig

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Feb 29 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.10-1
- Resolves: rhbz#1472290
  CVE-2017-7771 CVE-2017-7772 CVE-2017-7773 CVE-2017-7774
  CVE-2017-7775 CVE-2017-7776 CVE-2017-7777 CVE-2017-7778

* Mon Feb 29 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.6-1
- Related: rhbz#1309053 CVE-2016-1521 CVE-2016-1522 CVE-2016-1523 CVE-2016-1526

* Wed Feb 17 2016 Caolán McNamara <caolanm@redhat.com> - 1.3.5-1
- Resolves: rhbz#1309053 CVE-2016-1521 CVE-2016-1522 CVE-2016-1523 CVE-2016-1526

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.4-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sat Feb 21 2015 Till Maas <opensource@till.name> - 1.2.4-4
- Rebuilt for Fedora 23 Change
  https://fedoraproject.org/wiki/Changes/Harden_all_packages_with_position-independent_code

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 03 2014 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.4-1
- New upstream release

* Sat Dec 21 2013 Ville Skyttä <ville.skytta@iki.fi> - 1.2.2-5
- Move *.so.major symlink to main package.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Jun 24 2013 Caolán McNamara <caolanm@redhat.com> - 1.2.2-3
- clarify licenses

* Wed Jun 19 2013 Karsten Hopp <karsten@redhat.com> 1.2.2-2
- use minimum texlive buildrequires, Than Ngo, rhbz#975843 

* Thu May 30 2013 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.2-1
- New upstream release

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-4
- Drop refman.pdf as its same as manual.html
- patch install path for cmake files as they are arch dependent

* Tue Jan 29 2013 Kalev Lember <kalevlember@gmail.com> - 1.2.0-3
- Move manual.html to -devel subpackage

* Tue Jan 29 2013 Parag Nemade <paragn AT fedoraproject DOT org> - 1.2.0-2
- revert the wrongly committed f18 spec to f19
- spec file cleanup
- thanks to jnovy for finding me minimum texlive BR
- partial multilib fix for manual.html

* Fri Nov 9 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.2.0-1
- New upstream release
* Wed Oct 3 2012 Caolán McNamara <caolanm@redhat.com> - 1.1.1-4
- expand license field to cover tri-licenced GrUtfTextSrc test
* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild
* Tue Apr  3 2012 Peter Robinson <pbrobinson@fedoraproject.org> - 1.1.1-2
- Fix FTBFS on ARM
* Mon Feb 27 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.1-1
- New upstream release
* Wed Feb 8 2012 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.1.0-1
- New upstream release
* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild
* Fri Sep 23 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.3-1
- New upstream release
* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-3
- Obsolete silgraphite
* Fri Aug 26 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-2
- Removed dependency on silgraphite-devel
- Stopped building comparerenderer - the only thing that depended on silgraphite
* Fri Aug 19 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.2-1
- Rebase to new release
- SPEC Cleanup
- Documentation is now properly installed
* Wed Aug 17 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-2
- Added some necessary requires
* Wed Aug 10 2011 Nicholas van Oudtshoorn <vanoudt@gmail.com> - 1.0.1-1
- Initial build of graphite2
