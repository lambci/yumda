Name:           jbigkit
Version:        2.0
Release: 11%{?dist}.0.2
Summary:        JBIG1 lossless image compression tools

Group:          Development/Libraries
License:        GPLv2+
URL:            http://www.cl.cam.ac.uk/~mgk25/jbigkit/
Source0:        http://www.cl.cam.ac.uk/~mgk25/download/jbigkit-%{version}.tar.gz
Patch0:         jbigkit-2.0-shlib.patch
Patch1:         jbigkit-2.0-warnings.patch
Patch2:         jbigkit-2.0-CVE-2013-6369.patch

Prefix: %{_prefix}

%description
The jbigkit package contains tools for converting between PBM and JBIG1
formats.

%package libs
Summary:        JBIG1 lossless image compression library
Group:          Development/Libraries
Prefix: %{_prefix}

%description libs
JBIG-KIT provides a portable library of compression and decompression
functions with a documented interface that you can include very easily
into your image or document processing software. In addition, JBIG-KIT
provides ready-to-use compression and decompression programs with a
simple command line interface (similar to the converters found in netpbm).

JBIG-KIT implements the specification:
    ISO/IEC 11544:1993 and ITU-T Recommendation T.82(1993):
     Information technology — Coded representation of picture and audio
     information — Progressive bi-level image compression 

which is commonly referred to as the “JBIG1 standard”


%prep
%setup -q -n jbigkit
%patch0 -p1 -b .shlib
%patch1 -p1 -b .warnings
%patch2 -p1 -b .CVE-2013-6369

%build
make %{?_smp_mflags} CCFLAGS="$RPM_OPT_FLAGS"

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}

install -p -m0755 libjbig/libjbig.so.%{version} $RPM_BUILD_ROOT/%{_libdir}
install -p -m0755 libjbig/libjbig85.so.%{version} $RPM_BUILD_ROOT/%{_libdir}

install -p -m0755 pbmtools/???to??? $RPM_BUILD_ROOT%{_bindir}
install -p -m0755 pbmtools/???to???85 $RPM_BUILD_ROOT%{_bindir}

%files
%license COPYING
%{_bindir}/???to*

%files libs
%license COPYING
%{_libdir}/libjbig*.so.%{version}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Apr 02 2014 Jiri Popelka <jpopelka@redhat.com> - 2.0-11
- CVE-2013-6369 (#1083412)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.0-10
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.0-9
- Mass rebuild 2013-12-27

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Jul 17 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-7
- Fix a number of compiler warnings per feedback from Ubuntu security team (#840608)

* Mon Apr 16 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-6
- Don't install up-to-date license file, use the upstream one. (#807760)

* Wed Mar 28 2012 Jiri Popelka <jpopelka@redhat.com> - 2.0-5
- Moving from rpmfusion-free to Fedora because it will be free of known patents
  in all countries from 2012-04-04 onwards
- Changed license from GPL to GPLv2+ and included up-to-date license file

* Wed Feb 08 2012 Nicolas Chauvet <kwizart@gmail.com> - 2.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 2.0-3
- rebuild for new F11 features

* Fri Sep 05 2008 David Woodhouse <dwmw2@infradead.org> 2.0-2
- Add missing jbig_ar.h

* Wed Sep 03 2008 David Woodhouse <dwmw2@infradead.org> 2.0-1
- Update to 2.0

* Sun Aug 03 2008 Thorsten Leemhuis <fedora@leemhuis.info> - 1.6-3
- rebuild

* Sun Oct  1 2006 David Woodhouse <dwmw2@infradead.org> 1.6-2
- Review fixes

* Tue Sep 12 2006 David Woodhouse <dwmw2@infradead.org> 1.6-1
- Initial version
