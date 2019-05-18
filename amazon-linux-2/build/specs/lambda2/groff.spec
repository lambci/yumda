Summary: A document formatting system
Name: groff
Version: 1.22.2
Release: 8%{?dist}.0.2
License: GPLv3+ and GFDL and BSD and MIT
Group: Applications/Publishing
URL: http://www.gnu.org/software/groff/
Source: ftp://ftp.gnu.org/gnu/groff/groff-%{version}.tar.gz
# resolves: #530788
Patch0: 0001-missing-groff-x11-info-message-when-gxditview-not-fo.patch
Patch1: 0002-load-site-font-and-site-tmac-from-etc-groff.patch
# resolves: #709413, #720058, #720057
Patch2: 0003-various-security-fixes.patch
# resolves: #987069
Patch3: 0004-don-t-use-usr-bin-env-in-shebang.patch

Requires: coreutils, /sbin/install-info, groff-base = %{version}-%{release}
BuildRequires: git, netpbm-progs, psutils, ghostscript
Provides: nroff-i18n = %{version}-%{release}

Prefix: %{_prefix}

%description
Groff is a document formatting system. Groff takes standard text and
formatting commands as input and produces formatted output. The
created documents can be shown on a display or printed on a printer.
Groff's formatting commands allow you to specify font type and size,
bold type, italic type, the number and size of columns on a page, and
more.

Groff can also be used to format man pages. If you are going to use
groff with the X Window System, you will also need to install the
groff-x11 package.

%package base
Summary: Parts of the groff formatting system required to display manual pages
Group: Applications/Publishing
Prefix: %{_prefix}

%description base
The groff-base package contains only necessary parts of groff formatting
system which are required to display manual pages, and the groff's default
display device (PostScript).

%package perl
Summary: Parts of the groff formatting system that require Perl
Group: Applications/Publishing
Requires: groff-base = %{version}-%{release}
Prefix: %{_prefix}

%description perl
The groff-perl package contains the parts of the groff text processor
package that require Perl. These include the afmtodit (font processor
for creating PostScript font files), groffer (tool for displaying groff
files), grog (utility that can be used to automatically determine groff
command-line options), chem (groff preprocessor for producing chemical
structure diagrams), mmroff (reference preprocessor) and roff2dvi
roff2html roff2pdf roff2ps roff2text roff2x (roff code converters).

%prep
%setup -q
git init
git config user.email groff-owner@fedoraproject.org
git config user.name "groff owner"
git add .
git commit -n -m "release %{version}"
git am %{patches}

