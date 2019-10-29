%define _buildid .5

%global _hardened_build 1
Name:		libwebp
Version:	0.3.0
Release: 3%{?_buildid}%{?dist}
Group:		Development/Libraries
URL:		http://webmproject.org/
Summary:	Library and tools for the WebP graphics format
# Additional IPR is licensed as well. See PATENTS file for details
License:	BSD
Source0:	http://webp.googlecode.com/files/%{name}-%{version}.tar.gz
Source1:	libwebp_jni_example.java	
BuildRequires:	libjpeg-devel libpng-devel libtool swig 
BuildRequires:  giflib-devel
BuildRequires:  libtiff-devel
BuildRequires:	jpackage-utils

Prefix: %{_prefix}

%description
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%package tools
Group:		Development/Tools
Summary:	The WebP command line tools
Prefix: %{_prefix}

%description tools
WebP is an image format that does lossy compression of digital
photographic images. WebP consists of a codec based on VP8, and a
container based on RIFF. Webmasters, web developers and browser
developers can use WebP to compress, archive and distribute digital
images more efficiently.

%prep
%setup -q

%build
mkdir -p m4
./autogen.sh
# enable libwebpmux since gif2webp depends on it
%configure --disable-static --enable-libwebpmux
make %{?_smp_mflags}

%install
%make_install

%files tools
%{_bindir}/cwebp
%{_bindir}/dwebp
%{_bindir}/gif2webp
%{_bindir}/webpmux

%files -n %{name}
%license PATENTS COPYING
%{_libdir}/%{name}*.so.*

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Tue Oct 29 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Wed Sep 17 2014 Rodrigo Novo <rodarvus@amazon.com>
- Explicitly build against Java 1.6.0

* Wed May 7 2014 Cristian Gafton <gafton@amazon.com>
- import source package RHEL7/libwebp-0.3.0-3.el7

* Tue Mar 11 2014 Jamin W. Collins <jamin@amazon.com>
- adding -fPIC to gcc arguments

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 0.3.0-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.3.0-2
- Mass rebuild 2013-12-27

* Fri Dec 13 2013 Cristian Gafton <gafton@amazon.com>
- import source package RHEL7/libwebp-0.3.0-1.el7

* Thu Dec 12 2013 Cristian Gafton <gafton@amazon.com>
- setup complete for package libwebp

* Mon May 13 2013 Rahul Sundaram <sundaram@fedoraproject.org> - 0.3.0-1
- upstream release 0.3.0
- enable gif2webp
- add build requires on giflib-devel and libtiff-devel
- use make_install and hardened macros
- list binaries explicitly

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Adam Tkac <atkac redhat com> - 0.2.1-2
- rebuild due to "jpeg8-ABI" feature drop

* Thu Dec 27 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.2.1-1
- new upstream release 0.2.1

* Fri Dec 21 2012 Adam Tkac <atkac redhat com> - 0.1.3-3
- rebuild against new libjpeg

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 02 2012 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.3-1
- Several spec improvements by Scott Tsai <scottt.tw@gmail.com>

* Wed May 25 2011 Rahul Sundaram <sundaram@fedoraproject.org> - 0.1.2-1
- Initial spec. Based on openSUSE one
