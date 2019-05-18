%global cpan_version 0.2301
Name:           perl-File-Temp
# Keep 2-digit version to align with future versions
Version:        %(echo '%{cpan_version}' | sed 's/\(\...\)\(.\)/\1.\2/')
Release:        3%{?dist}
Summary:        Return name and handle of a temporary file safely
License:        GPL+ or Artistic
Group:          Development/Libraries
URL:            http://search.cpan.org/dist/File-Temp/
Source0:        http://www.cpan.org/authors/id/D/DA/DAGOLDEN/File-Temp-%{cpan_version}.tar.gz
BuildArch:      noarch
BuildRequires:  perl
BuildRequires:  perl(ExtUtils::MakeMaker) >= 6.30
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
# Run-time:
BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
# Keep Carp::Heavy optional
BuildRequires:  perl(constant)
BuildRequires:  perl(Cwd)
BuildRequires:  perl(Errno)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(Fcntl) >= 1.03
BuildRequires:  perl(File::Path) >= 2.06
BuildRequires:  perl(File::Spec) >= 0.8
BuildRequires:  perl(IO::Handle)
BuildRequires:  perl(IO::Seekable)
BuildRequires:  perl(overload)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Scalar::Util)
# Symbol not needed
BuildRequires:  perl(vars)
# VMS::Stdio not needed
# Tests:
BuildRequires:  perl(Config)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(FileHandle)
BuildRequires:  perl(List::Util)
BuildRequires:  perl(Test::More)
Requires:       perl(:MODULE_COMPAT_%(eval "`perl -V:version`"; echo $version))
Requires:       perl(File::Path) >= 2.06
Requires:       perl(POSIX)

# Filter unused dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Symbol|VMS::Stdio\\)
# Filter under-specified dependencies
%global __requires_exclude %{__requires_exclude}|^perl\\(File::Path\\)$

Prefix: %{_prefix}

%description
File::Temp can be used to create and open temporary files in a safe way.
There is both a function interface and an object-oriented interface. The
File::Temp constructor or the tempfile() function can be used to return the
name and the open file handle of a temporary file. The tempdir() function
can be used to create a temporary directory.

%prep
%setup -q -n File-Temp-%{cpan_version}
chmod -x misc/benchmark.pl
%fix_shbang_line misc/benchmark.pl

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
%license LICENSE
%{perl_vendorlib}/*

%exclude %{_mandir}

%changelog
* Wed May 15 2019 Michael Hart <michael@lambci.org>
- recompiled for AWS Lambda (Amazon Linux 2) with prefix /opt

* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 0.23.01-3
- Mass rebuild 2013-12-27

* Mon Jul 29 2013 Petr Pisar <ppisar@redhat.com> - 0.23.01-2
- Specify all dependencies

* Mon Apr 15 2013 Petr Pisar <ppisar@redhat.com> - 0.23.01-1
- 0.2301 bump

* Fri Mar 22 2013 Petr Pisar <ppisar@redhat.com> 0.23-1
- Specfile autogenerated by cpanspec 1.78.
