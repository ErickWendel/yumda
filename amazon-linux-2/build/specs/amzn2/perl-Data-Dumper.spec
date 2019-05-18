%global cpan_version 2.145
Name:           perl-Data-Dumper
Version:        %(echo '%{cpan_version}' | tr '_' '.')
Release: 3%{?dist}.0.2
Summary:        Stringify perl data structures, suitable for printing and eval
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Data-Dumper/
Source0:        http://www.cpan.org/authors/id/S/SM/SMUELLER/Data-Dumper-%{cpan_version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
# Run-time:
BuildRequires:  perl(B::Deparse)
BuildRequires:  perl(bytes)
BuildRequires:  perl(Carp)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(overload)
BuildRequires:  perl(XSLoader)
# perl-Test-Simple is in cycle with perl-Data-Dumper
%if !%{defined perl_bootstrap}
# Tests only:
BuildRequires:  perl(Config)
BuildRequires:  perl(lib)
BuildRequires:  perl(strict)
BuildRequires:  perl(Test::More) >= 0.98
# Optional tests:
BuildRequires:  perl(Encode)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(B::Deparse)
Requires:       perl(bytes)
Requires:       perl(Scalar::Util)
Requires:       perl(XSLoader)

%{?perl_default_filter}

%description
Given a list of scalars or reference variables, writes out their contents
in perl syntax. The references can also be objects. The content of each
variable is output in a single Perl statement. Handles self-referential
structures correctly.

%prep
%setup -q -n Data-Dumper-%{cpan_version}
sed -i '/MAN3PODS/d' Makefile.PL

%build
perl Makefile.PL INSTALLDIRS=vendor OPTIMIZE="$RPM_OPT_FLAGS"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
find $RPM_BUILD_ROOT -type f -name '*.bs' -size 0 -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%check
%if !%{defined perl_bootstrap}
make test
%endif

%files
%doc Changes Todo
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/Data*
%{_mandir}/man3/*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 2.145-3
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.145-2
- Mass rebuild 2013-12-27

* Mon Mar 18 2013 Petr Pisar <ppisar@redhat.com> - 2.145-1
- 2.145 bump

* Thu Feb 28 2013 Petr Pisar <ppisar@redhat.com> - 2.143-1
- 2.143 bump

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.139-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Dec 12 2012 Petr Pisar <ppisar@redhat.com> - 2.139-1
- 2.139 bump

* Fri Oct 05 2012 Petr Pisar <ppisar@redhat.com> - 2.136-1
- 2.136 bump

* Fri Aug 24 2012 Petr Pisar <ppisar@redhat.com> - 2.135.07-241
- Disable tests on bootstrap

* Mon Aug 13 2012 Marcela Mašláňová <mmaslano@redhat.com> - 2.135.07-240
- update the version to override the module from perl.srpm
- bump release to override sub-package from perl.spec 

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.131-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 2.131-2
- Perl 5.16 rebuild

* Tue Apr 10 2012 Petr Pisar <ppisar@redhat.com> 2.131-1
- Specfile autogenerated by cpanspec 1.78.
