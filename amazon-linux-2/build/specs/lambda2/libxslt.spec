Summary: Library providing the Gnome XSLT engine
Name: libxslt
Version: 1.1.28
Release: 6%{?dist}%{?extra_release}
License: MIT
Group: Development/Libraries
Source: ftp://xmlsoft.org/XSLT/libxslt-%{version}.tar.gz
URL: http://xmlsoft.org/XSLT/
BuildRequires: libxml2-devel >= 2.6.27
BuildRequires: python2-devel
BuildRequires: libxml2-python
BuildRequires: libgcrypt-devel
BuildRequires: automake autoconf

# Fedora specific patches
Patch0: multilib.patch
Patch1: libxslt-1.1.26-utf8-docs.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1775516
Patch2: libxslt-1.1.28-CVE-2019-18197.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1715731
Patch3: libxslt-1.1.28-CVE-2019-11068.patch

Prefix: %{_prefix}

%description
This C library allows to transform XML files into other XML files
(or HTML, text, ...) using the standard XSLT stylesheet transformation
mechanism. To use it you need to have a version of libxml2 >= 2.6.27
installed. The xsltproc command is a command line interface to the XSLT engine

%prep
%setup -q
%patch0 -p1
%patch1 -p1 -b .utf8
%patch2 -p1
%patch3 -p1
# Now fix up the timestamps of patched docs files
# ChangeLog needs to be retouched before gzip as well
# since timestamp affects output
touch -r ChangeLog.utf8 ChangeLog
gzip -9 ChangeLog
touch -r ChangeLog.utf8 ChangeLog.gz
touch -r NEWS.utf8 NEWS

chmod 644 python/tests/*

%build
%configure --disable-static --without-python
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%defattr(-, root, root,-)
%license Copyright
%{_libdir}/lib*.so.*
%dir %{_libdir}/libxslt-plugins
%{_bindir}/xsltproc

%exclude %{_includedir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/*.sh
%exclude %{_mandir}
%exclude %{_datadir}
%exclude %{_bindir}/xslt-config

%changelog
* Thu Oct 29 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Apr 22 2020 David King <dking@redhat.com> - 1.1.28-6
- Fix CVE-2019-18197 (#1775516)
- Fix CVE-2019-11068 (#1715731)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.1.28-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.1.28-4
- Mass rebuild 2013-12-27

* Fri Jun 21 2013 Matthias Clasen <mclasen@redhat.com> - 1.1.28-3
- Don't ship api docs twice (they were included in both
  the main and the devel package, by accident (need to save
  space on the f19 live images)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.28-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 21 2012 Daniel Veillard <veillard@redhat.com> - 1.1.28-1
- upstream release of libxslt-1.1.28
- a few bug fixes and cleanups

* Tue Oct  9 2012 Daniel Veillard <veillard@redhat.com> - 1.1.27-2
- fix a regression in default namespace handling

* Wed Sep 12 2012 Daniel Veillard <veillard@redhat.com> - 1.1.27-1
- upstream release of libxslt-1.1.27
- a lot of bug fixes and improvements

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.26-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.26-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 20 2011 Michel Salim <salimma@fedoraproject.org> - 1.1.26-8
- ChangeLog: fix character encoding
- Restore timestamps for patched documentation files

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.26-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Dec 17 2010 Dan Horák <dan[at]danny.cz> - 1.1.26-6
- libexslt needs libgcrypt-devel via its pkgconfig file

* Mon Oct 25 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.1.26-5
- Patch from Paul Howarth for converting files to utf8 (#226088)

* Tue Oct 05 2010 Parag Nemade <paragn AT fedoraproject.org> - 1.1.26-4
- Merge-review cleanup (#226088)

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 1.1.26-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon May 24 2010 Tom "spot" Callaway <tcallawa@redhat.com> 1.1.26-2
- disable static libs

* Thu Sep 24 2009 Daniel Veillard <veillard@redhat.com> 1.1.26-1
- couple of bug fixes
- export a symbol needed by lxml

* Mon Sep 21 2009 Daniel Veillard <veillard@redhat.com> 1.1.25-2
- fix a locking bug in 1.1.25

* Thu Sep 17 2009 Daniel Veillard <veillard@redhat.com> 1.1.25-1
- release of 1.1.25
- Add API versioning  for libxslt shared library
- xsl:sort lang support using the locale
- many bug fixes

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.24-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> 1.1.24-3
- Rebuild for Python 2.6

* Wed Oct  8 2008 Daniel Veillard <veillard@redhat.com> 1.1.24-2.fc10
- CVE-2008-2935 fix

* Tue May 13 2008 Daniel Veillard <veillard@redhat.com> 1.1.24-1.fc10
- release of 1.1.24
- fixes a few bugs including the key initialization problem
- tentative fix for multiarch devel problems

* Mon Apr 28 2008 Daniel Veillard <veillard@redhat.com> 1.1.23-3.fc10
- and the previous patch was incomplte breaking the python bindings
  see 444317 and 444455

* Tue Apr 22 2008 Daniel Veillard <veillard@redhat.com> 1.1.23-2.fc10
- revert a key initialization patch from 1.1.23 which seems broken
  see rhbz#442097

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> 1.1.23-1.fc9
- upstream release 1.1.23
- bugfixes

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.22-2
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Daniel Veillard <veillard@redhat.com> 1.1.22-1
- upstream release 1.1.22 see http://xmlsoft.org/XSLT/news.html

* Tue Jun 12 2007 Daniel Veillard <veillard@redhat.com> 1.1.21-1
- upstream release 1.1.21 see http://xmlsoft.org/XSLT/news.html

* Thu Feb 15 2007 Adam Jackson <ajax@redhat.com>
- Add dist tag to Release to fix 6->7 upgrades.

* Wed Jan 17 2007 Daniel Veillard <veillard@redhat.com>
- upstream release 1.1.20 see http://xmlsoft.org/XSLT/news.html

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 1.1.19-2
- rebuild against python 2.5

* Wed Nov 29 2006 Daniel Veillard <veillard@redhat.com>
- upstream release 1.1.19 see http://xmlsoft.org/XSLT/news.html

* Thu Oct 26 2006 Daniel Veillard <veillard@redhat.com>
- upstream release 1.1.18 see http://xmlsoft.org/XSLT/news.html

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.1.17-1.1
- rebuild

* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com>
- upstream release 1.1.17 see http://xmlsoft.org/XSLT/news.html
