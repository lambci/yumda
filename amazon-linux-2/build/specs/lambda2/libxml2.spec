# for -O3 on ppc64 c.f. 1051068
%global _performance_build 1
%global _trivial .5
%global _buildid .1

Summary: Library providing XML and HTML support
Name: libxml2
Version: 2.9.1
Release: 6%{?dist}%{?extra_release}%{?_trivial}%{?_buildid}
License: MIT
Group: Development/Libraries
Source: ftp://xmlsoft.org/libxml2/libxml2-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-root
BuildRequires: python python-devel zlib-devel pkgconfig xz-devel
URL: http://xmlsoft.org/
Patch0: libxml2-multilib.patch
Patch1: libxml2-2.9.0-do-not-check-crc.patch

Patch100: libxml2-Fix-a-regression-in-xmlGetDocCompressMode.patch
Patch101: CVE-2014-3660-rhel7.patch
Patch102: libxml2-Fix-missing-entities-after-CVE-2014-3660-fix.patch
Patch103: libxml2-Do-not-fetch-external-parameter-entities.patch
Patch104: libxml2-Fix-regression-introduced-by-CVE-2014-0191.patch
Patch105: libxml2-Stop-parsing-on-entities-boundaries-errors.patch
Patch106: libxml2-Cleanup-conditional-section-error-handling.patch
Patch107: libxml2-Fail-parsing-early-on-if-encoding-conversion-failed.patch
Patch108: libxml2-Another-variation-of-overflow-in-Conditional-sections.patch
Patch109: libxml2-Fix-an-error-in-previous-Conditional-section-patch.patch
Patch110: libxml2-Fix-parsing-short-unclosed-comment-uninitialized-access.patch
Patch111: libxml2-Avoid-extra-processing-of-MarkupDecl-when-EOF.patch
Patch112: libxml2-Avoid-processing-entities-after-encoding-conversion-failures.patch
Patch113: libxml2-xmlStopParser-reset-errNo.patch
Patch114: libxml2-CVE-2015-7497-Avoid-an-heap-buffer-overflow-in-xmlDictComputeFastQKey.patch
Patch115: libxml2-CVE-2015-5312-Another-entity-expansion-issue.patch
Patch116: libxml2-Add-xmlHaltParser-to-stop-the-parser.patch
Patch117: libxml2-Reuse-xmlHaltParser-where-it-makes-sense.patch
Patch118: libxml2-Do-not-print-error-context-when-there-is-none.patch
Patch119: libxml2-Detect-incoherency-on-GROW.patch
Patch120: libxml2-Fix-some-loop-issues-embedding-NEXT.patch
Patch121: libxml2-Bug-on-creating-new-stream-from-entity.patch
Patch122: libxml2-CVE-2015-7500-Fix-memory-access-error-due-to-incorrect-entities-boundaries.patch
Patch123: libxml2-CVE-2015-8242-Buffer-overead-with-HTML-parser-in-push-mode.patch
Patch124: libxml2-CVE-2015-1819-Enforce-the-reader-to-run-in-constant-memory.patch
patch125: libxml2-Add-missing-increments-of-recursion-depth-counter-to-XML-parser.patch
patch126: libxml2-Avoid-building-recursive-entities.patch
patch127: libxml2-Bug-757711-heap-buffer-overflow-in-xmlFAParsePosCharGroup-https-bugzilla.gnome.org-show_bug.cgi-id-757711.patch
patch128: libxml2-Bug-758588-Heap-based-buffer-overread-in-xmlParserPrintFileContextInternal-https-bugzilla.gnome.org-show_bug.cgi-id-758588.patch
patch129: libxml2-Bug-758605-Heap-based-buffer-overread-in-xmlDictAddString-https-bugzilla.gnome.org-show_bug.cgi-id-758605.patch
patch130: libxml2-Bug-759398-Heap-use-after-free-in-xmlDictComputeFastKey-https-bugzilla.gnome.org-show_bug.cgi-id-759398.patch
patch131: libxml2-Bug-763071-heap-buffer-overflow-in-xmlStrncat-https-bugzilla.gnome.org-show_bug.cgi-id-763071.patch
patch132: libxml2-Fix-inappropriate-fetch-of-entities-content.patch
patch133: libxml2-Fix-some-format-string-warnings-with-possible-format-string-vulnerability.patch
patch134: libxml2-Heap-based-buffer-overread-in-htmlCurrentChar.patch
patch135: libxml2-Heap-based-buffer-overread-in-xmlNextChar.patch
patch136: libxml2-Heap-based-buffer-underreads-due-to-xmlParseName.patch
patch137: libxml2-Heap-use-after-free-in-htmlParsePubidLiteral-and-htmlParseSystemiteral.patch
patch138: libxml2-Heap-use-after-free-in-xmlSAX2AttributeNs.patch
patch139: libxml2-More-format-string-warnings-with-possible-format-string-vulnerability.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1595697
patch140: libxml2-2.9.1-CVE-2015-8035.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1602817
patch141: libxml2-2.9.1-CVE-2018-14404.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1729857
patch142: libxml2-2.9.1-CVE-2017-15412.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1714050
patch143: libxml2-2.9.1-CVE-2016-5131.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1579211
patch144: libxml2-2.9.1-CVE-2017-18258.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1622715
patch145: libxml2-2.9.1-CVE-2018-14567.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1793000
patch146: libxml2-2.9.1-CVE-2019-19956.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1810057
patch147: libxml2-2.9.1-CVE-2019-20388.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1810073
patch148: libxml2-2.9.1-CVE-2020-7595.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=1812145
patch149: libxml2-2.9.1-xsd-any.patch

