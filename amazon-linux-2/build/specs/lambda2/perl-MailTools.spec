Summary:        Various mail-related perl modules
Name:           perl-MailTools
Version:        2.12
Release:        2%{?dist}
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/MailTools/
Source0:        http://search.cpan.org/CPAN/authors/id/M/MA/MARKOV/MailTools-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(Date::Format)
BuildRequires:  perl(Date::Parse)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Net::Domain) >= 1.05
BuildRequires:  perl(Net::SMTP) >= 1.03
BuildRequires:  perl(POSIX)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Test::Pod)
BuildRequires:  perl(vars)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

%description
MailTools is a set of Perl modules related to mail applications.

%prep
%setup -q -n MailTools-%{version}
# Set up example scripts
cd examples
for file in *.PL; do
        perl $file
done
chmod -c -x *_demo
# Remove example-generation scripts, no longer needed
# It causes warnings from MakeMaker, but we don't care
rm *.PL
cd -

%build
perl Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}
find %{buildroot} -type f -name .packlist -exec rm -f {} +
%{_fixperms} %{buildroot}

%check
make test
make test TEST_FILES="xt/*.t"

%files
%doc ChangeLog README* examples/
%dir %{perl_vendorlib}/Mail/
%dir %{perl_vendorlib}/Mail/Field/
%dir %{perl_vendorlib}/Mail/Mailer/
%doc %{perl_vendorlib}/Mail/Address.pod
%doc %{perl_vendorlib}/Mail/Cap.pod
%doc %{perl_vendorlib}/Mail/Field.pod
%doc %{perl_vendorlib}/Mail/Field/AddrList.pod
%doc %{perl_vendorlib}/Mail/Field/Date.pod
%doc %{perl_vendorlib}/Mail/Field/Generic.pod
%doc %{perl_vendorlib}/Mail/Filter.pod
%doc %{perl_vendorlib}/Mail/Header.pod
%doc %{perl_vendorlib}/Mail/Internet.pod
%doc %{perl_vendorlib}/Mail/Mailer.pod
%doc %{perl_vendorlib}/Mail/Send.pod
%doc %{perl_vendorlib}/Mail/Util.pod
%{perl_vendorlib}/Mail/Address.pm
%{perl_vendorlib}/Mail/Cap.pm
%{perl_vendorlib}/Mail/Filter.pm
%{perl_vendorlib}/Mail/Header.pm
%{perl_vendorlib}/Mail/Internet.pm
%{perl_vendorlib}/Mail/Field.pm
%{perl_vendorlib}/Mail/Mailer.pm
%{perl_vendorlib}/Mail/Send.pm
%{perl_vendorlib}/Mail/Util.pm
%{perl_vendorlib}/Mail/Field/AddrList.pm
%{perl_vendorlib}/Mail/Field/Date.pm
%{perl_vendorlib}/Mail/Field/Generic.pm
%{perl_vendorlib}/Mail/Mailer/qmail.pm
%{perl_vendorlib}/Mail/Mailer/rfc822.pm
%{perl_vendorlib}/Mail/Mailer/sendmail.pm
%{perl_vendorlib}/Mail/Mailer/smtp.pm
%{perl_vendorlib}/Mail/Mailer/smtps.pm
%{perl_vendorlib}/Mail/Mailer/testfile.pm
%{_mandir}/man3/Mail::Address.3*
%{_mandir}/man3/Mail::Cap.3*
%{_mandir}/man3/Mail::Field.3*
%{_mandir}/man3/Mail::Field::AddrList.3*
%{_mandir}/man3/Mail::Field::Date.3*
%{_mandir}/man3/Mail::Field::Generic.3*
%{_mandir}/man3/Mail::Filter.3*
%{_mandir}/man3/Mail::Header.3*
%{_mandir}/man3/Mail::Internet.3*
%{_mandir}/man3/Mail::Mailer.3*
%{_mandir}/man3/Mail::Send.3*
%{_mandir}/man3/Mail::Util.3*

%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.12-2
- Mass rebuild 2013-12-27

* Wed Aug 07 2013 Petr Šabata <contyk@redhat.com> - 2.12-1.1
- Add some missing built-time dependencies
- Fix a bogus date in changelog
- Modernize the spec

