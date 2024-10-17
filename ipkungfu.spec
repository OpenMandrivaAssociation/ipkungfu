Summary: 	Iptables-based Linux firewall
Name:		ipkungfu
Version:	0.6.1
Release:	8
License:	GPL
Group:		System/Configuration/Networking
Source:		http://linuxkungfu.org/ipkungfu/%{name}-%{version}.tar.bz2
Source1:	%{name}.init.bz2
URL:		https://www.linuxkungfu.org/
BuildArch:	noarch
Requires:	userspace-ipfilter
Buildrequires:	rpm-helper
Buildrequires:  iptables
Buildrequires:  iptables-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
IPKungFu is an iptables-based Linux firewall. It aims to simplify 
the configuration of Internet connection sharing, port forwarding, 
and packet filtering.

%prep
%setup -q

%build
%configure
%make

%install
rm -rf $RPM_BUILD_ROOT

# Create our directories
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/%{name} $RPM_BUILD_ROOT%{_mandir}/man8 $RPM_BUILD_ROOT%{_initrddir} $RPM_BUILD_ROOT%{_sbindir} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/

# install the files
bzcat %{SOURCE1} > 		$RPM_BUILD_ROOT%{_initrddir}/%{name}
for file in files/conf/*.conf; do
	install $file $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/
done
install %{name} 		$RPM_BUILD_ROOT%{_sbindir}
install man/%{name}.8		$RPM_BUILD_ROOT%{_mandir}/man8/

cat << EOF > $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/%{name} 
# this version of ipkungfu need to be configurated before
# it run, and, in order to not block people who install
# this rpm with a unconfigurated firewall, it will not run
# until you uncomment this line
#
# This was made to remind you to force you to configure
# ipkungfu before running it, in order to not break your internet
# connection.
#
# The configuration is in /etc/ipkungfu/
# and the doc in /usr/share/doc/ipkungfu*
#
#IPKF_CONFIGURATED=yes
EOF

# Fix perms
chmod +x $RPM_BUILD_ROOT%{_initrddir}/%{name}
chmod a-x $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/*

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
%_post_service %name
if [ $1 -ne "1" ] ; then
	if [ ! -f  %{_sysconfdir}/sysconfig/%{name} ];
	then 
		echo "IPKF_CONFIGURATED=yes" >> %{_sysconfdir}/sysconfig/%{name}
	else
		! grep -q "IPKF_CONFIGURATED" %{_sysconfdir}/sysconfig/%{name} && echo "IPKF_CONFIGURATED=yes" >> %{_sysconfdir}/sysconfig/%{name}
	fi
fi

%preun
%_preun_service %name 

%files
%defattr(-,root,root)
%doc ChangeLog FAQ README
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}.8.*
%{_initrddir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.conf
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Fri Dec 10 2010 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-7mdv2011.0
+ Revision: 619679
- the mass rebuild of 2010.0 packages

* Fri Sep 11 2009 Thierry Vignaud <tv@mandriva.org> 0.6.1-6mdv2010.0
+ Revision: 437967
- rebuild

* Sat Oct 25 2008 Oden Eriksson <oeriksson@mandriva.com> 0.6.1-5mdv2009.1
+ Revision: 297272
- fix deps
- rebuild

* Thu Jul 24 2008 Thierry Vignaud <tv@mandriva.org> 0.6.1-4mdv2009.0
+ Revision: 247251
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 0.6.1-2mdv2008.1
+ Revision: 170898
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Fri Jul 27 2007 Funda Wang <fwang@mandriva.org> 0.6.1-1mdv2008.0
+ Revision: 56239
- New version 0.6.1
- Import ipkungfu



* Tue Feb 14 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.6.0-2mdk
- Fix BuildRequires

* Sun Feb 12 2006 Eskild Hustvedt <eskild@mandriva.org> 0.6.0-1mdk
- New release 0.6.0 (based upon Buchan Milne's spec)
- Spec cleanups

* Tue Jan 03 2005 Lenny Cartier <lenny@mandriva.com> 0.5.2-6mdk
- rebuild

* Thu Mar 18 2004 Michael Scherer <misc@mandrake.org> 0.5.2-5mdk
- fix a typo ( /me really sucks )
- fix upgrade script
 
* Thu Mar 18 2004 Michael Scherer <misc@mandrake.org> 0.5.2-4mdk
- fix #9014, chmod +x on initscript

* Sun Jan 25 2004 Marcel Pol <mpol@mandrake.org> 0.5.2-3mdk
- make sure that iptables matches the running kernel

* Wed Dec 17 2003 Marcel Pol <mpol@mandrake.org> 0.5.2-2mdk
- depend on userspace-ipfilter

* Tue Nov 11 2003 Michael Scherer <scherer.michael@free.fr> 0.5.2-1mdk
- new init script, with idea from  Michael Spivak <phazeman@netvision.net.il>
- from Michael Spivak <phazeman@netvision.net.il>
  - New version 0.5.2

* Fri Jun 20 2003 Lenny Cartier <lenny@mandrakesoft.com> 0.5.0-3mdk
- from Sean Donner <siegex@identityflux.com> :
	- Added a patch so that the init script points to the correct location

* Wed Jun 03 2003 Sean Donner <siegex@identityflux.com> 0.5.0-2mdk
- Updated spec file to comply with rpmlint rules

* Tue Jun 03 2003 Sean Donner <siegex@identityflux.com> 0.5.0-1mdk
- Made numerous changes the spec file to comply with Mandrake contrib rules

* Mon Jan 20 2003 TJ Fontaine <tjfontaine@clemlumber.com> 0.3.2-1tjf
- Initial Release
