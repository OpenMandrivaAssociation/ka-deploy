%define name    ka-deploy
%define version 0.94.4
%define release %mkrel 4
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
Patch1:		ka-deploy_fix_unused_pdata_var.patch
Url:            http://kadeploy.imag.fr/
BuildRequires:	glibc-static-devel

%description
Ka-deploy is a tool for cloning large numbers of machines on a cluster

%package server
Summary:        Ka-deploy cluster installation solution - server host side
Group:          System/Cluster
Requires:       coreutils bind-utils, syslinux >= 1.67, clusterscripts-server-pxe
Obsoletes:	ka-deploy-server-host
License:        GPL

%description server
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
%patch1	-p0
%build
# remove all the CVS directories
rm -rf `find -type d -name "CVS"`

# compile
cd src && make

%install
rm -Rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir}
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
install -m 755 scripts/udev_creation.sh $RPM_BUILD_ROOT%{_bindir}/
install -m 755 scripts/replication.conf $RPM_BUILD_ROOT%{_sysconfdir}/ka

install -m 644 doc/ka-d.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d.1
install -m 644 doc/ka-deploy.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-deploy.1
ln -s ka-d.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d.sh.1
ln -s ka-deploy.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d-server.1
ln -s ka-deploy.1 $RPM_BUILD_ROOT%{_mandir}/man1/ka-d-client.1


%clean
rm -rf $RPM_BUILD_ROOT

%files server
%doc README BUGS INSTALL doc 


%files source-node
%defattr(-,root,root)
%doc doc/duplication.html
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/ka
%doc %{_mandir}/man1/ka-d*
%{_datadir}/%{name}-%{version}


%changelog
