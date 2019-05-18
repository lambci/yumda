Name:           libvoikko
Version:        4.1.1
Release: 1%{?dist}
Summary:        Voikko is a library for spellcheckers and hyphenators

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://voikko.sourceforge.net/
# The usual format of stable release URLs
Source0:        https://www.puimula.org/voikko-sources/libvoikko/%{name}-%{version}.tar.gz
# The usual format of test release URLs
#Source0:        http://www.puimula.org/htp/testing/%%{name}-%%{version}rc1.tar.gz

BuildRequires:  python2-devel
# Require the Finnish morphology because Finnish is currently the only language
# supported by libvoikko in Fedora.
Requires:       malaga-suomi-voikko

Prefix: %{_prefix}

%description
This is libvoikko, library for spellcheckers and hyphenators using Malaga
natural language grammar development tool. The library is written in C.

Currently only Finnish is supported, but the API of the library has been
designed to allow adding support for other languages later. Note however that
Malaga is rather low level tool that requires implementing the whole morphology
of a language as a left associative grammar. Therefore languages that have
simple or even moderately complex morphologies and do not require morphological
analysis in their hyphenators should be implemented using other tools such as
Hunspell.

%package -n     voikko-tools
Summary:        Test tools for %{name}
Group:          Applications/Text
Requires:       %{name}%{?_isa} = %{version}-%{release}
Prefix: %{_prefix}

%description -n voikko-tools
This package contains voikkospell and voikkohyphenate, small command line
tools for testing libvoikko. These tools may also be useful for shell
scripts.


%prep
%setup -q


%build
# The dictionary path must be the same where malaga-suomi-voikko is installed
%configure --with-dictionary-path=%{_libdir}/voikko --disable-hfst
# Remove rpath,
# https://fedoraproject.org/wiki/Packaging/Guidelines#Removing_Rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
make %{?_smp_mflags}


%install
make install INSTALL="install -p" DESTDIR=$RPM_BUILD_ROOT


