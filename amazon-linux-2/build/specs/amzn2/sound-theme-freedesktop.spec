Name: sound-theme-freedesktop
Version: 0.8
Release: 3%{?dist}
Summary: freedesktop.org sound theme
Group: User Interface/Desktops
Source0: http://people.freedesktop.org/~mccann/dist/sound-theme-freedesktop-%{version}.tar.bz2
# For details on the licenses used, see CREDITS
License: GPLv2+ and LGPLv2+ and CC-BY-SA and CC-BY
Url: http://www.freedesktop.org/wiki/Specifications/sound-theme-spec
BuildArch: noarch
BuildRequires: gettext
BuildRequires: intltool >= 0.40
Requires(post): /bin/touch
Requires(postun): /bin/touch

%description
The default freedesktop.org sound theme following the XDG theming
specification.  (http://0pointer.de/public/sound-theme-spec.html).

%prep
%setup -q

%build
%configure

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post
/bin/touch --no-create %{_datadir}/sounds/freedesktop %{_datadir}/sounds

%postun
/bin/touch --no-create %{_datadir}/sounds/freedesktop %{_datadir}/sounds

%files
%doc README
%dir %{_datadir}/sounds/freedesktop
%dir %{_datadir}/sounds/freedesktop/stereo
%{_datadir}/sounds/freedesktop/index.theme
%{_datadir}/sounds/freedesktop/stereo/*.oga

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.8-3
- Mass rebuild 2013-12-27

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Sep 25 2012 Matthias Clasen <mclasen@redhat.com> - 0.8-1
- Update to 0.8
- Drop obsolete Obsoletes

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 12 2009 Matthias Clasen <mclasen@redhat.com> - 0.7-2
- Obsolete gnome-audio

* Mon Sep 28 2009 Jon McCann <jmccann@redhat.com> 0.7-1
- Update to 0.7

* Thu Sep 10 2009 Lennart Poettering <lpoetter@redhat.com> 0.6.99-1
- Snapshot from Lennart's git tree

* Fri Aug 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.6-1
- New upstream

* Thu Aug 27 2009 Lennart Poettering <lpoetter@redhat.com> 0.5-1
- New upstream

* Sun Aug 23 2009 Jon McCann <jmccann@redhat.com> 0.4-1
- New release adds screen capture sound

* Tue Jul 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.3-2
- Forgot tarball

* Tue Jul 28 2009 Lennart Poettering <lpoetter@redhat.com> 0.3-1
- Update to 0.3

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Oct 22 2008 Jon McCann <jmccann@redhat.com> 0.2-2
- Rebuild with BuildRequires intltool

* Wed Oct 22 2008 Jon McCann <jmccann@redhat.com> 0.2-1
- Update to 0.2

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-4
- Fix changelog

* Tue Sep 9 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-3
- Touch root dirs, not just theme dirs

* Mon Aug 11 2008 Jeremy Katz <katzj@redhat.com> - 0.1-2
- require touch for scriptlets to not give errors

* Sun Jun 15 2008 Lennart Poettering <lpoetter@redhat.com> 0.1-1
- Initial package
