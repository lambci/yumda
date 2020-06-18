Name:		oniguruma
Version:	6.8.2
Release:	1%{?dist}
Summary:	Regular expressions library

Group:		System Environment/Libraries
License:	BSD
URL:		https://github.com/kkos/oniguruma/
Source0:	https://github.com/kkos/oniguruma/releases/download/v%{version}/onig-%{version}.tar.gz

%description
Oniguruma is a regular expressions library.
The characteristics of this library is that different character encoding
for every regular expression object can be specified.
(supported APIs: GNU regex, POSIX and Oniguruma native)


%package	devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name}%{?isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q -n onig-%{version}
%{__sed} -i.multilib -e 's|-L@libdir@||' onig-config.in

%if 0
for f in \
	README.ja \
	doc/API.ja \
	doc/FAQ.ja \
	doc/RE.ja
	do
	iconv -f EUC-JP -t UTF-8 $f > $f.tmp && \
		( touch -r $f $f.tmp ; %{__mv} -f $f.tmp $f ) || \
		%{__rm} -f $f.tmp
done
%endif

%build
%configure \
    --disable-silent-rules \
	--disable-static \
	--with-rubydir=%{_bindir}
%{__make} %{?_smp_mflags}


%install
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL="%{__install} -c -p"
find $RPM_BUILD_ROOT -name '*.la' \
	-exec %{__rm} -f {} ';'

%check
%{__make} check

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc	AUTHORS
%license	COPYING
%doc	HISTORY
%doc	README.md
%doc	index.html
%lang(ja)	%doc	README_japanese
%lang(ja)	%doc	index_ja.html

%{_libdir}/libonig.so.5*

%files devel
%defattr(-,root,root,-)
%doc	doc/API
%doc	doc/CALLOUTS.API
%doc	doc/CALLOUTS.BUILTIN
%doc	doc/FAQ
%doc	doc/RE
%lang(ja)	%doc	doc/API.ja
%lang(ja)	%doc	doc/CALLOUTS.API.ja
%lang(ja)	%doc	doc/CALLOUTS.BUILTIN.ja
%lang(ja)	%doc	doc/FAQ.ja
%lang(ja)	%doc	doc/RE.ja

%{_bindir}/onig-config

%{_libdir}/libonig.so
%{_includedir}/onig*.h
%{_libdir}/pkgconfig/%{name}.pc	

%changelog
* Tue May 26 2020 Carl George <carl@george.computer> - 6.8.2-1
- Rebase to 6.8.2 rhbz#1777660

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Nov 11 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.5-1
- 5.9.5

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.4-1
- 5.9.4

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jan  4 2013 Mamoru TASAKA <mtasaka@fedoraproject.org> - 5.9.3-1
- 5.9.3

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan  5 2012 Mamoru Tasaka <mtasaka@fedoraproject.org> - 5.9.2-3
- F-17: rebuild against gcc47

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.9.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 15 2010 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.2-1
- 5.9.2

* Sat Jul 25 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-3
- F-12: Mass rebuild

* Tue Feb 24 2009 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-2
- F-11: Mass rebuild

* Sat Feb  9 2008 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp>
- Rebuild against gcc43

* Thu Dec 27 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.1-1
- 5.9.1

* Wed Dec  5 2007 Mamoru Tasaka <mtasaka@ioa.s.u-tokyo.ac.jp> - 5.9.0-1
- Initial packaging

