Name:           perl-Params-Check
# Epoch to compete with perl.spec
Epoch:          1
Version:        0.38
Release:        2%{?dist}
Summary:        Generic input parsing/checking mechanism
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Params-Check/
Source0:        http://www.cpan.org/authors/id/B/BI/BINGOS/Params-Check-%{version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Locale::Maketext::Simple)
BuildRequires:  perl(vars)
# Tests:
BuildRequires:  perl(constant)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))

Prefix: %{_prefix}

%description
This is a generic input parsing/checking mechanism. It allows you to
validate input via a template. The only requirement is that the arguments
must be named.

%prep
%setup -q -n Params-Check-%{version}

%build
perl Makefile.PL INSTALLDIRS=vendor \
  PREFIX=%{_prefix} \
  INSTALLVENDORLIB=%{perl_vendorlib} \
  INSTALLVENDORARCH=%{perl_vendorarch}
make %{?_smp_mflags}

%install
make pure_install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name .packlist -exec rm -f {} \;
%{_fixperms} $RPM_BUILD_ROOT/*

%files
%license README
%{perl_vendorlib}/*

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1:0.38-2
- Mass rebuild 2013-12-27

* Fri Jun 21 2013 Petr Pisar <ppisar@redhat.com> - 1:0.38-1
- 0.38 bump

* Fri Jan 25 2013 Petr Pisar <ppisar@redhat.com> 1:0.36-1
- Specfile autogenerated by cpanspec 1.78.