* Fri Dec 21 2012 Paul Howarth <paul@city-fan.org> 2.12-1
- Update to 2.12
  - Default for Mail::Header::new(Modify) is 'false', not 'true'
    (CPAN RT#79985)
  - Mail::Address take username with rindex(), a bit better than index() but
    still poor (CPAN RT#82056)
  - Check for bad folding of header lines (CPAN RT#79993)
  - Add a note about better to avoid Mail::Address->name() (CPAN RT#81459)
- Drop UTF8 patch, no longer needed

* Wed Aug 29 2012 Paul Howarth <paul@city-fan.org> 2.11-1
- Update to 2.11
  - Fix typo in Mail::Mailer::smtp, which only shows up in Perl > 5.14

* Tue Aug 28 2012 Paul Howarth <paul@city-fan.org> 2.10-1
- Update to 2.10
  - Mail::Mailer::smtp set from address twice (CPAN RT#77161)
  - Mail::Mailer::smtps did not support the From option (CPAN RT#77161)
  - Mail::Util::mailaddress has now an optional parameter to set the returned
    value explicitly (CPAN #75975)
- BR: perl(base)
- Drop BR: perl(Config) and perl(POSIX), not dual-lived
- Drop %%defattr, redundant since rpm 4.4
- Don't need to remove empty directories from the buildroot

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.09-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Jun 11 2012 Petr Pisar <ppisar@redhat.com> - 2.09-2
- Perl 5.16 rebuild

* Sat Feb 25 2012 Paul Howarth <paul@city-fan.org> - 2.09-1
- Update to 2.09
  - Remove dependency to Test::Pod by moving 99pod.t from t/ to xt/
    (CPAN RT#69918)
- BR: perl(Net::Domain) ≥ 1.05 and perl(Net::SMTP) ≥ 1.03
- Explicitly run xt/ tests

* Thu Jan 12 2012 Paul Howarth <paul@city-fan.org> - 2.08-3
- Use DESTDIR rather than PERL_INSTALL_ROOT
- One buildreq per line for readability
- Add buildreqs for core perl modules, which might be dual-lived

* Mon Jun 20 2011 Marcela Mašláňová <mmaslano@redhat.com> - 2.08-2
- Perl mass rebuild

* Wed Jun  1 2011 Paul Howarth <paul@city-fan.org> - 2.08-1
- Update to 2.08 (#709697)
  - Respect errors on closing a Mail::Mailer::smtp/::smtps connection
  - Mail::Internet should accept Net::SMTP::SSL as well (CPAN RT#68590)
  - Document that Mail::Mailer::smtps needs Authen::SASL
- Use patch rather than iconv to convert docs to UTF8 encoding
- Nobody else likes macros for commands

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.07-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct  1 2010 Paul Howarth <paul@city-fan.org> 2.07-1
- Update to 2.07
  - Document perl 5.8.1 requirement in README (CPAN RT#61753)
  - Add "MAIL FROM" to Mail::Mailer::smtp

* Mon May 03 2010 Marcela Maslanova <mmaslano@redhat.com> - 2.06-2
- Mass rebuild with perl-5.12.0

* Wed Jan 27 2010 Paul Howarth <paul@city-fan.org> 2.06-1
- Update to 2.06 (add support for smtps via Net::SMTP::SSL)
- Use %%{_fixperms} macro instead of our own chmod incantation

* Mon Dec 21 2009 Paul Howarth <paul@city-fan.org> 2.05-1
- Update to 2.05
  - Fix de-ref error when index out of range in Mail::Header::get()
  - Repair fixed selection of smtp for non-unix systems
  - Do not run pod.t in devel environment
  - Set default output filename for Mail::Mailer::testfile::PRINT
  - Warn when no mailers were found (CPAN RT#52901)
- Tidy up %%files list

* Mon Dec  7 2009 Stepan Kasal <skasal@redhat.com> 2.04-4
- Rebuild against perl 5.10.1

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.04-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> 2.04-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 30 2008 Paul Howarth <paul@city-fan.org> 2.04-1
- Update to 2.04

* Tue Apr 15 2008 Paul Howarth <paul@city-fan.org> 2.03-1
- Update to 2.03

* Wed Feb 27 2008 Tom "spot" Callaway <tcallawa@redhat.com> - 2.02-3
- Rebuild for perl 5.10 (again)

* Sun Jan 20 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.02-2
- rebuild for new perl

* Mon Dec  3 2007 Paul Howarth <paul@city-fan.org> 2.02-1
- Update to 2.02
- Remove buildreqs perl(Net::SMTP) and perl(Net::Domain), bundled with perl
- Add buildreqs perl(Date::Format), perl(Date::Parse), perl(Test::More), and
  perl(Test::Pod)
- Remove patch for CPAN RT#20726, now fixed upstream
- Buildreq perl >= 5.8.1
- Tweak files list to mark pod files as %%doc
- Fix character encoding for ChangeLog

* Mon Aug 13 2007 Paul Howarth <paul@city-fan.org> 1.77-2
- Clarify license as GPL v1 or later, or Artistic (same as perl)
- Unexpand tabs in spec file

* Fri May 11 2007 Paul Howarth <paul@city-fan.org> 1.77-1
- Update to 1.77

* Tue Apr 10 2007 Paul Howarth <paul@city-fan.org> 1.76-1
- Update to 1.76
- Add comment text about the patch for fixing CPAN RT#20726
- BuildRequire perl(ExtUtils::MakeMaker) rather than perl-devel

* Thu Mar  8 2007 Paul Howarth <paul@city-fan.org> 1.74-4
- Buildrequire perl-devel for Fedora 7 onwards
- Fix argument order for find with -depth

* Wed Aug 30 2006 Paul Howarth <paul@city-fan.org> 1.74-3
- FE6 mass rebuild

* Fri Jul 28 2006 Paul Howarth <paul@city-fan.org> 1.74-2
- cosmetic spec file changes
- fix CPAN RT#20726 (RH #200450), allowing Mail::Util::read_mbox() to open
  files with weird names

* Wed Mar  1 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.74-1
- 1.74.

* Sun Jan 22 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.73-1
- 1.73.

* Wed Jan 18 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.72-1
- 1.72.

* Fri Jan  6 2006 Ville Skyttä <ville.skytta at iki.fi> - 1.71-1
- 1.71.

* Wed Dec 14 2005 Ville Skyttä <ville.skytta at iki.fi> - 1.67-2
- Fix demo scripts.
- Sync with fedora-rpmdevtools' perl spec template.

* Fri Jul  1 2005 Paul Howarth <paul@city-fan.org> - 1.67-1
- update to 1.67 (#161830)
- assume perl_vendorlib is set
- license is same as perl (GPL or Artistic) according to README
- don't include module name in summary
- use macros consistently
- add dist tag

* Wed Apr  6 2005 Michael Schwendt <mschwendt[AT]users.sf.net> - 1.66-2
- rebuilt

* Sat Jan 22 2005 Ville Skyttä <ville.skytta at iki.fi> - 0:1.66-1
- Update to 1.66.

* Wed Aug 18 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.64-0.fdr.1
- Update to 1.64, patch applied upstream.
- Bring up to date with current fedora.us Perl spec template.

* Sat Mar 20 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.61-0.fdr.2
- Add patch to complete test.pm -> testfile.pm change introduced in 1.61.

* Sun Mar 14 2004 Ville Skyttä <ville.skytta at iki.fi> - 0:1.61-0.fdr.1
- Update to 1.61.
- Reduce directory ownership bloat.
- Run tests in the %%check section.

* Thu Sep 25 2003 Ville Skyttä <ville.skytta at iki.fi> - 0:1.60-0.fdr.1
- Update to 1.60.
- Install into vendor dirs.
- Spec cleanups.

* Sat Jul 12 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.5
- Package is now noarch

* Fri Jul 11 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.4
- Changed group tag
- Making test in build section

* Tue Jul  1 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.3
- Modified files section

* Tue Jun 17 2003 Dams <anvil[AT]livna.org> 0:1.58-0.fdr.2
- Added forgotten description
- Modified Summary according to Michael Schwendt suggestion
- Modified tarball permissions to 0644

* Sun Jun 15 2003 Dams <anvil[AT]livna.org>
- Initial build.
