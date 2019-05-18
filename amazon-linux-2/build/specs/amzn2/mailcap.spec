Name:           mailcap
Version:        2.1.41
Release:        2%{?dist}
Summary:        Helper application and MIME type associations for file types

Group:          System Environment/Base
License:        Public Domain and MIT
URL:            http://git.fedorahosted.org/git/mailcap.git
Source0:        https://fedorahosted.org/released/mailcap/%{name}-%{version}.tar.xz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

%description
The mailcap file is used by the metamail program.  Metamail reads the
mailcap file to determine how it should display non-text or multimedia
material.  Basically, mailcap associates a particular type of file
with a particular program that a mail agent or other program can call
in order to handle the file.  Mailcap should be installed to allow
certain programs to be able to handle non-text files.

Also included in this package is the mime.types file which contains a
list of MIME types and their filename "extension" associations, used
by several applications e.g. to determine MIME types for filenames.


%prep
%setup -q


%build


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT sysconfdir=%{_sysconfdir} mandir=%{_mandir}


%check
make check


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING NEWS
%config(noreplace) %{_sysconfdir}/mailcap
%config(noreplace) %{_sysconfdir}/mime.types
%{_mandir}/man4/mailcap.*


%changelog
* Fri Dec 27 2013 Daniel Mach <dmach@redhat.com> - 2.1.41-2
- Mass rebuild 2013-12-27

* Tue May 14 2013 Ville Skyttä <ville.skytta@iki.fi> - 2.1.41-1
- Update to 2.1.41.
- Fix bogus dates in %%changelog.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.40-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Aug  5 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.1.40-1
- Update to 2.1.40.

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.39-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Ville Skyttä <ville.skytta@iki.fi> - 2.1.39-1
- Update to 2.1.39.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.38-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Aug 16 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.1.38-1
- Update to 2.1.38.

* Tue Mar 29 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.1.37-1
- Update to 2.1.37.

