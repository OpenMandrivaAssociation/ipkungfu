Summary: 	Iptables-based Linux firewall
Name:		ipkungfu
Version:	0.6.1
Release:	%mkrel 5
License:	GPL
Group:		System/Configuration/Networking
Source:		http://linuxkungfu.org/ipkungfu/%{name}-%{version}.tar.bz2
Source1:	%{name}.init.bz2
URL:		http://www.linuxkungfu.org/
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
