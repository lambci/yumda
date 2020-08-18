Name:           userspace-rcu
Version:        0.7.7
Release:        1%{?dist}
Summary:        RCU (read-copy-update) implementation in user space

Group:          System Environment/Libraries
License:        LGPLv2+
URL:            http://lttng.org/urcu/
Source0:        http://lttng.org/files/urcu/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  pkgconfig 
# Upstream do not yet support mips
ExcludeArch:    mips

Prefix: %{_prefix}

%description
This data synchronization library provides read-side access which scales
linearly with the number of cores. It does so by allowing multiples copies
of a given data structure to live at the same time, and by monitoring
the data structure accesses to detect grace periods after which memory
reclamation is possible.


%prep
%setup -q


%build
%configure --disable-static
#Remove Rpath from build system
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

V=1 make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -vf $RPM_BUILD_ROOT%{_libdir}/*.la


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%license LICENSE gpl-2.0.txt lgpl-relicensing.txt lgpl-2.1.txt
%{_libdir}/*.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_docdir}


%changelog
* Mon Aug 17 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jul 05 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.7-1
- New upstream version

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan 18 2013 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.6-1
- New upstream version

* Tue Oct 23 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.5-1
- New upstream version 

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jun 14 2012 Yannick Brosseau <yannick.brosseau@gmail.com> - 0.7.3-1
- New upstream version (#828716)

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.4.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Feb 26 2010 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.4.1-1
- new upstream version.

* Tue Oct 20 2009 Jan "Yenya" Kasprzak <kas@fi.muni.cz> 0.2.4-1
- Initial revision.