# Amazon patches
Patch10001: libxml2-CVE-2016-4658.patch
Patch10002: libxml2-CVE-2017-16931.patch

Prefix: %{_prefix}

%description
This library allows to manipulate XML files. It includes support
to read, modify and write XML and HTML files. There is DTDs support
this includes parsing and validation even with complex DtDs, either
at parse time or later once the document has been modified. The output
can be a simple SAX stream or and in-memory DOM like representations.
In this case one can use the built-in XPath and XPointer implementation
to select sub nodes or ranges. A flexible Input/Output mechanism is
available, with existing HTTP and FTP modules and combined to an
URI library.

%prep
%setup -q
%patch0 -p1
# workaround for #877567 - Very weird bug gzip decompression bug in "recent" libxml2 versions
%patch1 -p1 -b .do-not-check-crc

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1
%patch108 -p1
%patch109 -p1
%patch110 -p1
%patch111 -p1
%patch112 -p1
%patch113 -p1
%patch114 -p1
%patch115 -p1
%patch116 -p1
%patch117 -p1
%patch118 -p1
%patch119 -p1
%patch120 -p1
%patch121 -p1
%patch122 -p1
%patch123 -p1
%patch124 -p1
%patch125 -p1
%patch126 -p1
%patch127 -p1
%patch128 -p1
%patch129 -p1
%patch130 -p1
%patch131 -p1
%patch132 -p1
%patch133 -p1
%patch134 -p1
%patch135 -p1
%patch136 -p1
%patch137 -p1
%patch138 -p1
%patch139 -p1
%patch140 -p1
%patch141 -p1
%patch142 -p1
%patch143 -p1
%patch144 -p1
%patch145 -p1
%patch146 -p1
%patch147 -p1
%patch148 -p1
%patch149 -p1

%patch10001 -p1
%patch10002 -p1

%build
%configure --disable-static --without-python
make %{_smp_mflags}

%install
make install DESTDIR=%{buildroot}

%files
%defattr(-, root, root)
%license Copyright
%{_libdir}/lib*.so.*
%{_bindir}/xmllint
%{_bindir}/xmlcatalog

