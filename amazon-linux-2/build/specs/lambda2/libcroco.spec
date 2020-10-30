Name:             libcroco
Summary:          A CSS2 parsing library
Version:          0.6.12
Release:          6%{?dist}
License:          LGPLv2
Group:            System Environment/Libraries
Source:           http://download.gnome.org/sources/libcroco/0.6/%{name}-%{version}.tar.xz
#Fedora-specific patch
Patch0:           libcroco-0.6.1-multilib.patch
# https://gitlab.gnome.org/GNOME/libcroco/-/merge_requests/5
Patch1:           CVE-2020-12825.patch

BuildRequires:    pkgconfig
BuildRequires:    glib2-devel
BuildRequires:    libxml2-devel

Prefix: %{_prefix}

%description
CSS2 parsing and manipulation library for GNOME

%prep
%setup -q
%patch0 -p1 -b .multilib
%patch1 -p1 -b .CVE-2020-12825

%build
%configure --disable-static
make %{?_smp_mflags} CFLAGS="$CFLAGS -fno-strict-aliasing"

%install
%make_install

%files
%license COPYING COPYING.LIB
%{_bindir}/csslint-0.6
%{_libdir}/*.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_datadir}
%exclude %{_bindir}/croco-0.6-config

%changelog
* Thu Oct 29 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Mon Aug 03 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 0.6.12-6
- Rebuild with 7.9-z target
  Related: #1835951

* Mon Aug 03 2020 Michael Catanzaro <mcatanzaro@redhat.com> - 0.6.12-5
- Fix CVE-2020-12825
  Resolves: #1835951

* Thu Apr 06 2017 Richard Hughes <rhughes@redhat.com> - 0.6.12-4
- Update to 0.6.12
- Resolves: #1569991

* Thu Dec 17 2015 Kalev Lember <klember@redhat.com> - 0.6.11-1
- Update to 0.6.11
- Resolves: #1386999

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.6.8-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.8-4
- Mass rebuild 2013-12-27

* Tue Jul 16 2013 Matthias Clasen <mclasen@redhat.com> - 0.6.8-3
- Disable strict aliasing, since the code is not strict-aliasing-clean

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Nov 09 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.8-1
- Update to 0.6.8

* Tue Oct 16 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.7-1
- Update to 0.6.7

* Wed Sep 19 2012 Richard Hughes <hughsient@gmail.com> - 0.6.6-1
- Update to 0.6.6

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Mar 27 2012 Kalev Lember <kalevlember@gmail.com> - 0.6.5-1
- Update to 0.6.5
- Dropped unused configure options

* Mon Feb  6 2012 Matthias Clasen <mclasen@redhat.com> - 0.6.4-1
- Update to 0.6.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Nov 22 2011 Matthias Clasen <mclasen@redhat.com> - 0.6.3-1
- Update to 0.6.3

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Sep 10 2010 Parag Nemade <paragn AT fedoraproject.org> 0.6.2-5
- Merge-review cleanup (#225994)

* Tue Dec  8 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.2-4
- Add source url

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb  4 2009 Matthias Clasen <mclasen@redhat.com> - 0.6.2-1
- Update to 0.6.2

* Tue Apr  1 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.1-5
- Clean up dependencies

* Fri Feb  8 2008 Matthias Clasen <mclasen@redhat.com> - 0.6.1-4
- Rebuild for gcc 4.3

* Wed Oct 10 2007 Matthias Clasen <mclasen@redhat.com> - 0.6.1-3
- Rebuild
- Update license tag

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.6.1-2.1
- rebuild

* Tue May 23 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.1-2
- Make config script a pkg-config wrapper to fix multilib conflict

* Mon Mar 13 2006 Matthias Clasen <mclasen@redhat.com> - 0.6.1-1
- Update to 0.6.1
- Drop upstreamed patches

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-6.2.1
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.6.0-6.2
- rebuilt for new gcc4.1 snapshot and glibc changes

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Sat Oct 15 2005 Florian La Roche <laroche@redhat.com>
- link shared lib against -lglib-2.0 and -lxml2

* Wed Mar  2 2005 Matthias Clasen <mclasen@redhat.com> - 0.6.0-5
- Rebuild with gcc4

* Wed Sep 22 2004 Matthias Clasen <mclasen@redhat.com> - 0.6.0-4
- Move croco-config to the devel package

* Mon Sep 20 2004 Matthias Clasen <mclasen@redhat.com> - 0.6-3
- Don't memset() stack variables

* Tue Aug 31 2004 Matthias Clasen <mclasen@redhat.com> - 0.6-2
- Add missing ldconfig calls (#131279)

* Fri Jul 30 2004 Matthias Clasen <mclasen@redhat.com> - 0.6-1
- Update to 0.6

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Sat Apr 10 2004 Warren Togami <wtogami@redhat.com>
- BR and -devel req libgnomeui-devel

* Tue Mar 02 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Tue Jan 27 2004 Jonathan Blandford <jrb@redhat.com> 0.4.0-1
- new version

* Wed Aug 13 2003 Jonathan Blandford <jrb@redhat.com> 0.3.0-1
- initial import into the tree.  Based on the spec file in the package
