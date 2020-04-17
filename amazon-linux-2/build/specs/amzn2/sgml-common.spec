%global xmlxsdver 2009/01

Name: sgml-common
Version: 0.6.3
Release: 39%{?dist}
Group: Applications/Text

Summary: Common SGML catalog and DTD files

License: GPL+

BuildArch: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#Actually - there is no homepage of this project, on that URL
#page you could get complete ISO 8879 listing as was on the
#old page - only part of it is included in sgml-common package.
URL: http://www.w3.org/2003/entities/

Source0: ftp://sources.redhat.com/pub/docbook-tools/new-trials/SOURCES/%{name}-%{version}.tgz
# Following 4 from openjade/pubtext - same maintainer as in SGML-common, so up2date:
Source1: xml.dcl
Source2: xml.soc
Source3: html.dcl
Source4: html.soc
Source5: http://www.w3.org/%{xmlxsdver}/xml.xsd

Patch0: sgml-common-umask.patch
Patch1: sgml-common-xmldir.patch
Patch2: sgml-common-quotes.patch

BuildRequires: libxml2
BuildRequires: automake
Requires: /bin/basename

%description
The sgml-common package contains a collection of entities and DTDs
that are useful for processing SGML, but that don't need to be
included in multiple packages.  Sgml-common also includes an
up-to-date Open Catalog file.

%package -n xml-common
Group: Applications/Text
Summary: Common XML catalog and DTD files
License: GPL+
Requires(pre): %{_bindir}/xmlcatalog

%description -n xml-common
The xml-common is a subpackage of sgml-common which contains
a collection XML catalogs that are useful for processing XML,
but that don't need to be included in main package.

%prep
%setup -q
%patch0 -p1 -b .umask
%patch1 -p1 -b .xmldir
%patch2 -p1 -b .quotes

# replace bogus links with files
automakedir=`ls -1d /usr/share/automake* | head -n +1`
for file in COPYING INSTALL install-sh missing mkinstalldirs; do
   rm $file
   cp -p $automakedir/$file .
done

%build
%configure

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR="$RPM_BUILD_ROOT" htmldir='%{_datadir}/doc' INSTALL='install -p'
mkdir $RPM_BUILD_ROOT%{_sysconfdir}/xml
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sgml/docbook
mkdir -p $RPM_BUILD_ROOT%{_datadir}/sgml/docbook
# Touch SGML catalog
touch $RPM_BUILD_ROOT%{_sysconfdir}/sgml/catalog
# Create an empty XML catalog.
XMLCATALOG=$RPM_BUILD_ROOT%{_sysconfdir}/xml/catalog
%{_bindir}/xmlcatalog --noout --create $XMLCATALOG
# ...and add xml.xsd in it
for type in system uri ; do
	for path in 2001 %{xmlxsdver} ; do
		%{_bindir}/xmlcatalog --noout --add $type \
			"http://www.w3.org/$path/xml.xsd" \
			"file://%{_datadir}/xml/xml.xsd" $XMLCATALOG
	done
done
# Now put the common DocBook entries in it
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//ENTITIES DocBook XML" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"ISO 8879:1986" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegateSystem" \
	"http://www.oasis-open.org/docbook/" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
%{_bindir}/xmlcatalog --noout --add "delegateURI" \
	"http://www.oasis-open.org/docbook/" \
	"file://%{_sysconfdir}/sgml/docbook/xmlcatalog" $XMLCATALOG
# Also create the common DocBook catalog
%{_bindir}/xmlcatalog --noout --create \
	$RPM_BUILD_ROOT%{_sysconfdir}/sgml/docbook/xmlcatalog
ln -sf %{_sysconfdir}/sgml/docbook/xmlcatalog\
	$RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xmlcatalog

rm -f $RPM_BUILD_ROOT%{_datadir}/sgml/xml.dcl
install -p -m0644 %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} \
	$RPM_BUILD_ROOT%{_datadir}/sgml
