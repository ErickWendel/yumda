Name:           perl-Locale-Maketext
Version:        1.23
Release:        3%{?dist}
Summary:        Framework for localization
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/Locale-Maketext/
Source0:        http://www.cpan.org/authors/id/T/TO/TODDR/Locale-Maketext-%{version}.tar.gz
# Fix escaping backslashes, bug #1026761, RT#120457
Patch0:         Locale-Maketext-1.23-Commit-1735f6f53ca19f99c6e9e39496c486af323ba6a8-star.patch
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(strict)
# Run-time:
BuildRequires:  perl(Carp)
BuildRequires:  perl(I18N::LangTags) >= 0.31
BuildRequires:  perl(I18N::LangTags::Detect)
BuildRequires:  perl(integer)
# utf8 is optional
BuildRequires:  perl(vars)
BuildRequires:  perl(warnings)
# Tests:
BuildRequires:  perl(base)
BuildRequires:  perl(Scalar::Util)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(utf8)
# Optional tests:
%if !%{defined perl_bootstrap}
BuildRequires:  perl(Test::Pod) >= 1.14
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(I18N::LangTags) >= 0.31

# Filter under-specified dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(I18N::LangTags\\)$

Prefix: %{_prefix}

%description
It is a common feature of applications (whether run directly, or via the Web)
for them to be "localized" -- i.e., for them to present an English interface
to an English-speaker, a German interface to a German-speaker, and so on for
all languages it's programmed with. Locale::Maketext is a framework for
software localization; it provides you with the tools for organizing and
accessing the bits of text and text-processing code that you need for
producing localized applications.

%prep
%setup -q -n Locale-Maketext-%{version}
%patch0 -p1

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

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 1.23-3
- Mass rebuild 2013-12-27

* Mon Nov 11 2013 Petr Pisar <ppisar@redhat.com> - 1.23-2
- Fix escaping backslashes (bug #1026761)

* Fri Apr 05 2013 Petr Pisar <ppisar@redhat.com> 1.23-1
- Specfile autogenerated by cpanspec 1.78.
