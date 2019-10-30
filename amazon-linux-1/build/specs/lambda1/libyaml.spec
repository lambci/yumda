%define _buildid .7

%define tarballname yaml

#====================================================================#

Name:       libyaml
Version:    0.1.6
Release: 6%{?_buildid}%{?dist}
Summary:    YAML 1.1 parser and emitter written in C

Group:      System Environment/Libraries
License:    MIT
URL:        http://pyyaml.org/
Source0:    http://pyyaml.org/download/libyaml/%{tarballname}-%{version}.tar.gz
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Patch0: libyaml-CVE-2014-9130.patch

Prefix: %{_prefix}

%description
YAML is a data serialization format designed for human readability and
interaction with scripting languages.  LibYAML is a YAML parser and
emitter written in C.


%prep
%setup -q -n %{tarballname}-%{version}

%patch0 -p1

%build
%configure --disable-static
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} INSTALL="install -p" install
rm -f %{buildroot}%{_libdir}/*.{la,a}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%license LICENSE
%{_libdir}/%{name}*.so.*

%exclude %{_includedir}
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig

%changelog
* Wed Oct 30 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 1) with prefix /opt

* Tue Feb 3 2015 Sean Kelly <seankell@amazon.com>
- import source package F21/libyaml-0.1.6-6.fc21

* Mon Dec  1 2014 John Eckersberg <eck@redhat.com> - 0.1.6-6
- Add patch for CVE-2014-9130 (RHBZ#1169371)

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jul 18 2014 Tom Callaway <spot@fedoraproject.org> - 0.1.6-4
- fix license handling

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Thu Apr 3 2014 hpetty <hpetty@amazon.com>
- import source package F19/libyaml-0.1.6-1.fc19
- import source package F19/libyaml-0.1.5-1.fc19

* Mon Mar 31 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.6-2
- Work around ldconfig bug with libyaml.so (bz1082822)

* Wed Mar 26 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.6-1
- New upstream release 0.1.6 (bz1081492)
- Fixes CVE-2014-2525 (bz1078083)

* Thu Feb 13 2014 hpetty <hpetty@amazon.com>
- removed duplicate line from spec file

* Sat Feb 8 2014 hpetty <hpetty@amazon.com>
- import source package F19/libyaml-0.1.4-6.fc19
- import source package F19/libyaml-0.1.4-4.fc19
- import source package F18/libyaml-0.1.4-3.fc18
- import source package F17/libyaml-0.1.4-2.fc17
- import source package F16/libyaml-0.1.4-1.fc16

* Tue Feb  4 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.5-1
- New upstream release 0.1.5 (bz1061087)
- Removed patches for CVE-2013-6393; they are included in 0.1.5
  upstream

* Wed Jan 29 2014 John Eckersberg <jeckersb@redhat.com> - 0.1.4-6
- Add patches for CVE-2013-6393 (bz1033990)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Feb 16 2012 Cristian Gafton <gafton@amazon.com>
- update to upstream 0.1.4

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul 20 2011 Cristian Gafton <gafton@amazon.com>
- import source package EPEL6/libyaml-0.1.3-1.el6

* Tue Jul 19 2011 Cristian Gafton <gafton@amazon.com>
- setup complete for package libyaml

* Thu Jun 23 2011 John Eckersberg <jeckersb@redhat.com> - 0.1.4-1
- New upstream release 0.1.4

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jan 22 2011 Cristian Gafton <gafton@amazon.com>
- import source package GOBI/libyaml-0.1.3-1.el6
- setup complete for package libyaml

* Fri Oct 02 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.3-1
- New upstream release 0.1.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-4
- Minor tweaks to spec file
- Enable %%check section
- Thanks Gareth Armstrong <gareth.armstrong@hp.com>

* Tue Mar 3 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-3
- Remove static libraries

* Thu Feb 26 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-2
- Remove README and LICENSE from docs on -devel package
- Remove -static package and merge contents into the -devel package

* Wed Feb 25 2009 John Eckersberg <jeckersb@redhat.com> - 0.1.2-1
- Initial packaging for Fedora
