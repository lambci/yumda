%bcond_with bootstrap
%bcond_with tests

%bcond_without python2
%bcond_without python3
%if %{without python3} || %{?amzn}
%bcond_with doc
%else
%bcond_without doc
%endif

%global srcname pip
%global python_wheelname %{srcname}-%{version}-py2.py3-none-any.whl
%if %{without bootstrap}
%if %{with python2}
%global python2_wheelname %python_wheelname
%endif
%if %{with python3}
%global python3_wheelname %python_wheelname
%endif
%endif

# Note that with disabled python3, bashcomp2 will be disabled as well because
# bashcompdir will point to a different path than with python3 enabled.
%global bashcompdir %(b=$(pkg-config --variable=completionsdir bash-completion 2>/dev/null); echo ${b:-%{_sysconfdir}/bash_completion.d})
%if "%{bashcompdir}" != "%{_sysconfdir}/bash_completion.d"
%global bashcomp2 1
%endif

%define _trivial .0
%define _buildid .1
Name:           python-%{srcname}
# When updating, update the bundled libraries versions bellow!
Version:        9.0.3
Release:        1%{?dist}%{?_trivial}%{?_buildid}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz
Source1000:     pip.conf

BuildArch:      noarch

%if %{with tests}
BuildRequires:  git
BuildRequires:  bzr
%endif

# to get tests:
# git clone https://github.com/pypa/pip && cd pip
# git checkout 9.0.1 && tar -czvf ../pip-9.0.1-tests.tar.gz tests/
%if %{with tests}
Source1:        pip-9.0.1-tests.tar.gz
%endif

# Patch until the following issue gets implemented upstream:
# https://github.com/pypa/pip/issues/1351
Patch0:         allow-stripping-given-prefix-from-wheel-RECORD-files.patch

# Downstream only patch
# Emit a warning to the user if pip install is run with root privileges
# Issue upstream: https://github.com/pypa/pip/issues/4288
Patch1:         emit-a-warning-when-running-with-root-privileges.patch

%description
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs
Packages" or "Pip Installs Python".


%if %{with python2}
%package -n python2-%{srcname}
Summary:        A tool for installing and managing Python 2 packages
Group:          Development/Libraries
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-mock
BuildRequires:  python2-pytest
BuildRequires:  python2-pretend
BuildRequires:  python2-freezegun
BuildRequires:  python2-pytest-capturelog
BuildRequires:  python2-scripttest
BuildRequires:  python2-virtualenv
%endif
%if %{without bootstrap}
BuildRequires:  python2-pip
BuildRequires:  python2-wheel
%endif
Requires:       python2-setuptools

