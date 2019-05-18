Summary: Fonts for the Ghostscript PostScript interpreter
Name: ghostscript-fonts
Version: 5.50
Release: 32%{?dist}
# Contacted Kevin Hartig, who agreed to relicense his fonts under the SIL Open Font 
# License. Hershey fonts are under the "Hershey Font License", which is not what Fontmap 
# says (Fontmap is wrong).
License: GPLv2+ and Hershey and MIT and OFL and Public Domain
Group: Applications/Publishing
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
URL: http://www.gnu.org/software/ghostscript/
Source0: gnu-gs-fonts-other-%{version}-nobch.tar.gz
Source1: Kevin_Hartig-Font_License.txt
Source2: SIL-Open-Font-License.txt
# gnu-gs-fonts-other-5.50 contains fonts with a non-free license (bug #690593).
# Therefore we use this script to remove those fonts before shipping
# it.  Download the upstream tarball (from
# http://ftp.gnu.org/gnu/ghostscript/) and invoke this script while in
# the tarball's directory:
# ./generate-tarball.sh 5.50
Source3: generate-tarball.sh
Requires: fontconfig
Requires(post): fontconfig
Requires(postun): fontconfig
BuildArchitectures: noarch

%define fontdir %{_datadir}/fonts/default/ghostscript

Prefix: %{_prefix}

%description
Ghostscript-fonts contains a set of fonts that Ghostscript, a
PostScript interpreter, uses to render text. These fonts are in
addition to the fonts shared by Ghostscript and the X Window System.

%prep
%setup -q -c ghostscript-fonts-%{version}
cp -p %{SOURCE1} %{SOURCE2} .

# Remove Hershey fonts as they cause problems (bug #707007).
find fonts -type f | xargs grep -lw Hershey | xargs rm -f

%build

%install
mkdir -p $RPM_BUILD_ROOT%{fontdir}
cp -p fonts/* $RPM_BUILD_ROOT%{fontdir}

%post
{
   fc-cache %{fontdir}
} &> /dev/null || :

%postun
{
   if [ "$1" = "0" ]; then
      fc-cache %{fontdir}
   fi
} &> /dev/null || :

%files
%defattr(-,root,root,-)
%license Kevin_Hartig-Font_License.txt SIL-Open-Font-License.txt
%{_datadir}/fonts/default/

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 5.50-32
- Mass rebuild 2013-12-27

* Wed Nov  6 2013 Tim Waugh <twaugh@redhat.com> - 5.50-31
- Run fc-cache on our font directory, not the entire font collection
  (bug #1023977).

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.50-30
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.50-29
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.50-28
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Tim Waugh <twaugh@redhat.com> 5.50-27
- Removed Hershey fonts as they cause problems (bug #707007).

* Mon May 30 2011 Ville Skyttä <ville.skytta@iki.fi> - 5.50-26
- Own %%ghosted fonts.dir and fonts.scale.

* Fri Mar 25 2011 Tim Waugh <twaugh@redhat.com> 5.50-25
- Removed non-free fonts (bug #690593).

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.50-24
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.50-23
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jun 10 2009 Tim Waugh <twaugh@redhat.com> 5.50-22
- Further changes from package review (bug #225794):
  - Don't use umask in scriptlet.
  - Don't use 'which' in scriptlet.

* Wed Jun 10 2009 Tim Waugh <twaugh@redhat.com> 5.50-21
- Changes from package review (bug #225794):
  - Requires xorg-x11-font-utils, not mkfontscale/mkfontdir.
  - Use macro for /etc.
  - Don't own catalogue directory.

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.50-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Jul 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 5.50-19
- fix license tag
- add licensing information for fhirw* and fkarw* fonts

* Fri Aug 10 2007 Kristian Høgsberg <krh@redhat.com> - 5.50-18
- Change link name to be default-ghostscript.

* Tue Jun 26 2007 Kristian Høgsberg <krh@redhat.com> - 5.50-17
- Drop chkfontpath dependency and use the catalogue font path mechanism.

* Wed Feb  7 2007 Tim Waugh <twaugh@redhat.com> 5.50-16
- Fixed URL again (bug #225794).
- Fixed requires tags (bug #225794).
- Preserve timestamps on installed files (bug #225794).
- Added empty %%build section (bug #225794).
- Use FHS macros for file manifest (bug #225794).
- Fixed summary (bug #225794).
- Fixed description (bug #225794).
- Fixed license (bug #225794).

* Tue Feb  6 2007 Tim Waugh <twaugh@redhat.com> 5.50-15
- Fixed URL (bug #225794).
- Fixed build root tag (bug #225794).
- This package does not require ghostscript (bug #225794).

* Fri Dec 15 2006 Tim Waugh <twaugh@redhat.com> 5.50-14
- Copied post/postun scriptlets from urw-fonts (bug #203369).

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 5.50-13.1.1
- rebuild

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Fri Sep  3 2004 Tim Waugh <twaugh@redhat.com> 5.50-13
- Own /usr/share/fonts/default (bug #131650).

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Thu Jan 22 2004 Tim Waugh <twaugh@redhat.com> 5.50-10
- Rebuilt. (The 8.11 package which briefly appeared in rawhide should
  not be used.)  Bug #99323, bug #113866.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Nov 20 2002 Tim Powers <timp@redhat.com>
- rebuild in latest collinst

* Mon Sep  2 2002 Owen Taylor <otaylor@redhat.com>
- Run /usr/bin/fc-cache in the %%post

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Matt Wilson <msw@redhat.com>
- rebuild for next release

* Mon Feb 14 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- 5.50

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Wed Jan 13 1999 Preston Brown <pbrown@redhat.com>
- renamed package to be consistent with new ghostscript.

* Fri Nov 13 1998 Preston Brown <pbrown@redhat.com>
- removed the std fonts...now shared between X11 and gs with URW fonts pkg.

* Thu Jul  2 1998 Jeff Johnson <jbj@redhat.com>
- update to 4.03.

* Mon May 04 1998 Erik Troan <ewt@redhat.com>
- set the owner and group of all of the files to 0.0

* Tue Sep 23 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
