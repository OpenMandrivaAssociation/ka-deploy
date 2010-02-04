%define name    ka-deploy
%define version 0.93
%define release %mkrel 1
%define tftpbase tftpboot
%define dont_strip 1


Release:        %{release}
Version:        %{version}
Summary:        Ka-deploy cluster installation solution
Name:           %{name}
License:        GPL
Group:          System/Cluster
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Source:         %{name}-%{version}.tar.bz2
Patch0:		ka-deploy_dont_use_m32.patch
Url:            http://kadeploy.imag.fr/
BuildRequires:	glibc-static-devel

%description
Ka-deploy is a tool for cloning large numbers of machines on a cluster

%package server-host
Summary:        Ka-deploy cluster installation solution - server host side
Group:          System/Cluster
Requires:       coreutils bind-utils, syslinux >= 1.67
License:        GPL

%description server-host
Ka-deploy is a tool for cloning large numbers of machines on a cluster
This package is to be installed on a server

%package source-node
Summary:        Ka-deploy cluster installation solution - source node side
Group:          System/Cluster
Requires:       coreutils
License:        GPL

%description source-node
Ka-deploy is a tool for cloning large numbers of machines on a cluster
This package is to be installed on the source node

%prep
%setup -q -n %name-%version
%ifarch mips arm
%patch0 -p1 -b .m32
%endif
%build
# remove all the CVS directories
rm -rf `find -type d -name "CVS"`

# e2fsprog should provide a static binairies
# or latest busybox 1.6.0 to get mke2fs
# i will ask for an update of busybox
EXCLUDE_FROM_STRIP="%{_bindir}/mke2fs.static"
export EXCLUDE_FROM_STRIP
# compile
cd src && make

%install
rm -Rf $RPM_BUILD_ROOT
#SERVER SIDE
mkdir -p $RPM_BUILD_ROOT/%{tftpbase}/ka
mkdir -p $RPM_BUILD_ROOT/%{tftpbase}/ka/pxelinux.cfg
mkdir -p $RPM_BUILD_ROOT/%{tftpbase}/ka/pxelinux.cfg/IP
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ka
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

install -m 755 scripts/ka_pxe_step $RPM_BUILD_ROOT/%{tftpbase}/ka/ka_pxe_step
install -m 644 scripts/template  $RPM_BUILD_ROOT/%{tftpbase}/ka/pxelinux.cfg/template
install -m 644 scripts/ka.conf $RPM_BUILD_ROOT/etc/ka/ka.conf
install -m 644 scripts/ka.funcs $RPM_BUILD_ROOT/etc/ka/ka.funcs
ln -s pxelinux.cfg/template $RPM_BUILD_ROOT/%{tftpbase}/ka/template
#install -m 644 syslinux-1.67/pxelinux.0 $RPM_BUILD_ROOT/%{tftpbase}/ka/pxelinux.0
install -m 755 scripts/configure_server.sh $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/configure_server.sh
install -m 755 scripts/test_services.sh $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/test_services.sh
install -m 644 doc/ka-deploy.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-deploy.1

ln -s ka-deploy.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d-server.1
ln -s ka-deploy.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d-client.1

#install -m 644 kernel/vmlinuz-nfsroot $RPM_BUILD_ROOT/%{tftpbase}/ka/vmlinuz-nfsroot
#END OF SERVER SIDE

#BEGINING OF CLIENT SIDE
mkdir -p $RPM_BUILD_ROOT/usr/bin/
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d/
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/ka

install -m 755 src/ka-d-server $RPM_BUILD_ROOT%{_bindir}/ka-d-server
install -m 755 src/ka-d-client $RPM_BUILD_ROOT%{_bindir}/ka-d-client
install -m 755 scripts/ka-d.sh $RPM_BUILD_ROOT%{_bindir}/ka-d.sh
install -m 755 scripts/bootable_flag.sh $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/fdisk_to_desc $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/gen_modprobe_conf.pl $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/ka-d.sh $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/ka_replication.sh $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/make_initrd_grub $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/make_initrd_lilo $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/prepare_node.sh $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/send_status.pl $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/status_node.pl $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/store_log.sh $RPM_BUILD_ROOT%{_bindir}/
# mke2fs built with -static
install -m 755 scripts/mke2fs.static $RPM_BUILD_ROOT%{_bindir}/mke2fs.static
install -m 755 scripts/replication.conf $RPM_BUILD_ROOT%{_sysconfdir}/ka

install -m 644 doc/ka-d.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d.1
ln -s ka-d.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d.sh.1
# END OF CLIENT SIDE



%clean
rm -rf $RPM_BUILD_ROOT

%post server-host
cp -f /usr/lib/syslinux/pxelinux.0 /%{tftpbase}/ka/pxelinux.0
# Add our IP address in the tftpserver file
#/sbin/ifconfig | grep -v 127.0.0.1 | grep "inet addr" | sed 's/^.*inet addr:\([^ ]*\) .*$/\1/g' | tail -n 1 > /%{tftpbase}/NFSROOT/tftpserver
# will be done by the configuration script

%files server-host
%defattr(-,root,root)

%doc README BUGS INSTALL doc 
%doc %{_mandir}/man1/ka-d-server.*
%doc %{_mandir}/man1/ka-d-client.*
%doc %{_mandir}/man1/ka-deploy.*

%config(noreplace) %{_sysconfdir}/ka
/%{tftpbase}/ka
%{_datadir}/%{name}-%{version}


%files source-node
%defattr(-,root,root)

%config(noreplace) %{_sysconfdir}/ka
%doc %{_mandir}/man1/ka-deploy.*
%doc %{_mandir}/man1/ka-d-server.*
%doc %{_mandir}/man1/ka-d.*

%{_bindir}/*
%{_datadir}/%{name}-%{version}


%changelog