# Virtual provides for the packages bundled by pip.
# You can find the versions in pip/_vendor/vendor.txt file.
# Don't forget to update this bellow for python3 as well.
Provides: bundled(python2dist(appdirs)) = 1.4.0
Provides: bundled(python2dist(cachecontrol)) = 0.11.7
Provides: bundled(python2dist(colorama)) = 0.3.7
Provides: bundled(python2dist(distlib)) = 0.2.4
Provides: bundled(python2dist(distro)) = 1.0.1
Provides: bundled(python2dist(html5lib)) = 1.0b10
Provides: bundled(python2dist(ipaddress) = 1.0.17
Provides: bundled(python2dist(lockfile)) = 0.12.2
Provides: bundled(python2dist(packaging)) = 16.8
Provides: bundled(python2dist(setuptools)) = 28.8.0
Provides: bundled(python2dist(progress)) = 1.2
Provides: bundled(python2dist(pyparsing)) = 2.1.10
Provides: bundled(python2dist(requests)) = 2.11.1
Provides: bundled(python2dist(retrying)) = 1.3.3
Provides: bundled(python2dist(six)) = 1.10.0
Provides: bundled(python2dist(webencodings)) = 0.5

# Bundled within the requests bundle
Provides: bundled(python2dist(chardet)) = 2.3.0
Provides: bundled(python2dist(urllib3)) = 1.16

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs
Packages" or "Pip Installs Python".

%endif # with python2


%if %{with python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        A tool for installing and managing Python3 packages
Group:          Development/Libraries

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  bash-completion
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-mock
BuildRequires:  python%{python3_pkgversion}-pytest
BuildRequires:  python%{python3_pkgversion}-pretend
BuildRequires:  python%{python3_pkgversion}-freezegun
BuildRequires:  python%{python3_pkgversion}-pytest-capturelog
BuildRequires:  python%{python3_pkgversion}-scripttest
BuildRequires:  python%{python3_pkgversion}-virtualenv
%endif
%if %{without bootstrap}
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif
Requires:  python%{python3_pkgversion}-setuptools

# Virtual provides for the packages bundled by pip.
# See the python2 list above for instructions.
Provides: bundled(python3dist(appdirs)) = 1.4.0
Provides: bundled(python3dist(cachecontrol)) = 0.11.7
Provides: bundled(python3dist(colorama)) = 0.3.7
Provides: bundled(python3dist(distlib)) = 0.2.4
Provides: bundled(python3dist(distro)) = 1.0.1
Provides: bundled(python3dist(html5lib)) = 1.0b10
Provides: bundled(python3dist(ipaddress) = 1.0.17
Provides: bundled(python3dist(lockfile)) = 0.12.2
Provides: bundled(python3dist(packaging)) = 16.8
Provides: bundled(python3dist(setuptools)) = 28.8.0
Provides: bundled(python3dist(progress)) = 1.2
Provides: bundled(python3dist(pyparsing)) = 2.1.10
Provides: bundled(python3dist(requests)) = 2.11.1
Provides: bundled(python3dist(retrying)) = 1.3.3
Provides: bundled(python3dist(six)) = 1.10.0
Provides: bundled(python3dist(webencodings)) = 0.5

# Bundled within the requests bundle
Provides: bundled(python3dist(chardet)) = 2.3.0
Provides: bundled(python3dist(urllib3)) = 1.16

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
pip is a package management system used to install and manage software packages
written in Python. Many packages can be found in the Python Package Index
(PyPI). pip is a recursive acronym that can stand for either "Pip Installs
Packages" or "Pip Installs Python".

%if %{with doc}
%package doc
Summary:        A documentation for a tool for installing and managing Python packages

BuildRequires:  python%{python3_pkgversion}-sphinx

%description doc
A documentation for a tool for installing and managing Python packages

%endif

%endif # with python3


%prep
%if %{with doc} && %{without python3}
echo "This combination (with doc, without python3) is unsupported"
exit 1
%endif

%setup -q -n %{srcname}-%{version}
%if %{with tests}
tar -xf %{SOURCE1}
%endif

%patch0 -p1
%patch1 -p1

sed -i '1d' pip/__init__.py

# Remove ordereddict as it is only required for python <= 2.6
rm pip/_vendor/ordereddict.py


%build
%if %{with python2}
%if %{without bootstrap}
%py2_build_wheel
%else
%py2_build
%endif
%endif # with python2

%if %{with python3}
%if %{without bootstrap}
%py3_build_wheel
%else
%py3_build
%endif
%endif # with python3

%if %{with doc}
pushd docs
make html
make man
rm _build/html/.buildinfo
popd
%endif


%install
%if %{with python3}
%if %{without bootstrap}
%py3_install_wheel %{python3_wheelname}
%else
%py3_install
%endif

# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/pip
%endif # with python3

%if %{with doc}
install -d %{buildroot}%{_mandir}/man1
%if %{with python2}
install -pm0644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/pip.1
install -pm0644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/pip2.1
%endif
%if %{with python3}
install -pm0644 docs/_build/man/*.1 %{buildroot}%{_mandir}/man1/pip3.1
%endif
%endif # with doc

%if %{with python2}
%if %{without bootstrap}
%py2_install_wheel %{python2_wheelname}
%else
%py2_install
%endif
%endif # with python2

mkdir -p %{buildroot}%{bashcompdir}
%if %{with python2}
PYTHONPATH=%{buildroot}%{python2_sitelib} \
    %{buildroot}%{_bindir}/pip completion --bash \
    > %{buildroot}%{bashcompdir}/pip
%endif
%if %{with python3}
PYTHONPATH=%{buildroot}%{python3_sitelib} \
    %{buildroot}%{_bindir}/pip3 completion --bash \
    > %{buildroot}%{bashcompdir}/pip3
%endif
pips2=pip
pips3=pip3
for pip in %{buildroot}%{_bindir}/pip*; do
    pip=$(basename $pip)
    case $pip in
%if %{with python2}
        pip2*)
            pips2="$pips2 $pip"
%if 0%{?bashcomp2}
            ln -s pip %{buildroot}%{bashcompdir}/$pip
%endif
            ;;
%endif
%if %{with python3}
        pip3?*)
            pips3="$pips3 $pip"
%if 0%{?bashcomp2}
            ln -s pip3 %{buildroot}%{bashcompdir}/$pip
%endif
            ;;
%endif
    esac
done
%if %{with python3}
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 $pips3/" \
    -e s/_pip_completion/_pip3_completion/ \
    %{buildroot}%{bashcompdir}/pip3
%endif
%if %{with python2}
sed -i -e "s/^\\(complete.*\\) pip\$/\\1 $pips2/" \
    %{buildroot}%{bashcompdir}/pip
%endif

# Provide symlinks to executables to comply with Fedora guidelines for Python
%if %{with python2}
ln -s ./pip%{python2_version} %{buildroot}%{_bindir}/pip-%{python2_version}
ln -s ./pip-%{python2_version} %{buildroot}%{_bindir}/pip-2
%endif
%if %{with python3}
ln -s ./pip%{python3_version} %{buildroot}%{_bindir}/pip-%{python3_version}
ln -s ./pip-%{python3_version} %{buildroot}%{_bindir}/pip-3
%endif


%if %{with tests}
%check
%if %{with python2}
py.test-%{python2_version} -m 'not network'
%endif
%if %{with python3}
py.test-%{python3_version} -m 'not network'
%endif
%endif

install -d %{buildroot}%{_sysconfdir}
install -pm0644 %{SOURCE1000} %{buildroot}%{_sysconfdir}/pip.conf

%if %{with python2}
%files -n python2-%{srcname}
%license LICENSE.txt
%doc README.rst
%if %{with doc}
%{_mandir}/man1/pip.*
%{_mandir}/man1/pip2.*
%endif
%{_bindir}/pip
%{_bindir}/pip2
%{_bindir}/pip-2
%{_bindir}/pip%{python2_version}
%{_bindir}/pip-%{python2_version}
%{python2_sitelib}/pip*
%dir %{bashcompdir}
%{bashcompdir}/pip
%if 0%{?bashcomp2}
%{bashcompdir}/pip2*
%dir %(dirname %{bashcompdir})
%endif
%config(noreplace)%{_sysconfdir}/pip.conf
%endif # with python2

%if %{with python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE.txt
%doc README.rst
%if %{with doc}
%{_mandir}/man1/pip3.*
%endif
%{_bindir}/pip3
%{_bindir}/pip-3
%{_bindir}/pip%{python3_version}
%{_bindir}/pip-%{python3_version}
%{python3_sitelib}/pip*
%dir %{bashcompdir}
%{bashcompdir}/pip3*
%if 0%{?bashcomp2}
%dir %(dirname %{bashcompdir})
%endif
%config(noreplace)%{_sysconfdir}/pip.conf

%if %{with doc}
%files doc
%license LICENSE.txt
%doc README.rst
%doc docs/_build/html
%endif # with doc
%endif # with python3

%changelog
* Wed May 2 2018 Frederick Lefebvre <fredlef@amazon.com> - 9.0.3-1.amzn2.0.1
- Add a pip.conf config file to force the list format

* Thu Mar 29 2018 Charalampos Stratakis <cstratak@redhat.com> - 9.0.3-1
- Update to 9.0.3

* Wed Feb 21 2018 Lumír Balhar <lbalhar@redhat.com> - 9.0.1-16
- Include built HTML documentation (in the new -doc subpackage) and man page

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Dec 04 2017 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-14
- Reintroduce the ipaddress module in the python3 subpackage.

* Mon Nov 20 2017 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-13
- Add virtual provides for the bundled libraries. (rhbz#1096912)

* Tue Aug 29 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-12
- Switch macros to bcond's and make Python 2 optional to facilitate building
  the Python 2 and Python 3 modules

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue May 23 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-10
- Modernized package descriptions
Resolves: rhbz#1452568

* Tue Mar 21 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-9
- Fix typo in the sudo pip warning

* Fri Mar 03 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-8
- Patch 1 update: No sudo pip warning in venv or virtualenv

* Thu Feb 23 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-7
- Patch 1 update: Customize the warning with the proper version of the pip
  command

* Tue Feb 14 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-6
- Added patch 1: Emit a warning when running with root privileges

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 9.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Jan 02 2017 Tomas Orsava <torsava@redhat.com> - 9.0.1-4
- Provide symlinks to executables to comply with Fedora guidelines for Python
Resolves: rhbz#1406922

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-3
- Rebuild for Python 3.6 with wheel

* Fri Dec 09 2016 Charalampos Stratakis <cstratak@redhat.com> - 9.0.1-2
- Rebuild for Python 3.6 without wheel

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 9.0.1-1
- Update to 9.0.1

* Fri Nov 18 2016 Orion Poplawski <orion@cora.nwra.com> - 8.1.2-5
- Enable EPEL Python 3 builds
- Use new python macros
- Cleanup spec

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-4
- Updated the test sources

* Fri Aug 05 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-3
- Moved python-pip into the python2-pip subpackage
- Added the python_provide macro

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 8.1.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 17 2016 Tomas Orsava <torsava@redhat.com> - 8.1.2-1
- Update to 8.1.2
- Moved to a new PyPI URL format
- Updated the prefix-stripping patch because of upstream changes in pip/wheel.py

* Mon Feb 22 2016 Slavek Kabrda <bkabrda@redhat.com> - 8.0.2-1
- Update to 8.0.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 7.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Oct 14 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-3
- Rebuilt for Python3.5 rebuild
- With wheel set to 1

* Tue Oct 13 2015 Robert Kuska <rkuska@redhat.com> - 7.1.0-2
- Rebuilt for Python3.5 rebuild

* Wed Jul 01 2015 Slavek Kabrda <bkabrda@redhat.com> - 7.1.0-1
- Update to 7.1.0

* Tue Jun 30 2015 Ville Skyttä <ville.skytta@iki.fi> - 7.0.3-3
- Install bash completion
- Ship LICENSE.txt as %%license where available

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 7.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Jun 04 2015 Matej Stuchlik <mstuchli@redhat.com> - 7.0.3-1
- Update to 7.0.3

* Fri Mar 06 2015 Matej Stuchlik <mstuchli@redhat.com> - 6.0.8-1
- Update to 6.0.8

* Thu Dec 18 2014 Slavek Kabrda <bkabrda@redhat.com> - 1.5.6-5
- Only enable tests on Fedora.

* Mon Dec 01 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-4
- Add tests
- Add patch skipping tests requiring Internet access

* Tue Nov 18 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-3
- Added patch for local dos with predictable temp dictionary names
  (http://seclists.org/oss-sec/2014/q4/655)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file 
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