for file in NEWS src/devices/grolbp/grolbp.man doc/{groff.info*,webpage.ms} \
                contrib/mm/*.man contrib/mom/examples/{README.txt,*.mom,mom.vim}; do
    iconv -f iso-8859-1 -t utf-8 < "$file" > "${file}_"
    mv "${file}_" "$file"
done

%build
%configure \
    --docdir=%{_docdir}/%{name}-%{version} \
    --without-x \
    --with-grofferdir=%{_datadir}/%{name}/%{version}/groffer

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# some binaries need alias with 'g' or 'z' prefix
for file in g{nroff,troff,tbl,pic,eqn,neqn,refer,lookbib,indxbib,soelim} zsoelim; do
    ln -s ${file#?} %{buildroot}%{_bindir}/${file}
done

# rename groff downloadable postscript fonts to meet Fedora Font Packaging guidelines,
# as these files are more PS instructions, than general-purpose fonts (bz #477394)
for file in $(find %{buildroot}%{_datadir}/%{name}/%{version}/font/devps -name "*.pfa"); do
    mv ${file} ${file}_
done
sed --in-place 's/\.pfa$/.pfa_/' %{buildroot}%{_datadir}/%{name}/%{version}/font/devps/download

# fix privileges
chmod 755 %{buildroot}%{_datadir}/groff/%{version}/groffer/version.sh
chmod 755 %{buildroot}%{_datadir}/groff/%{version}/font/devlj4/generate/special.awk

sed -i '1 s|/usr/bin/perl|%{_bindir}/perl|' %{buildroot}%{_bindir}/*


%files
# data
%{_datadir}/%{name}/%{version}/font/devdvi/
%{_datadir}/%{name}/%{version}/font/devlbp/
%{_datadir}/%{name}/%{version}/font/devlj4/
%{_datadir}/%{name}/%{version}/oldfont/
%{_datadir}/%{name}/%{version}/pic/
%{_datadir}/%{name}/%{version}/tmac/62bit.tmac
%{_datadir}/%{name}/%{version}/tmac/a4.tmac
%{_datadir}/%{name}/%{version}/tmac/dvi.tmac
%{_datadir}/%{name}/%{version}/tmac/e.tmac
%{_datadir}/%{name}/%{version}/tmac/ec.tmac
%{_datadir}/%{name}/%{version}/tmac/hdmisc.tmac
%{_datadir}/%{name}/%{version}/tmac/hdtbl.tmac
%{_datadir}/%{name}/%{version}/tmac/lbp.tmac
%{_datadir}/%{name}/%{version}/tmac/lj4.tmac
%{_datadir}/%{name}/%{version}/tmac/m.tmac
%{_datadir}/%{name}/%{version}/tmac/me.tmac
%{_datadir}/%{name}/%{version}/tmac/mm.tmac
%{_datadir}/%{name}/%{version}/tmac/mm/
%{_datadir}/%{name}/%{version}/tmac/mmse.tmac
%{_datadir}/%{name}/%{version}/tmac/mom.tmac
%{_datadir}/%{name}/%{version}/tmac/ms.tmac
%{_datadir}/%{name}/%{version}/tmac/mse.tmac
%{_datadir}/%{name}/%{version}/tmac/om.tmac
%{_datadir}/%{name}/%{version}/tmac/pdfmark.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-me.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-mm.tmac
%{_datadir}/%{name}/%{version}/tmac/refer-ms.tmac
%{_datadir}/%{name}/%{version}/tmac/refer.tmac
%{_datadir}/%{name}/%{version}/tmac/s.tmac
%{_datadir}/%{name}/%{version}/tmac/spdf.tmac
%{_datadir}/%{name}/%{version}/tmac/trace.tmac
# programs
%{_bindir}/addftinfo
%{_bindir}/eqn2graph
%{_bindir}/gdiffmk
%{_bindir}/grap2graph
%{_bindir}/grn
%{_bindir}/grodvi
%{_bindir}/grolbp
%{_bindir}/grolj4
%{_bindir}/hpftodit
%{_bindir}/indxbib
%{_bindir}/lkbib
%{_bindir}/lookbib
%{_bindir}/pdfroff
%{_bindir}/pfbtops
%{_bindir}/pic2graph
%{_bindir}/refer
%{_bindir}/tfmtodit
# compatibility symlinks
%{_bindir}/grefer
%{_bindir}/glookbib
%{_bindir}/gindxbib

%files base
%license COPYING FDL LICENSES
# configuration
%dir %{_sysconfdir}/groff/
%config(noreplace) %{_sysconfdir}/groff/*
# data
%dir %{_datadir}/%{name}/
%dir %{_datadir}/%{name}/%{version}/
%dir %{_datadir}/%{name}/%{version}/font/
%dir %{_datadir}/%{name}/%{version}/tmac/
%{_datadir}/%{name}/current
%{_datadir}/%{name}/%{version}/eign
%{_datadir}/%{name}/%{version}/font/devascii/
%{_datadir}/%{name}/%{version}/font/devlatin1/
%{_datadir}/%{name}/%{version}/font/devps/
%{_datadir}/%{name}/%{version}/font/devutf8/
%{_datadir}/%{name}/%{version}/font/devhtml/
%{_datadir}/%{name}/%{version}/tmac/an-ext.tmac
%{_datadir}/%{name}/%{version}/tmac/an-old.tmac
%{_datadir}/%{name}/%{version}/tmac/an.tmac
%{_datadir}/%{name}/%{version}/tmac/andoc.tmac
%{_datadir}/%{name}/%{version}/tmac/composite.tmac
%{_datadir}/%{name}/%{version}/tmac/cp1047.tmac
%{_datadir}/%{name}/%{version}/tmac/cs.tmac
%{_datadir}/%{name}/%{version}/tmac/de.tmac
%{_datadir}/%{name}/%{version}/tmac/den.tmac
%{_datadir}/%{name}/%{version}/tmac/devtag.tmac
%{_datadir}/%{name}/%{version}/tmac/doc-old.tmac
%{_datadir}/%{name}/%{version}/tmac/doc.tmac
%{_datadir}/%{name}/%{version}/tmac/eqnrc
%{_datadir}/%{name}/%{version}/tmac/europs.tmac
%{_datadir}/%{name}/%{version}/tmac/fallbacks.tmac
%{_datadir}/%{name}/%{version}/tmac/fr.tmac
%{_datadir}/%{name}/%{version}/tmac/html-end.tmac
%{_datadir}/%{name}/%{version}/tmac/html.tmac
%{_datadir}/%{name}/%{version}/tmac/hyphen.cs
%{_datadir}/%{name}/%{version}/tmac/hyphen.den
%{_datadir}/%{name}/%{version}/tmac/hyphen.det
%{_datadir}/%{name}/%{version}/tmac/hyphen.fr
%{_datadir}/%{name}/%{version}/tmac/hyphen.sv
%{_datadir}/%{name}/%{version}/tmac/hyphen.us
%{_datadir}/%{name}/%{version}/tmac/hyphenex.cs
%{_datadir}/%{name}/%{version}/tmac/hyphenex.det
%{_datadir}/%{name}/%{version}/tmac/hyphenex.us
%{_datadir}/%{name}/%{version}/tmac/ja.tmac
%{_datadir}/%{name}/%{version}/tmac/latin1.tmac
%{_datadir}/%{name}/%{version}/tmac/latin2.tmac
%{_datadir}/%{name}/%{version}/tmac/latin5.tmac
%{_datadir}/%{name}/%{version}/tmac/latin9.tmac
%{_datadir}/%{name}/%{version}/tmac/man.tmac
%{_datadir}/%{name}/%{version}/tmac/mandoc.tmac
%{_datadir}/%{name}/%{version}/tmac/mdoc.tmac
%{_datadir}/%{name}/%{version}/tmac/mdoc/
%{_datadir}/%{name}/%{version}/tmac/papersize.tmac
%{_datadir}/%{name}/%{version}/tmac/pic.tmac
%{_datadir}/%{name}/%{version}/tmac/ps.tmac
%{_datadir}/%{name}/%{version}/tmac/psatk.tmac
%{_datadir}/%{name}/%{version}/tmac/psold.tmac
%{_datadir}/%{name}/%{version}/tmac/pspic.tmac
%{_datadir}/%{name}/%{version}/tmac/safer.tmac
%{_datadir}/%{name}/%{version}/tmac/sv.tmac
%{_datadir}/%{name}/%{version}/tmac/trans.tmac
%{_datadir}/%{name}/%{version}/tmac/troffrc
%{_datadir}/%{name}/%{version}/tmac/troffrc-end
%{_datadir}/%{name}/%{version}/tmac/tty-char.tmac
%{_datadir}/%{name}/%{version}/tmac/tty.tmac
%{_datadir}/%{name}/%{version}/tmac/unicode.tmac
%{_datadir}/%{name}/%{version}/tmac/www.tmac
# programs
%{_bindir}/eqn
%{_bindir}/groff
%{_bindir}/grops
%{_bindir}/grotty
%{_bindir}/neqn
%{_bindir}/nroff
%{_bindir}/pic
%{_bindir}/post-grohtml
%{_bindir}/pre-grohtml
%{_bindir}/preconv
%{_bindir}/soelim
%{_bindir}/tbl
%{_bindir}/troff
# compatibility symlinks
%{_bindir}/gnroff
%{_bindir}/gtroff
%{_bindir}/gtbl
%{_bindir}/gpic
%{_bindir}/geqn
%{_bindir}/gneqn
%{_bindir}/gsoelim
%{_bindir}/zsoelim

%files perl
# data
%{_datadir}/%{name}/%{version}/font/devpdf/
%{_datadir}/%{name}/%{version}/groffer/
%{_datadir}/%{name}/%{version}/tmac/pdf.tmac
# programs
%{_bindir}/afmtodit
%{_bindir}/chem
%{_bindir}/groffer
%{_bindir}/grog
%{_bindir}/gropdf
%{_bindir}/mmroff
%{_bindir}/pdfmom
%{_bindir}/roff2dvi
%{_bindir}/roff2html
%{_bindir}/roff2pdf
%{_bindir}/roff2ps
%{_bindir}/roff2text
%{_bindir}/roff2x

%exclude %{_mandir}
%exclude %{_infodir}
%exclude %{_docdir}
%exclude %{_datadir}/X11
%exclude %{_datadir}/%{name}/%{version}/font/devX*/
%exclude %{_datadir}/%{name}/%{version}/tmac/X.tmac
%exclude %{_datadir}/%{name}/%{version}/tmac/Xps.tmac
%exclude %{_bindir}/gxditview
%exclude %{_bindir}/xtotroff

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.22.2-8
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.22.2-7
- Mass rebuild 2013-12-27