%exclude %{_includedir}
%exclude %{_mandir}
%exclude %{_libdir}/*.la
%exclude %{_libdir}/*.so
%exclude %{_libdir}/pkgconfig
%exclude %{_libdir}/*.sh
%exclude %{_datadir}
%exclude %{_bindir}/xml2-config

%changelog
* Thu Oct 29 2020 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Wed Apr 22 2020 David King <dking@redhat.com> - 2.9.1-6.5
- Fix CVE-2019-19956 (#1793000)
- Fix CVE-2019-20388 (#1810057)
- Fix CVE-2020-7595 (#1810073)
- Fix xsd:any schema validation (#1812145)

* Fri Nov 01 2019 David King <dking@redhat.com> - 2.9.1-6.4
- Fix CVE-2015-8035 (#1595697)
- Fix CVE-2018-14404 (#1602817)
- Fix CVE-2017-15412 (#1729857)
- Fix CVE-2016-5131 (#1714050)
- Fix CVE-2017-18258 (#1579211)
- Fix CVE-2018-1456 (#1622715)

* Wed Sep  18 2019 Frederick Lefebvre <fredlef@amazon.com> - libxml2-2.9.1-6.amzn2.3.3
- Disallow namespace nodes in XPointer ranges (CVE-2016-4658)
- Fix handling of parameter-entity references (CVE-2017-16931)

* Mon Jun  6 2016 Daniel Veillard <veillard@redhat.com> - libxml2-2.9.1-6.3
- Heap-based buffer overread in xmlNextChar (CVE-2016-1762)
- Bug 763071: Heap-buffer-overflow in xmlStrncat <https://bugzilla.gnome.org/show_bug.cgi?id=763071> (CVE-2016-1834)
- Bug 757711: Heap-buffer-overflow in xmlFAParsePosCharGroup <https://bugzilla.gnome.org/show_bug.cgi?id=757711> (CVE-2016-1840)
- Bug 758588: Heap-based buffer overread in xmlParserPrintFileContextInternal <https://bugzilla.gnome.org/show_bug.cgi?id=758588> (CVE-2016-1838)
- Bug 758605: Heap-based buffer overread in xmlDictAddString <https://bugzilla.gnome.org/show_bug.cgi?id=758605> (CVE-2016-1839)
- Bug 759398: Heap use-after-free in xmlDictComputeFastKey <https://bugzilla.gnome.org/show_bug.cgi?id=759398> (CVE-2016-1836)
- Fix inappropriate fetch of entities content (CVE-2016-4449)
- Heap use-after-free in htmlParsePubidLiteral and htmlParseSystemiteral (CVE-2016-1837)
- Heap use-after-free in xmlSAX2AttributeNs (CVE-2016-1835)
- Heap-based buffer-underreads due to xmlParseName (CVE-2016-4447)
- Heap-based buffer overread in htmlCurrentChar (CVE-2016-1833)
- Add missing increments of recursion depth counter to XML parser. (CVE-2016-3705)
- Avoid building recursive entities (CVE-2016-3627)
- Fix some format string warnings with possible format string vulnerability (CVE-2016-4448)
- More format string warnings with possible format string vulnerability (CVE-2016-4448)

* Mon Nov 30 2015 Daniel Veillard <veillard@redhat.com> - 2.9.1-6.2
- Fix a series of CVEs (rhbz#1286496)
- CVE-2015-7941 Stop parsing on entities boundaries errors
- CVE-2015-7941 Cleanup conditional section error handling
- CVE-2015-8317 Fail parsing early on if encoding conversion failed
- CVE-2015-7942 Another variation of overflow in Conditional sections
- CVE-2015-7942 Fix an error in previous Conditional section patch
- Fix parsing short unclosed comment uninitialized access
- CVE-2015-7498 Avoid processing entities after encoding conversion failures
- CVE-2015-7497 Avoid an heap buffer overflow in xmlDictComputeFastQKey
- CVE-2015-5312 Another entity expansion issue
- CVE-2015-7499 Add xmlHaltParser() to stop the parser
- CVE-2015-7499 Detect incoherency on GROW
- CVE-2015-7500 Fix memory access error due to incorrect entities boundaries
- CVE-2015-8242 Buffer overead with HTML parser in push mode
- CVE-2015-1819 Enforce the reader to run in constant memory

* Mon Mar 23 2015 Daniel Veillard <veillard@redhat.com> - 2.9.1-6
- Fix missing entities after CVE-2014-3660 fix
- CVE-2014-0191 Do not fetch external parameter entities (rhbz#1195650)
- Fix regressions introduced by CVE-2014-0191 patch

* Sat Oct 11 2014 Daniel Veillard <veillard@redhat.com> - 2.9.1-5.1
- CVE-2014-3660 denial of service via recursive entity expansion (rhbz#1149087)

* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.9.1-5
- Mass rebuild 2014-01-24

* Wed Jan 15 2014 Daniel Veillard <veillard@redhat.com> - 2.9.1-4
- rebuild to activate -O3 on ppc64 rhbz#1051068

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.9.1-3
- Mass rebuild 2013-12-27

* Fri Nov 15 2013 Daniel Veillard <veillard@redhat.com> - 2.9.1-2
- Fix a regression in xmlGetDocCompressMode() rhbz#963716

* Fri Apr 19 2013 Daniel Veillard <veillard@redhat.com> - 2.9.1-1
- upstream release of 2.9.1
- a couple more API entry point
- compatibility with python3
- a lot of bug fixes

* Mon Feb 11 2013 Daniel Veillard <veillard@redhat.com> - 2.9.0-4
- fix --nocheck build which I broke in october rhbz#909767

* Mon Nov 19 2012 Jaroslav Reznik <jreznik@redhat.com> - 2.9.0-3
- workaround for crc/len check failure, rhbz#877567

* Thu Oct 11 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-2
- remaining cleanups from merge bug rhbz#226079
- do not put the docs in the main package, only in -devel rhbz#864731

* Tue Sep 11 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-1
- upstream release of 2.9.0
- A few new API entry points
- More resilient push parser mode
- A lot of portability improvement
- Faster XPath evaluation
- a lot of bug fixes and smaller improvement

* Fri Aug 10 2012 Daniel Veillard <veillard@redhat.com> - 2.9.0-0rc1
- upstream release candidate 1 of 2.9.0
- introduce a small API change, but ABI compatible, see
  https://mail.gnome.org/archives/xml/2012-August/msg00005.html
  patches for php, gcc/libjava and evolution-data-connector are upstream
  Grab me in cases of problems veillard@redhat.com
- many bug fixes including security aspects and small improvements

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Daniel Veillard <veillard@redhat.com> - 2.8.0-1
- upstream release of 2.8.0
- add lzma compression support
- many bug fixes and small improvements

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Mar  4 2011 Daniel Veillard <veillard@redhat.com> - 2.7.8-6
- fix a double free in XPath CVE-2010-4494 bug 665965

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.8-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Nov  5 2010 Daniel Veillard <veillard@redhat.com> - 2.7.8-4
- reactivate shared libs versionning script

* Thu Nov  4 2010 Daniel Veillard <veillard@redhat.com> - 2.7.8-1
- Upstream release of 2.7.8
- various bug fixes, including potential crashes
- new non-destructive formatting option
- date parsing updated to RFC 5646

* Wed Jul 21 2010 David Malcolm <dmalcolm@redhat.com> - 2.7.7-2
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Mon Mar 15 2010 Daniel Veillard <veillard@redhat.com> - 2.7.7-1
- Upstream release of 2.7.7
- fix serious trouble with zlib >= 1.2.4
- xmllint new option --xpath
- various HTML parser improvements
- includes a number of nug fixes

* Tue Oct  6 2009 Daniel Veillard <veillard@redhat.com> - 2.7.6-1
- Upstream release of 2.7.6
- restore thread support off by default in 2.7.5

* Thu Sep 24 2009 Daniel Veillard <veillard@redhat.com> - 2.7.5-1
- Upstream release of 2.7.5
- fix a couple of Relax-NG validation problems
- couple more fixes

* Tue Sep 15 2009 Daniel Veillard <veillard@redhat.com> - 2.7.4-2
- fix a problem with little data at startup affecting inkscape #523002

* Thu Sep 10 2009 Daniel Veillard <veillard@redhat.com> - 2.7.4-1
- upstream release 2.7.4
- symbol versioning of libxml2 shared libs
- very large number of bug fixes

* Mon Aug 10 2009 Daniel Veillard <veillard@redhat.com> - 2.7.3-4
- two patches for parsing problems CVE-2009-2414 and CVE-2009-2416

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Jan 18 2009 Daniel Veillard <veillard@redhat.com> - 2.7.3-1
- new release 2.7.3
- limit default max size of text nodes
- special parser mode for PHP
- bug fixes and more compiler checks

* Wed Dec  3 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-7
- Pull back into Python 2.6

* Wed Dec  3 2008 Caolán McNamara <caolanm@redhat.com> - 2.7.2-6
- AutoProvides requires BuildRequires pkgconfig

* Wed Dec  3 2008 Caolán McNamara <caolanm@redhat.com> - 2.7.2-5
- rebuild to get provides(libxml-2.0) into HEAD rawhide

* Mon Dec  1 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-4
- Rebuild for pkgconfig logic

* Fri Nov 28 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 2.7.2-3
- Rebuild for Python 2.6

* Wed Nov 12 2008 Daniel Veillard <veillard@redhat.com> - 2.7.2-2.fc11
- two patches for size overflows problems CVE-2008-4225 and CVE-2008-4226

* Fri Oct  3 2008 Daniel Veillard <veillard@redhat.com> 2.7.2-1.fc10
- new release 2.7.2
- Fixes the known problems in 2.7.1
- increase the set of options when saving documents

* Thu Oct  2 2008 Daniel Veillard <veillard@redhat.com> 2.7.1-2.fc10
- fix a nasty bug in 2.7.x, http://bugzilla.gnome.org/show_bug.cgi?id=554660

* Mon Sep  1 2008 Daniel Veillard <veillard@redhat.com> 2.7.1-1.fc10
- fix python serialization which was broken in 2.7.0
- Resolve: rhbz#460774

* Sat Aug 30 2008 Daniel Veillard <veillard@redhat.com> 2.7.0-1.fc10
- upstream release of 2.7.0
- switch to XML 1.0 5th edition
- switch to RFC 3986 for URI parsing
- better entity handling
- option to remove hardcoded limitations in the parser
- more testing
- a new API to allocate entity nodes
- and lot of fixes and clanups

* Mon Aug 25 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-4.fc10
- fix for entities recursion problem
- Resolve: rhbz#459714

* Fri May 30 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-3.fc10
- cleanup based on Fedora packaging guidelines, should fix #226079
- separate a -static package

* Thu May 15 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-2.fc10
- try to fix multiarch problems like #440206

* Tue Apr  8 2008 Daniel Veillard <veillard@redhat.com> 2.6.32-1.fc9
- upstream release 2.6.32 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 2.6.31-2
- Autorebuild for GCC 4.3

* Fri Jan 11 2008 Daniel Veillard <veillard@redhat.com> 2.6.31-1.fc9
- upstream release 2.6.31 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Thu Aug 23 2007 Daniel Veillard <veillard@redhat.com> 2.6.30-1
- upstream release 2.6.30 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Tue Jun 12 2007 Daniel Veillard <veillard@redhat.com> 2.6.29-1
- upstream release 2.6.29 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Wed May 16 2007 Matthias Clasen <mclasen@redhat.com> 2.6.28-2
- Bump revision to fix N-V-R problem

* Tue Apr 17 2007 Daniel Veillard <veillard@redhat.com> 2.6.28-1
- upstream release 2.6.28 see http://xmlsoft.org/news.html
- many bug fixed upstream

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 2.6.27-2
- rebuild against python 2.5

* Wed Oct 25 2006 Daniel Veillard <veillard@redhat.com> 2.6.27-1
- upstream release 2.6.27 see http://xmlsoft.org/news.html
- very large amount of bug fixes reported upstream

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.26-2.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.6.26-2.1
- rebuild

* Wed Jun  7 2006 Daniel Veillard <veillard@redhat.com> 2.6.26-2
- fix bug #192873
* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com> 2.6.26-1
- upstream release 2.6.26 see http://xmlsoft.org/news.html

* Tue Jun  6 2006 Daniel Veillard <veillard@redhat.com>
- upstream release 2.6.25 broken, do not ship !

