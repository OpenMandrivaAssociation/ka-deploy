%define name    ka-deploy
%define version 0.94.4
%define release %mkrel 6
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
%patch1	-p1
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
* Thu May 05 2011 Antoine Ginies <aginies@mandriva.com> 0.94.4-4mdv2011.0
+ Revision: 669218
- still some unused var to remove
- patches should use .patch extension (better)
- rename with patch extension
- fix another unused var
- fix rebuild on 2011

  + Oden Eriksson <oeriksson@mandriva.com>
    - mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.94.4-2mdv2011.0
+ Revision: 606248
- rebuild

* Mon May 31 2010 Antoine Ginies <aginies@mandriva.com> 0.94.4-1mdv2010.1
+ Revision: 546732
- release 0.94.4
- remove old tarball

* Fri May 07 2010 Antoine Ginies <aginies@mandriva.com> 0.94.3-2mdv2010.1
+ Revision: 543148
- oups ! it is the same version, but no the same release
- add missing script udev_creation.sh

* Fri May 07 2010 Antoine Ginies <aginies@mandriva.com> 0.94.3-1mdv2010.1
+ Revision: 543135
- fix anoying bug to umount $CHROOT/dev

* Fri May 07 2010 Antoine Ginies <aginies@mandriva.com> 0.94.2-1mdv2010.1
+ Revision: 543124
- fix a lot of bugs in fstab, grub preparation, remove udev persistent rules on client node

* Tue May 04 2010 Antoine Ginies <aginies@mandriva.com> 0.94.1-1mdv2010.1
+ Revision: 542126
- remove all old scripts, cleaning the spec file
- new version 0.94.1
- remove old tarball

* Tue May 04 2010 Antoine Ginies <aginies@mandriva.com> 0.93.1-1mdv2010.1
+ Revision: 542041
- update ka script to support UUID, remove old mke2fs static binairie

* Thu Feb 04 2010 Antoine Ginies <aginies@mandriva.com> 0.93-1mdv2010.1
+ Revision: 500720
- dont use pathc on 32b and 64b release (break the ka-d-client), update ka-d.sh script (support of UUID)

* Sun Sep 27 2009 Olivier Blin <oblin@mandriva.com> 0.92-23mdv2010.0
+ Revision: 449781
- do not build with -m32, doesn't exist on arm and mips
  (from Arnaud Patard)

  + Christophe Fergeau <cfergeau@mandriva.com>
    - rebuild

* Tue Jun 17 2008 Thierry Vignaud <tv@mandriva.org> 0.92-21mdv2009.0
+ Revision: 221764
- rebuild
- fix no-buildroot-tag
- kill (multiple!) definitions of %%buildroot on Pixel's request

* Thu Oct 25 2007 Antoine Ginies <aginies@mandriva.com> 0.92-20mdv2008.1
+ Revision: 102042
- move replication.conf to %%sysconfdir

* Thu Oct 25 2007 Antoine Ginies <aginies@mandriva.com> 0.92-19mdv2008.1
+ Revision: 102038
- udpate source, add mke2fs build with dietlibc
- merge patch (no more supported by inria), add various other scripts needed to do a full KA replication

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 0.92-18mdv2008.0
+ Revision: 70278
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Fri Jun 22 2007 Thierry Vignaud <tv@mandriva.org> 0.92-17mdv2008.0
+ Revision: 43000
- fix group

* Thu May 31 2007 Adam Williamson <awilliamson@mandriva.org> 0.92-16mdv2008.0
+ Revision: 32998
- BuildRequires glibc-static-devel
- whoops: really fix ALL groups
- correct group (fixes #27317 and #27318)


* Sun Aug 13 2006 Nicolas Lécureuil <neoclust@mandriva.org> 0.92-14mdv2007.0
- Fix rpmlint warnings

* Fri Aug 11 2006 Erwan Velu <erwan@seanodes.com> 0.92-13mdk
- Rebuild

* Wed Apr 06 2005 <guibo@guibo.mdkc.com> 0.92-12mdk
- add cciss support

* Thu Mar 31 2005 <guibo@guibpiv.guibland.com> 0.92-11mdk
- fix pb of fdisk_commands

* Wed Mar 30 2005 Erwan Velu <erwan@seanodes.com> 0.92-10mdk
- Using -m32 & static flags

* Fri Apr 02 2004 Erwan Velu <erwan@mandrakesoft.com> 0.92-9mdk
- Rebuild