rm -rf $RPM_BUILD_ROOT%{_datadir}/xml/*
install -p -m0644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/xml

# remove installed doc file and prepare installation with %%doc
rm $RPM_BUILD_ROOT%{_datadir}/doc/*.html
rm -rf __dist_doc/html/
mkdir -p __dist_doc/html/
cp -p doc/HTML/*.html __dist_doc/html/


%clean
rm -rf $RPM_BUILD_ROOT

%pre -n xml-common
if [ $1 -gt 1 ] && [ -e %{_sysconfdir}/xml/catalog ]; then
	for type in system uri ; do
		for path in 2001 %{xmlxsdver} ; do
			%{_bindir}/xmlcatalog --noout --add $type \
				"http://www.w3.org/$path/xml.xsd" \
				"file://%{_datadir}/xml/xml.xsd" \
				%{_sysconfdir}/xml/catalog
		done
	done
fi

%files
%defattr (-,root,root, -)
%doc __dist_doc/html/ AUTHORS NEWS ChangeLog COPYING README
%dir %{_sysconfdir}/sgml
%config(noreplace) %{_sysconfdir}/sgml/sgml.conf
%ghost %verify(not md5 size mtime) %config(noreplace,missingok) %{_sysconfdir}/sgml/catalog
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/sgml-iso-entities-8879.1986
%{_datadir}/sgml/sgml-iso-entities-8879.1986/*
%{_datadir}/sgml/xml.dcl
%{_datadir}/sgml/xml.soc
%{_datadir}/sgml/html.dcl
%{_datadir}/sgml/html.soc
%{_bindir}/sgmlwhich
%{_bindir}/install-catalog
%{_mandir}/man8/install-catalog.8*

%files -n xml-common
%defattr (-,root,root,-)
%doc AUTHORS NEWS ChangeLog COPYING README
%dir %{_sysconfdir}/xml
%dir %{_sysconfdir}/sgml/docbook
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/xml/catalog
%config(noreplace) %verify(not md5 size mtime) %{_sysconfdir}/sgml/docbook/xmlcatalog
%dir %{_datadir}/sgml
%dir %{_datadir}/sgml/docbook
%{_datadir}/sgml/docbook/xmlcatalog
%dir %{_datadir}/xml
%{_datadir}/xml/xml.xsd

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.6.3-39
- Mass rebuild 2013-12-27

* Thu Oct 11 2012 Ondrej Vasik <ovasik@redhat.com> 0.6.3-38
- get rid of the explicit automake14 requirement

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-36
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sun Oct 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 0.6.3-35
- Include xml.xsd in xml-common (#750073).

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-34
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Jul 12 2010 Ondrej Vasik <ovasik@redhat.com> 0.6.3-33
- ship COPYING file with both sgml-common and xml-common
- ship documentation with xml-common

* Fri Jan 14 2010 Ondrej Vasik <ovasik@redhat.com> 0.6.3-32
- Merge review #226415: remove unapplied patches, remove
  versioned BR

* Wed Nov 11 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.3-31
- apply quotes patch once again (accidently deleted in Nov07-#533058)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu May 28 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.3-29
- do own /etc/sgml/catalog

* Tue May 19 2009 Ondrej Vasik <ovasik@redhat.com> 0.6.3-28
- do not provide explicit url for xml-common subpackage,
  fix trailing spaces
- add Requires: /bin/basename (#501360)

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.6.3-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Aug 07 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.3-26
- /etc/sgml/docbook dir now owned by package(#458230)
- get rid off fuzz in patches

* Tue Jul 01 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.3-25
- mark xmlcatalog config(noreplace) to prevent overwriting
  of the content, move it to sysconfdir and make symlink for
  it to silence rpmlint

* Mon Jun 30 2008 Ondrej Vasik <ovasik@redhat.com> 0.6.3-24
- mark catalog files as (not md5 size mtime) for verify to
  prevent info about changed files (#453271)

* Thu Nov 22 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.3-23
- Another MergeReview improvements(provided by Patrice Dumas)
- copy Automake-1.4 files instead of rerunning autotools,
- better preserving timestamps, better handling of documentation
- improved XML-common description

* Thu Nov 15 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.3-22
- Merge Review(226415)
- changed: License Tag, using RPM macros instead of hardcoded
  dirs, summary ended with dot, added URL, removed CHANGES
  file as obsolete, preserved timestamps and some other cosmetic
  changes
- no longer shipping old automake tarball, fixed issue with man8_DATA,
  BuildRequire:Automake,Autoconf again(see MergeReview discussion)

* Mon May 28 2007 Ondrej Vasik <ovasik@redhat.com> 0.6.3-21
- Fixed broken URL (changed to XML entity declarations) (bug #237726)
- Rebuilt

* Tue May 15 2007 Tim Waugh <twaugh@redhat.com> 0.6.3-20
- Added dist tag.
- Fixed summary.
- Removed build dependency on autoconf/automake.

* Tue Oct 24 2006 Tim Waugh <twaugh@redhat.com> 0.6.3-19
- Removed stale URL (bug #210848).

* Mon Jun 12 2006 Tim Waugh <twaugh@redhat.com> 0.6.3-18
- Build requires automake and autoconf (bug #194709).

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Wed Sep 22 2004 Than Ngo <than@redhat.com> 0.6.3-17
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Dec  8 2003 Tim Waugh <twaugh@redhat.com> 0.6.3-15
- Patch from Ville Skyttä <ville.skytta@iki.fi> (bug #111625):
  - Include /usr/share/xml in xml-common.
  - Own /usr/share/sgml and /usr/share/xml.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Oct 23 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-13
- Ship the installed documentation.
- Don't install files not packaged.

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 24 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-10
- Ship {xml,html}.{dcl,soc} (bug #63500, bug #62980).
- Work around broken tarball packaging.

* Thu Feb 21 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-9
- Rebuild in new environment.

* Thu Jan 17 2002 Tim Waugh <twaugh@redhat.com> 0.6.3-8
- Back to /usr/share/sgml.  Now install docbook-dtds.
- Use a real install-sh, not the symlink shipped in the tarball.

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 0.6.3-7
- automated rebuild

* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-6
- Don't create a useless empty catalog.
- Don't try to put install things outside the build root.
- Build requires a libxml2 that actually works.

* Mon Nov  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-4
- Use (and handle) catalog files with quotes in install-catalog.

* Thu Nov  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-3
- Create default XML Catalog at build time, not install time.

* Fri Oct  5 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-2
- Move XML things into /usr/share/xml, and split them out into separate
  xml-common package.

* Mon Oct  1 2001 Tim Waugh <twaugh@redhat.com> 0.6.3-1
- 0.6.3.  Incorporates oldsyntax and quiet patches.
- Make /etc/sgml/sgml.conf noreplace.
- Own /etc/sgml, various other directories (bug #47485, bug #54180).

* Wed May 23 2001 Tim Waugh <twaugh@redhat.com> 0.5-7
- Remove execute bit from data files.

* Mon May 21 2001 Tim Waugh <twaugh@redhat.com> 0.5-6
- install-catalog needs to make sure that it creates world-readable files
  (bug #41552).

* Wed Mar 14 2001 Tim Powers <timp@redhat.com> 0.5-5
- fixed license

* Wed Jan 24 2001 Tim Waugh <twaugh@redhat.com>
- Make install-catalog quieter during normal operation.

* Tue Jan 23 2001 Tim Waugh <twaugh@redhat.com>
- Require textutils, fileutils, grep (bug #24719).

* Wed Jan 17 2001 Tim Waugh <twaugh@redhat.com>
- Require sh-utils.

* Mon Jan 15 2001 Tim Waugh <twaugh@redhat.com>
- Don't play so many macro games.
- Fix typo in install-catalog patch.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Change group.
- Install by hand (man/en/...).  Use %%{_mandir}.
- Use %%{_tmppath}.
- Make install-catalog fail silently if given the old syntax.
- Add CHANGES file.
- Change Copyright: to License:.
- Remove Packager: line.

* Mon Jan 08 2001 Tim Waugh <twaugh@redhat.com>
- Based on Eric Bischoff's new-trials packages.