* Tue Feb 22 2011 Ville Skyttä <ville.skytta@iki.fi> - 2.1.36-1
- Update to 2.1.36.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.35-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec  2 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.1.35-2
- Fix URL tag (#659210, Matt McCutchen).

* Wed Oct 13 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.1.35-1
- Update to 2.1.35.

* Tue Aug 24 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.1.34-1
- Update to 2.1.34.

* Sat Jul  3 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.1.33-1
- Update to 2.1.33, fixes #604924.

* Fri Mar 19 2010 Ville Skyttä <ville.skytta@iki.fi> - 2.1.32-1
- Update to 2.1.32, fixes #546116.

* Tue Nov 17 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.1.31-1
- Update to 2.1.31, fixes #529584.

* Sat Sep 19 2009 Ville Skyttä <ville.skytta@iki.fi> - 2.1.30-1
- Update to 2.1.30, see NEWS for details.
- Improve summary and description.
- Add MIT to License: for mailcap.4 man page.
- Specfile cleanup.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.29-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1.29-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Dec 15 2008 Miroslav Lichvar <mlichvar@redhat.com> 2.1.29-1
- update mime.types (Ville Skyttä) (#476455)

* Fri Feb 15 2008 Miroslav Lichvar <mlichvar@redhat.com> 2.1.28-1
- add new entries from perl-libwww-perl's media.types
  (Ville Skyttä) (#432290)

* Thu Feb 07 2008 Miroslav Lichvar <mlichvar@redhat.com> 2.1.27-1
- associate *.ent with text/xml-external-parsed-entity
  (Ville Skyttä) (#431722)

* Tue Jan 22 2008 Miroslav Lichvar <mlichvar@redhat.com> 2.1.26-1
- use xdg-open (Ville Skyttä) (#388481)
- spec cleanup (#226116)

* Tue Jul 10 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.1.25-1
- add image/vnd.microsoft.icon to mime.types (#247222)

* Mon Jun 18 2007 Miroslav Lichvar <mlichvar@redhat.com> 2.1.24-1
- add text/x-vcard to mime.types (#243889)
- mark configs noreplace, cleanup spec a bit

* Tue Sep 05 2006 Miroslav Lichvar <mlichvar@redhat.com> 2.1.23-1
- add video/x-flv to mime.types (#205239)

* Mon Aug 07 2006 Miroslav Lichvar <mlichvar@redhat.com> 2.1.22-1
- add java/mobile mime types (#201512 <ville.skytta@iki.fi>)

* Tue Jul 18 2006 Miroslav Lichvar <mlichvar@redhat.com> 2.1.21-1
- add audio and video x-ms mime types (#197840)

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 2.1.20-1.1
- rebuild

* Mon Feb 13 2006 Miroslav Lichvar <mlichvar@redhat.com> 2.1.20-1
- add OpenOffice.org 2.0 mime types (#173789)

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Mar  7 2005 Bill Nottingham <notting@redhat.com> 2.1.19-1
- s/ggv/evince/ (#150509)

* Fri Jan 21 2005 Bill Nottingham <notting@redhat.com> 2.1.18-1
- add iso, img to octet-stream (#142459 <ville.skytta@iki.fi>)

* Mon Oct 11 2004 Bill Nottingham <notting@redhat.com> 2.1.17-1
- pdfs -> back to ggv

* Thu Sep 23 2004 Bill Nottingham <notting@redhat.com> 2.1.16-1
- eog -> gthumb
- pdfs -> gpdf

* Mon May  3 2004 Bill Nottingham <notting@redhat.com> 2.1.15-1
- xpdf/gv -> ggv (#118401)
- add application/x-bittorrent (#118752)

* Fri Jul 11 2003 Bill Nottingham <notting@redhat.com> 2.1.14-1
- add application/ogg and OpenOffice.org mime.types

* Fri Feb  7 2003 Bill Nottingham <notting@redhat.com> 2.1.13-1
- resync mime.types with apache
- clean out mailcap some

* Tue Sep  3 2002 Bill Nottingham <notting@redhat.com> 2.1.12-1
- add application/x-ogg to mime.types

* Fri Jul 19 2002 Jens Petersen <petersen@redhat.com> 2.1.11-1
- use eog instead of ee

* Tue Jun 18 2002 Nalin Dahyabhai <nalin@redhat.com> 2.1.10-1
- resync mime.types with apache 1.3.26

* Mon Dec 24 2001 Bill Nottingham <notting@rehdat.com> 2.1.9-1
- fix Sep. 17 changes (#57362)

* Tue Oct 23 2001 Nalin Dahyabhai <nalin@redhat.com> 2.1.8-1
- resync mime.types with apache 1.3.22

* Mon Sep 17 2001 Bill Nottingham <notting@redhat.com> 2.1.7-1
- associate PS files with gv (#53734)

* Fri Aug 10 2001 Bill Nottingham <notting@redhat.com>
- switch gtv & xanim order (#51408)

* Tue Jul 17 2001 Bill Nottingham <notting@redhat.com>
- use htmlview for text/html (#48141)

* Wed Mar 21 2001 Tim Waugh <twaugh@redhat.com> 2.1.4-2
- Use gtv not xanim for video/mpeg, since we no longer ship the codecs.

* Thu Jan 18 2001 Bill Nottingham <notting@redhat.com>
- use gpg, not pgp (#13816, others)

* Sat Jan  6 2001 Bill Nottingham <notting@redhat.com>
- fix typo (#23409)

* Thu Dec 28 2000 Bill Nottingham <notting@redhat.com>
- reintegrate stuff into the package so it doesn't get lost 

* Thu Dec 28 2000 Than Ngo <than@redhat.com>
- add ms(TM) word document entry (Bug #17474)
- bzip2 sources

* Mon Jun 12 2000 Preston Brown <pbrown@redhat.com>
- add wap entries

* Fri Jun  9 2000 Bill Nottingham <notting@redhat.com>
- remove mailcap.vga

* Thu Feb  3 2000 Bill Nottingham <notting@redhat.com>
- handle compressed man pages

* Tue Jan 18 2000 Bill Nottingham <notting@redhat.com>
- add .bz2

* Thu Jan 13 2000 Bill Nottingham <notting@redhat.com>
- add tgz/gz to gzip

* Wed Jun 16 1999 Bill Nottingham <notting@redhat.com>
- rpm files are RPM files. :)

* Sat May 15 1999 Jeff Johnson <jbj@redhat.com>
- fix typo in pdf entry (#2618).

* Mon Mar 29 1999 Bill Nottingham <notting@redhat.com>
- comment out play

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- updated mime type for images from xv to ee
- cleaned up for our new version of the package which is in CVS

* Sat Mar 13 1999 Matt Wilson <msw@redhat.com>
- updated mime.types

* Fri Feb 12 1999 Bill Nottingham <notting@redhat.com>
- comment out backticked %%variables to work around security problems

* Wed Jan 06 1999 Cristian Gafton <gafton@redhat.com>
- glibc version 2.1

* Mon Sep 21 1998 Bill Nottingham <notting@redhat.com>
- we don't ship tracker, use mikmod instead

* Wed Jul 29 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- added /etc/mime.types from mutt to this package to make it universal

* Tue Sep 09 1997 Erik Troan <ewt@redhat.com>
- made a noarch package