* Tue Jul 23 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-6
- don't use /usr/bin/env in shebang

* Mon Jul 22 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-5
- removed BSD and MIT license files - the text is already included
  in the upstream tarball

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 1.22.2-4
- Perl 5.18 rebuild

* Tue Jul  9 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-3
- added BSD and MIT license files

* Mon Mar 11 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-2
- resolves: #915682
  moved html device to the groff-base subpackage

* Tue Feb 12 2013 Peter Schiffer <pschiffe@redhat.com> 1.22.2-1
- resolves: #909154
  updated to 1.22.2
- cleaned .spec file

* Tue Jan 01 2013 Jan Vcelak <jvcelak@redhat.com> 1.22.1-1
- new upstream release (#890973)
  + various fixes in manual pages
  + various fixes and improvements in macros
  + new gropdf driver for generating PDF files
- fix: backslash-period escape does not work (#682857)
- fix: groff ftbfs - patch does not apply (#885225)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue May 29 2012 Jan Vcelak <jvcelak@redhat.com> 1.21-9
- older security fixes (#709415, #720060):
  + CVE-2009-5044: insecure temporary file handling in pdfroff
  + CVE-2009-5080: improper handling of failed attempts to create temporary directories in eqn2graph/pic2graph/grap2graph
  + CVE-2009-5081: roff2.pl and groffer.pl use easy-to-guess temporary file names

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Oct 12 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-7
- update: move local configuration from /usr/share/groff/site-* to /etc/groff/*
  (change the paths in the app instead of symlinking to avoid RPM issues)
- fix groff package: add install-info to %%post and %%preun

* Tue Oct 11 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-6
- fix build warnings: File listed twice

* Tue Sep 20 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-5
- fix #739318: fix upgrade from previous versions (workaround for RPM bug)

* Fri Sep 16 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-4
- new subpackage: groff-base (minimal for manual page rendering)
- move shared data used by gxditview to groff-x11 subpackage
- move groff reference manual to groff-doc subpackage
- make groff-doc an architecture independent package
- move local configuration from /usr/share/groff/site-* to /etc/groff/*

* Fri Jun 17 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-3
- fix #678572: groffer libdir is incorrect
- fix #709474: unowned groff doc dir
- fix #712904: Japanese bold/underline text not displayed correctly (Daiki Ueno <dueno@redhat.com>)

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Jan Vcelak <jvcelak@redhat.com> 1.21-1
- package rebase to 1.21

* Fri Nov 26 2010 Jan Vcelak <jvcelak@redhat.com> 1.20.1-3
- experimental support of Japanese (charclass and wcwidth patches)
  thanks to Daiki Ueno (dueno@redhat.com)

* Fri Jul 30 2010 Jan Vcelak <jvcelak@redhat.com> 1.20.1-2
- Resolves: #477394 - Please convert to new font packaging guidelines

* Fri Mar 19 2010 Jan Vcelak <jvcelak@redhat.com> - 1.20.1-1
- Resolves: #530788

* Tue Mar 12 2010 Jan Vcelak <jvcelak@redhat.com> - 1.20.1-0
- Package rebase to upstream 1.20.1

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.4-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.18.1.4-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Oct 19 2008 Robert Scheck <robert@fedoraproject.org> - 1.18.1.14-16
- Fixed wrong symlinking of man pages into %%{_bindir} after simplifying

* Mon Sep 29 2008 Stepan Kasal <skasal@redhat.com> - 1.18.1.14-15
- Replace groff-1.18-nohtml.patch by a code in spec file
- fix groff-1.18-gzip.patch to apply cleanly
- simplify the code for symlinking in %%install

* Wed Mar 26 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-14
- 175459 warning goes on stderr

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.18.1.4-13
- Autorebuild for GCC 4.3

* Wed Jan 23 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-12
- rewrite nroff for using -Tencoding with main support of utf8
- Resolves: rhbz#251064

* Thu Jan  3 2008 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-11
- fix for gcc4.3.0

* Mon Oct  8 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-10
- path for groffer wasn't set correctly #89210

* Mon Sep 17 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-9
- fix license

* Tue Sep 11 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-8
- another change in spec for review

* Thu Aug 16 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-7
- rebuild
- another encoding are print correct with nroff
- Resolves: rhbz#251064

* Mon Jul  2 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-5
- Resolves: rhbz#245934

* Tue Feb 27 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-4
- merge review
- rhbz#225859 review

* Mon Jan 22 2007 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-2
- changes in spec, remove patches groff-1.18.1.1-bigendian.patch, groff-xlibs.patch
 
* Mon Oct 23 2006 Marcela Maslanova <mmaslano@redhat.com> - 1.18.1.4-1
- new version from upstream - update groffer

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-11.1
- rebuild

* Wed Apr 26 2006 Adam Jackson <ajackson@redhat.com> - 1.18.1.1-11
- Rebuild for updated imake build rules.

* Thu Feb 16 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-10
- use mktemp for temporary files in pic2graph and eqn2graph scripts

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-9.2
- bump again for double-long bug on ppc(64)
- bump again for double-long bug on ppc(64)
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 1.18.1.1-9.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Feb 02 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-9
- remove gxditview from groff package (#179684)
- remove obsolete "--enable-japanese" configure option

* Fri Jan 12 2006 Miroslav Lichvar <mlichvar@redhat.com> - 1.18.1.1-8
- fix segfault in grotty on 64-bit big endian machines (#176904)
- fix assertion failure on abort message (#141912)
- attempt to fix a space problem with several european languages (#137728)

* Fri Jan 06 2006 Jindrich Novy <jnovy@redhat.com> - 1.18.1.1-7
- require X dependencies only for gxditview (#177118)
- work if bash's noclobber is on (#127492)

* Thu Jan 05 2006 Jindrich Novy <jnovy@redhat.com> - 1.18.1.1-6
- add BuildRequires imake and update dependencies for modular X
- spec cleanup
- fix compilation with gcc-4.1.0

* Wed Nov 24 2004 Miloslav Trmac <mitr@redhat.com> - 1.18.1.1-5
- Convert also mmroff.1 to UTF-8

* Sat Nov 20 2004 Miloslav Trmac <mitr@redhat.com> - 1.18.1.1-4
- Convert man pages to UTF-8

* Tue Oct 19 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-3
- fixed groffer scripte security problem (#136314)

* Thu Sep 16 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-2
- fixed DoCharacter calls in xditview (#110812)
- fixed fclose called once too often (#132690): thanks to Ulrich Drepper for
  the bug hunting

* Tue Jun 29 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1.1-1
- new version 1.18.1.1 (fixed groffer script)

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Jun  7 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-35
- fixed build prereq and requires

* Mon Mar  8 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-34
- new debian groff patch: groff_1.18.1-15.diff
- new fix for debian patch: groff-1.18.1-fix15.patch
- fixed width in devutf8 font M: groff-1.18.1-devutf8.patch
- removed iconv patch

* Mon Mar  1 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-33
- fixed nroff script: convert output to locale charmap

* Wed Feb 25 2004 Thomas Woerner <twoerner@redhat.com> 1.18.1-32
- fixed nroff script input (#116596)

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Feb 09 2004 Adrian Havill <havill@redhat.com>
- provide I18N version of nroff that accepts --legacy parameter
  (used by man-1.5m2-2)

* Thu Dec 18 2003 Thomas Woerner <twoerner@redhat.com>
- fixed missing BuildRequires (#110574)

* Tue Sep 23 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- allow compiling this without XFree86

* Wed Aug  6 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-28.2
- new devutf8 font description
- use -Tutf8 for ru_*.UTF-8 in nroff.sh
- fixes #88618 (ru_RU man pages in cambridge are using UTF-8, now)

* Fri Jun 13 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-28
- rebuild (debian-9)

* Tue Jun 10 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-27
- going back to 1.18.1-4 from debian (the newer versions did not work properly)
- fixed nroff.sh for ru_RU.(!UTF-8)

* Mon May 19 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-26
- fix input and output handler for 1.18.1-9 to be compatible with 1.18.1-4

* Tue Apr 29 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.18.1-9 from debian

* Tue Apr 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.18.1-8 from debian: use latin1 instead of C locale

* Sun Mar 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- update to debian patch 1.18.1-7 located at
  ftp://ftp.debian.org/debian/pool/main/g/groff/

* Thu Feb 13 2003 Elliot Lee <sopwith@redhat.com> 1.18.1-21
- groff-xlibs.patch to fix ppc64 builds

* Wed Feb 12 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-20
- Make the iconv patch a little less broken (bug #84132).

* Tue Feb 11 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-19
- added new iconv patch

* Tue Feb 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- disable the iconv patch, this will go into a wrapper within the man rpm

* Mon Feb 10 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-17
- fixed source of gzipped files

* Mon Feb 10 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add Korean support from ynakai@redhat.com, #83933

* Sun Feb 09 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- remove automatic conversion for ru_* and cz_*
- add 8bit patch
- update to 1.18.1-4 debian patch
- disable Patch8: groff-1.18.1-multichar.patch for now
- add ugly patch within the iconv patch to partly fix display of russian
  man-pages with "-Tnippon"

* Thu Feb  6 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-11
- Unbreak EUC-JP (bug #83608).

* Mon Feb  3 2003 Thomas Woerner <twoerner@redhat.com> 1.18.1-10
- fixed missing minus
- added iconv conversion script

* Fri Jan 31 2003 Tim Waugh <twaugh@redhat.com> 1.18.1-9
- Fix UTF-8.

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Wed Jan 15 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- also add hyphen changes to man.local in addition to mdoc.local

* Tue Jan 14 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- really include mdoc.local changes from debian

* Sat Jan 11 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- fix #81401, maybe also #57410

* Fri Jan 03 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- add more documentation #80729

* Wed Jan 01 2003 Florian La Roche <Florian.LaRoche@redhat.de>
- hot fix for devascii8 breakage

* Sun Dec 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to debian patch 1.18.1-2 located at
  ftp://ftp.debian.org/debian/pool/main/g/groff/

* Mon Nov 18 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.18.1
- use newest debian patch on top of it

* Mon Nov 04 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add gzip decompression patch

* Sat Nov 02 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.18.1
- apply groff_1.18-7 from debian
- remove some not-packaged files
- rm old printfilters completely

* Fri Oct 04 2002 Elliot Lee <sopwith@redhat.com> 1.18-7
- Patch7 - move pfbtops to CCPROGDIRS (it needs to link to C++ stuff)

* Sat Aug 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add patch for #72924

* Mon Aug 26 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- remove README.A4  #65920

* Sun Aug 11 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- use info files as installed by groff package
- completely disable older printconf stuff

* Thu Aug  8 2002 Yukihiro Nakai <ynakai@redhat.com>
- link docj.tmac to doc.tmac #57560

* Thu Aug  1 2002 Harald Hoyer <harald@redhat.de>
- update to 1.18
- mmroff(7) is now mmroff(1)

* Tue Jul 23 2002 Tim Powers <timp@redhat.com>
- build using gcc-3.2-0.1

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Jun 12 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- prereq install-info and add post/preun for info files

* Wed May 29 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add info files #64667

* Fri Feb 22 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- rebuild in new environment

* Sun Feb 17 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-16
- patch4 is already included in that

* Thu Jan 31 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- disable printconf support, but do not yet delete it from the source rpm

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Mon Jan 07 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- check string input

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- add URL tag

* Sat Jan 05 2002 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-13

* Thu Dec 06 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to newest debian patch 1.17.2-12

* Wed Aug 15 2001 Mike A. Harris <mharris@redhat.com> 1.17.2-3
- Added symlink from soelim to zsoelim, fixing bug (#51037)

* Tue Aug 14 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- fixes security bug #50494

* Sun Aug 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.17.2
- strerror patch is not needed anymore
- apply newest debian patch

* Fri Apr 27 2001 Bill Nottingham <notting@redhat.com>
- rebuild for C++ exception handling on ia64

* Tue Apr 03 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- do not change groff to use /etc/papersize. Deleted the changes
  in the debian patch.

* Fri Mar 30 2001 Trond Eivind GlomsrĹd <teg@redhat.com>
- Add hyphen.cs - file generated as described in Czech how-to, 6.7

* Wed Mar 28 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- updated to newest debian patch to get nippon/ascii8 support
  better working

* Fri Feb  9 2001 Crutcher Dunnavant <crutcher@redhat.com>
- switch to printconf filtration rules

* Tue Jan 09 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- change app-defaults to /usr/X11R6/lib/X11/app-defaults/
  and do not mark it as config file

* Thu Dec 14 2000 Yukihiro Nakai <ynakai@redhat.com>
- Add Japanese patch from RHL7J

* Fri Aug  4 2000 Florian La Roche <Florian.LaRoche@redhat.de>
- update to bug-fix release 1.16.1

* Fri Jul 28 2000 Tim Waugh <twaugh@redhat.com>
- Install troff-to-ps.fpi in /usr/lib/rhs-printfilters (#13634).

* Wed Jul 19 2000 Jeff Johnson <jbj@redhat.com>
- rebuild with gcc-2.96-41.

* Mon Jul 17 2000 Jeff Johnson <jbj@redhat.com>
- rebuild to fix miscompilation manifesting in alpha build of tcltk.

* Thu Jul 13 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul  4 2000 Jakub Jelinek <jakub@redhat.com>
- Rebuild with new C++

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- move mmroff to -perl

* Wed Jun  7 2000 Bernhard Rosenkraenzer <bero@redhat.com>
- Fix build
- FHS
- 1.16

* Sun May 14 2000 Jeff Johnson <jbj@redhat.com>
- install tmac.mse (FWIW tmac.se looks broken) to fix dangling symlink (#10757).
- add README.A4, how to set up for A4 paper (#8276).
- add other documents to package.

* Thu Mar  2 2000 Jeff Johnson <jbj@redhat.com>
- permit sourcing on regular files within cwd tree (unless -U specified).

* Wed Feb  9 2000 Jeff Johnson <jbj@redhat.com>
- fix incorrectly installed tmac.m file (#8362).

* Mon Feb  7 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- check if build system is sane again

* Thu Feb 03 2000 Cristian Gafton <gafton@redhat.com>
- fix description and summary
- man pages are compressed. This is ugly.

* Mon Jan 31 2000 Bill Nottingham <notting@redhat.com>
- put the binaries actually in the package *oops*

* Fri Jan 28 2000 Bill Nottingham <notting@redhat.com>
- split perl components into separate subpackage

* Wed Dec 29 1999 Bill Nottingham <notting@redhat.com>
- update to 1.15

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 9)
* Tue Feb 16 1999 Cristian Gafton <gafton@redhat.com>
- glibc 2.1 patch for xditview (#992)

* Thu Oct 22 1998 Bill Nottingham <notting@redhat.com>
- build for Raw Hide

* Thu Sep 10 1998 Cristian Gafton <gafton@redhat.com>
- fix makefiles to work with bash2

* Fri May 08 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Thu Apr 30 1998 Cristian Gafton <gafton@redhat.com>
- use g++ for C++ code

* Wed Apr 08 1998 Cristian Gafton <gafton@redhat.com>
- manhattan and buildroot

* Mon Nov  3 1997 Michael Fulbright <msf@redhat.com>
- made xdefaults file a config file

* Thu Oct 23 1997 Erik Troan <ewt@redhat.com>
- split perl components into separate subpackage

* Tue Oct 21 1997 Michael Fulbright <msf@redhat.com>
- updated to 1.11a
- added safe troff-to-ps.fpi

* Tue Oct 14 1997 Michael Fulbright <msf@redhat.com>
- removed troff-to-ps.fpi for security reasons.

* Fri Jun 13 1997 Erik Troan <ewt@redhat.com>
- built against glibc

