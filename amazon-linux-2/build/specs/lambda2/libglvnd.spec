%global _trivial .0
%global _buildid .1
#global commit0 8d4d03f77d6e7684ff32180b8ef78aa87d945b49
#global date 20170818
#global shortcommit0 %%(c=%%{commit0}; echo ${c:0:7})

%if 0%{?rhel} && 0%{?rhel} < 7
%global _without_mesa_glvnd_default 1
%endif

# Set to 0 to skip testsuite.
%global with_tests 1

Name:           libglvnd
Version:        1.0.0
Release: 1%{?commit0:.%{date}git%{shortcommit0}}%{?dist}.0.2
# Provide an upgrade path from the negativo17.org pkgs which have Epoch 1
Epoch:          1
Summary:        The GL Vendor-Neutral Dispatch library

License:        MIT
URL:            https://github.com/NVIDIA/libglvnd
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
#Source0:        %%{url}/archive/%%{commit0}.tar.gz#/%%{name}-%%{shortcommit0}.tar.gz

BuildRequires:  libtool
BuildRequires:  gcc
BuildRequires:  python
BuildRequires:  libxml2-python
BuildRequires:  pkgconfig(glproto)
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xext)

# X11 tests:
#Xvfb is unlikely to reproduce a full Xorg environnement
#So some tests are failing
#https://github.com/NVIDIA/libglvnd/issues/93
%if 0%{?with_tests}
BuildRequires:  xorg-x11-server-Xvfb
%endif

%if (0%{?rhel} && 0%{?rhel} <= 6)
BuildRequires:  autoconf268
%endif

%{?_without_mesa_glvnd_default:
%if (0%{?rhel} && 0%{?rhel} <= 6)

%{?filter_setup:
%filter_provides_in %{_libdir}/%{name}
%filter_requires_in %{_libdir}/%{name}
%filter_setup
}

%else

%global __provides_exclude_from %{_libdir}/%{name}
%global __requires_exclude_from %{_libdir}/%{name}

%endif
}

Prefix: %{_prefix}

%description
libglvnd is an implementation of the vendor-neutral dispatch layer for
arbitrating OpenGL API calls between multiple vendors on a per-screen basis.


%package        opengl
Summary:        OpenGL support for libglvnd
Requires:       %{name}%{?_isa} = %{epoch}:%{version}-%{release}
Prefix: %{_prefix}

%description    opengl
libOpenGL is the common dispatch interface for the workstation OpenGL API.


%prep
%setup -q -n %{name}-%{?commit0}%{?!commit0:%{version}}
%if 0%{?rhel} == 6
autoreconf268 -vif
%else
autoreconf -vif
%endif


%build
#Prefer asm and tls for x86* and ppc64*
#armhfp and aarch64 fallback to asm and tsd
#Others arches fallback to pure-c and tls.
%configure \
  --disable-static \
  --enable-asm \
  --enable-tls

%make_build V=1


%install
%make_install INSTALL="install -p"
find %{buildroot} -name '*.la' -delete

%{?_without_mesa_glvnd_default:
# Avoid conflict with mesa-libGL
mkdir -p %{buildroot}%{_libdir}/%{name}
for l in libEGL libGL libGLESv1_CM libGLESv2 libGLX; do
  mv %{buildroot}%{_libdir}/${l}.so* \
    %{buildroot}%{_libdir}/%{name}
done
}

# Create directory layout
mkdir -p %{buildroot}%{_sysconfdir}/glvnd
mkdir -p %{buildroot}%{_datadir}/glvnd


%files
%license README.md
%dir %{_sysconfdir}/glvnd
%dir %{_datadir}/glvnd
%{_libdir}/libGLdispatch.so.0*

%files opengl
%{_libdir}/libOpenGL.so.0*