%files
%license COPYING
%{_libdir}/*.so.*

%files -n voikko-tools
%{_bindir}/voikkospell
%{_bindir}/voikkohyphenate
%{_bindir}/voikkogc
%{_bindir}/voikkovfstc

%exclude %{_mandir}
%exclude %{_includedir}
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
# %{python_sitelib}/%{name}.py*

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org> - 4.1.1-1
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 3.6-5
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 3.6-4
- Mass rebuild 2013-12-27

* Mon Jul 29 2013 Parag <paragn AT fedoraproject DOT org> - 3.6-2
- Ah don't add %%{?_isa} for noarch packages

* Mon Jul 29 2013 Parag <paragn AT fedoraproject DOT org> - 3.6-2
- Fix spec file to follow packaging guidelines

* Sun Apr 14 2013 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.6-1
- New upstream release

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sun Jul 01 2012 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.5-1
- New upstream release

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4.1-2
- Rebuilt for c++ ABI breakage

* Sat Feb 04 2012 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.4.1-1
- New upstream release, fixes build with GCC 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 27 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.4-1
- Update to the latest upstream release:
- A crash bug affecting grammar checker has been fixed.
- New grammar checker rule for missing verbs has been added.

* Sun Sep 25 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3.1-0.3.rc1
- Remove the isa macro from the malaga-suomi-voikko dependency,
  malaga-suomi-voikko is not a library and is thus not multilib'd. The previous
  change was a misunderstanding.

* Sat Sep 24 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3.1-0.2.rc1
- Add the isa macro to the malaga-suomi-voikko dependency and drop the version.

* Sat Sep 24 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3.1-0.1.rc1
- New upstream release candidate, fixes a bug which crashed Firefox when
  using Finnish spell checking.

* Fri Sep 16 2011 Ville-Pekka Vainio <vpvainio AT iki.fi> - 3.3-1
- New upstream release

* Sun Jun 12 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.2.1-1
- New upstream release
- Fixes handling of embedded null characters in input strings entered through
  Python or Java interfaces.

* Fri Mar 25 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.2-1
- New upstream release

* Tue Feb 15 2011 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-3
- Add patch to fix build with GCC 4.6

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov 22 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.1-1
- New upstream release
- Remove the unneeded %%clean section, not needed in Fedora >= 13

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 3.0-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Thu May 27 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-1
- 3.0 final

* Thu May 13 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 3.0-0.1.rc1
- New upstream release candidate with multithread support
- Remove unneeded BuildRoot tag

* Thu Feb 18 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.3.1-1
- Version 2.3.1 contains fixes for bugs found in version 2.3

* Sun Jan 31 2010 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.3-0.1.rc1
- New release candidate
- Dependency on glib has been removed

* Wed Nov 11 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2.2-1
- Version 2.2.2 fixes a crash found in version 2.2.1 that can occur when the
  APIs that use wchar_t strings as arguments are used.

* Mon Oct 26 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2.1-2
- Add Python interface (package python-libvoikko, noarch)

* Fri Oct 09 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2.1-1
- New upstream release, fixes bugs found in 2.2

* Fri Sep 18 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.3.rc2
- 2.2rc2
- Remove getcwd() value check patch, accepted upstream

* Wed Sep 16 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.2.rc1
- Remove rpath which was set for the voikko-tools binaries in 64 bit
  architechtures

* Tue Sep 15 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.2-0.1.rc1
- New release candidate
- Improvements to spelling suggestions, grammar checker etc.
- Libvoikko now uses its own internal implementation of malaga.
- This prevents symbol conflicts such as https://bugzilla.redhat.com/502546
- BuildRequires malaga removed and glib2-devel added.
- Require malaga-suomi-voikko >= 1.4, libvoikko 2.2 expects the newer
  dictionary format
- Add a patch to make it compile on Fedora with -Werror

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sat May 2 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-1
- 2.1 final, including fixes to grammar checking

* Fri Apr 17 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.5.rc4
- 2.1rc4:
  - Fix invalid use of delete vs. delete[]
  - Limit the scope of some variables

* Mon Apr 13 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.4.rc3
- 2.1rc3, remove patch

* Sat Apr 11 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.3.rc2
- Patch to current SVN HEAD, includes a fix for a memory leak in the grammar
  checker

* Mon Apr 6 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.2.rc2
- New release candidate
- Both patches applied upstream

* Mon Apr 6 2009 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.1-0.1.rc1
- New release candidate
- Improvements on grammar checking and dictionary loading
- Raise malaga-suomi-voikko dependency to 1.3-10, which has the new dictionary
  data directory layout needed by this version of libvoikko
- Add BuildRequires python for running the trie compiler during build
- Add patch for GCC 4.4 and glibc 2.90 compliance
- Add patch to fix warn_unused_result errors

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 28 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.0-1
- libvoikko 2.0

* Sat Aug 23 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 2.0-0.1.rc1
- New release candidate, including the new voikkogc tool in voikko-tools
- Add defattr to voikko-tools
- Drop upstreamed pkg-config patch

* Fri May 30 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-3
- Add Requires pkgconfig to -devel

* Mon May 26 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-2
- Add patch which makes a libvoikko.pc file for pkg-config

* Sat May 24 2008 Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> - 1.7-1
- libvoikko 1.7

* Thu May 22 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.7-0.2.rc2
- Don't BuildRequire the Finnish data files, this should make Koji builds a bit
  quicker

* Sun May 11 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.7-0.1.rc2
- New release candidate

* Sun Mar 02 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-3
- Put voikkospell and voikkohyphenate into a separate voikko-tools
  subpackage to decrease the size of the binary libvoikko package

* Sat Feb 16 2008 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-2
- Rebuild for GCC 4.3

* Tue Dec 04 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-1
- libvoikko 1.6
- Add versioned BuildRequires and Requires as per the Voikko release notes
  at http://voikko.sourceforge.net/releases.html

* Mon Dec 03 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.4.rc4
- Upstream released a new release candidate

* Wed Nov 28 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.3.rc3
- Upstream released a new release candidate

* Wed Nov 28 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.2.rc2
- Upstream released a new release candidate

* Tue Nov 27 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.6-0.1.rc1
- Upstream released a new release candidate

* Thu Nov 08 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-1
- Bump Release for the first Fedora build

* Wed Nov 07 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-0.3
- libvoikko-devel: remove unneeded Requires: malaga-devel
- install with -p so that timestamps are preserved

* Wed Nov 07 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-0.2
- Requires only malaga-suomi-voikko, BR malaga-devel and malaga-suomi-voikko
- Remove static archive

* Wed Oct 24 2007 - Ville-Pekka Vainio <vpivaini AT cs.helsinki.fi> 1.5-0.1
- Initial package
