Name:           perl-Scalar-List-Utils
Version:        1.27
Release: 248%{?dist}.0.2
Summary:        A selection of general-utility scalar and list subroutines
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Scalar-List-Utils/
Source0:        http://search.cpan.org/CPAN/authors/id/P/PE/PEVANS/Scalar-List-Utils-%{version}.tar.gz
BuildRequires:  perl
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(Config)
BuildRequires:  perl(constant)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(IO::File)
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(overload)
BuildRequires:  perl(strict)
BuildRequires:  perl(Symbol)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(threads)
BuildRequires:  perl(threads::shared)
BuildRequires:  perl(Tie::Handle)
BuildRequires:  perl(Tie::Scalar)
BuildRequires:  perl(Tie::StdScalar)
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
BuildRequires:  perl(XSLoader)
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires:       perl(Carp)

%{?perl_default_filter}

%description
This package contains a selection of subroutines that people have expressed
would be nice to have in the perl core, but the usage would not really be
high enough to warrant the use of a keyword, and the size so small such
that being individual extensions would be wasteful.

%prep
%setup -q -n Scalar-List-Utils-%{version}

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor OPTIMIZE="%{optflags}"
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} \;
find %{buildroot} -type f -name '*.bs' -size 0 -exec rm -f {} \;

%{_fixperms} %{buildroot}/*

%check
make test

%files
%doc Changes README
%{perl_vendorarch}/auto/*
%{perl_vendorarch}/List*
%{perl_vendorarch}/Scalar*
%{_mandir}/man3/*

%changelog
* Fri Jan 24 2014 Daniel Mach <dmach@redhat.com> - 1.27-248
- Mass rebuild 2014-01-24

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.27-247
- Mass rebuild 2013-12-27

* Wed Jul 31 2013 Petr Pisar <ppisar@redhat.com> - 1.27-246
- Specify all dependencies

* Fri Jan 04 2013 Iain Arnell <iarnell@gmail.com> 1.27-245
- update to latest upstream version

* Fri Aug 17 2012 Petr Pisar <ppisar@redhat.com> - 1.25-240
- Increase release to replace perl sub-package (bug #848961)

* Thu Aug 16 2012 Petr Pisar <ppisar@redhat.com> - 1.25-4
- Correct dependencies

* Tue Aug 14 2012 Daniel Mach <dmach@redhat.com> - 1.25-3.1
- Rebuild for perl 5.16

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.25-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 06 2012 Petr Pisar <ppisar@redhat.com> - 1.25-2
- Perl 5.16 rebuild

* Sun Mar 25 2012 Iain Arnell <iarnell@gmail.com> 1.25-1
- update to latest upstream version

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.23-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jun 17 2011 Marcela Mašláňová <mmaslano@redhat.com> - 1.23-2
- Perl mass rebuild

* Mon Feb 21 2011 Iain Arnell <iarnell@gmail.com> 1.23-1
- Specfile autogenerated by cpanspec 1.79.