%exclude %{_libdir}/libGLES*.so.*
%exclude %{_libdir}/libGL.so.*
%exclude %{_libdir}/libGLX.so.*
%exclude %{_libdir}/libEGL*.so.*
%exclude %{_includedir}
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/*.so


%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Thu Nov 09 2017 Leigh Scott <leigh123linux@googlemail.com> - 1:1.0.0-1
- Update to 1.0.0 release

* Wed Aug 23 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-24.20170818git8d4d03f
- Update snapshot to 20170818

* Mon Aug 14 2017 Ville Skyttä <ville.skytta@iki.fi> - 1:0.2.999-23.20170620gitd850cdd
- Own %%{_sysconfdir}/egl and %%{_datadir}/egl dirs

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.999-22.20170620gitd850cdd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1:0.2.999-21.20170620gitd850cdd
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Jul 07 2017 Igor Gnatenko <ignatenko@redhat.com> - 1:0.2.999-20.20170620gitd850cdd
- Rebuild due to bug in RPM (RHBZ #1468476)

* Thu Jul 06 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-19.20170620gitd850cdd
- Update snapshot to 20170620

* Tue Jun 13 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-18.20170607git80d9a87
- Update snapshot to 20170607
- Default to asm and tls when available
- Use the fixed tsd for armhfp and aarch64
  fixed in https://github.com/NVIDIA/libglvnd/issues/116

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-17.20170308git8e6e102
- Add conditional to disable testsuite, when needed

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-16.20170308git8e6e102
- Rebuilt with testsuite again

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-15.20170308git8e6e102
- Rebuilt without testssuite

* Tue Apr 04 2017 Björn Esser <besser82@fedoraproject.org> - 1:0.2.999-14.20170308git8e6e102
- Fix conditionals for _without_mesa_glvnd_default
- Fix other RHEL-conditionals, too

* Tue Apr 04 2017 Simone Caronni <negativo17@gmail.com> - 1:0.2.999-13.20170308git8e6e102
- Update RPM filters for private libraries (includes GLX, fixes RHEL 6).

* Mon Apr 03 2017 Simone Caronni <negativo17@gmail.com> - 1:0.2.999-12.20170308git8e6e102
- Update to latest snapshot, remove upstreamed patches.
- Update release to packaging guidelines format.
- Make sure that for Fedora 24 and RHEL the libraries are always private.

* Thu Feb 23 2017 Nicolas Chauvet <kwizart@gmail.com> - 1:0.2.999-11.gitdc16f8c
- asm enabled only for x86 - rhbz#1419944

* Mon Feb  6 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-10.gitdc16f8c
- Drop 0007-GLX-Add-GLX_SGIX_fbconfig-functions.patch the bug this works
  around actually is in mesa

* Thu Feb  2 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-9.gitdc16f8c
- Add eglexternalplatform spec. config dirs to -egl subpackage (rhbz#1415143)

* Thu Feb  2 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-8.gitdc16f8c
- Fix GLX_SGIX_fbconfig extension, this fixes games such as "The Binding of
  Isaac: Rebirth" and "Crypt of the NecroDancer" from Steam not working

* Wed Jan 11 2017 Hans de Goede <hdegoede@redhat.com> - 1:0.2.999-7.gitdc16f8c
- Epoch:1 to provide upgrade path from negativo17.org rpms
- New snapshot
- Add patches to fix building on ARM (from Rob Clark)
- Add BuildRequires: python
- Add ldconfig scriptlets for library sub-packages

* Wed Jan 11 2017 Adam Jackson <ajax@redhat.com>
- Don't hide libraries in a subdir (rhbz#1413579)
- Split up libraries to appropriate subpackages
- Make the req/prov filter catch more cases
- Restore libGLESv1 for ABI compliance

* Wed Oct 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.2.999-6.git28867bb
- Update snapshot
- Fix EGL crash for KDE/Plasma (rfbz#4303)

* Tue Oct 25 2016 Leigh Scott <leigh123linux@googlemail.com> - 0.2.999-5.git295e5e5
- Fix EGL crash (rfbz#4303)

* Fri Oct 14 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.2.999-4.git295e5e5
- Update snapshot

* Wed Oct 12 2016 Adam Jackson <ajax@redhat.com> - 0.2.999-3.git14f6283
- Restore hardened build
- Remove ExclusiveArch
- Remove some pointless Provides/Obsoletes
- BuildRequires pkgconfig(xext) not pkgconfig(xv)
- Update description to be a bit more confident
- Dump make check errors into the build log

* Wed Oct 05 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.2.999-2.git14f6283
- Add the correct License: MIT

* Thu Sep 15 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.2.999-1.git14f6283
- Update to 2.999 version
- Add EGL

* Fri Sep 02 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-2.gitf7fbc4b
- Update license
- Fix Obsoletes/Provides to avoid self obsolete

* Tue Aug 30 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.1-1.gitf7fbc4b
- Update to 1.1.gitf7fbc4b

* Tue Jun 14 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-4.git093f048
- Update to 20160610 git commit

* Fri May 20 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-3.gita82982d
- Update to current snapshot

* Fri May 13 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-2.git509de0d
- Update to current snapshot
- Remove unused dt-auxiliary
- Add support for graphical make test
- Undefine hardened build for xorg

* Wed May 04 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.1.0-1.git8277115
- Update to lastest snapshot

* Thu Feb 18 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-9.git4d977ea
- Remove patch to enable by default

* Wed Feb 17 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-8git20160217
- Update to git20160217
- Introduce --with mesa-libglvnd-default build conditional
- Avoid error on make check - testglxqueryversion.sh stil fails in mock
- Filter on provided libGL until glvnd support is in upstream mesa
- Use upstream tarball and use autoreconf

* Fri Jan 15 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-7git20160115
- Bump for 20160115
- Enable make check
- Description improvements
- Enable libglvnd by default
- Enable devel sub-package

* Wed Jan 06 2016 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-6git20160106
- Update to 20160106 snapshot
- Remove 10-x11glvnd

* Sat Nov 21 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-5git20151121
- Update to 20151121 snapshot
- Avoid conflicts with mesa-libGL{,ES}
- Disable libGLESv1_CM

* Tue Nov 10 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-4git20151110
- Update to today snapshot
- Fix license

* Tue Sep 01 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-3git20150901
- Update to snapshot 20150901

* Fri Aug 07 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-2
- Update to today snapshoot

* Fri Feb  6 2015 Nicolas Chauvet <kwizart@gmail.com> - 0.0.0-1
- Initial spec file
