Summary:        PostgreSQL database engine
Name:           postgresql
Version:        14.18
Release:        1%{?dist}
License:        PostgreSQL
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Databases
URL:            https://www.postgresql.org
Source0:        https://ftp.postgresql.org/pub/source/v%{version}/%{name}-%{version}.tar.bz2

# Common libraries needed
BuildRequires:  krb5-devel
BuildRequires:  libxml2-devel
BuildRequires:  openldap
BuildRequires:  openssl-devel
BuildRequires:  perl
BuildRequires:  readline-devel
BuildRequires:  tzdata
BuildRequires:  zlib-devel

%if %{with_check}
BuildRequires:  sudo
%endif

Requires:       %{name}-libs = %{version}-%{release}
Requires:       krb5
Requires:       libxml2
Requires:       openldap
Requires:       openssl
Requires:       readline
Requires:       tzdata
Requires:       zlib

%description
PostgreSQL is an object-relational database management system.

%package docs
Summary:        Extra documentation for PostgreSQL

%description docs
The postgresql-docs package includes the documentation.

%package libs
Summary:        Libraries for use with PostgreSQL
Group:          Applications/Databases
# Mariner used to have libpq and libpq-devel as separate packages, following Fedora's packaging scheme,
# but this isn't needed for our use case and overcomplicates our packaging. So, let's ensure that
# (a) the names are provided for compatibility, and
# (b) we obsolete all versions published in Mariner 2.0's repositories (only libpq{,-devel}-12.2-3.cm2)
Provides:       libpq = %{version}-%{release}
Obsoletes:      libpq < 13

%description libs
The postgresql-libs package provides the essential shared libraries for any
PostgreSQL client program or interface. You will need to install this package
to use any other PostgreSQL package or any clients that need to connect to a
PostgreSQL server.

%package        devel
Summary:        Development files for postgresql.
Group:          Development/Libraries
Requires:       postgresql = %{version}-%{release}
# See libs subpackage for explanation of the libpq-devel provides/obsoletes
Provides:       libpq-devel = %{version}-%{release}
Obsoletes:      libpq-devel < 13

%description    devel
The postgresql-devel package contains libraries and header files for
developing applications that use postgresql.

%prep
%autosetup -p1

%build
sed -i '/DEFAULT_PGSOCKET_DIR/s@/tmp@/run/postgresql@' src/include/pg_config_manual.h

./configure \
    --enable-thread-safety \
    --prefix=%{_prefix} \
    --with-ldap \
    --with-libxml \
    --with-openssl \
    --with-gssapi \
    --with-readline \
    --with-system-tzdata=%{_datadir}/zoneinfo \
    --docdir=%{_docdir}/postgresql

%make_build world

%install
%make_install install-world

# For postgresql 10+, commands are renamed
# Ref: https://wiki.postgresql.org/wiki/New_in_postgres_10
ln -sf pg_receivewal %{buildroot}%{_bindir}/pg_receivexlog
ln -sf pg_resetwal %{buildroot}%{_bindir}/pg_resetxlog
ln -sf  pg_waldump %{buildroot}%{_bindir}/pg_xlogdump
%{_fixperms} %{buildroot}/*

# Remove anything related to Python 2.  These have no need to be
# around as only Python 3 is supported.
rm -f %{buildroot}%{_pgdatadir}/extension/*plpython2u* \
      %{buildroot}%{_pgdatadir}/extension/*plpythonu-* \
      %{buildroot}%{_pgdatadir}/extension/*_plpythonu.control

# Remove currently unnecessary man pages.
rm -f %{buildroot}%{_mandir}/man1/* \
      %{buildroot}%{_mandir}/man3/* \
      %{buildroot}%{_mandir}/man7/*

%check
chown -Rv nobody:nogroup .
sudo -u nobody -s /bin/bash -c "PATH=$PATH make -k check"

%ldconfig_scriptlets

%files
%defattr(-,root,root)
%license COPYRIGHT
%{_bindir}/initdb
%{_bindir}/oid2name
%{_bindir}/pg_amcheck
%{_bindir}/pg_archivecleanup
%{_bindir}/pg_basebackup
%{_bindir}/pg_checksums
%{_bindir}/pg_controldata
%{_bindir}/pg_ctl
%{_bindir}/pg_receivewal
%{_bindir}/pg_receivexlog
%{_bindir}/pg_recvlogical
%{_bindir}/pg_resetwal
%{_bindir}/pg_resetxlog
%{_bindir}/pg_rewind
%{_bindir}/pg_test_fsync
%{_bindir}/pg_test_timing
%{_bindir}/pg_upgrade
%{_bindir}/pg_verifybackup
%{_bindir}/pg_waldump
%{_bindir}/pg_xlogdump
%{_bindir}/pgbench
%{_bindir}/postgres
%{_bindir}/postmaster
%{_bindir}/vacuumlo
%{_datadir}/postgresql/*
%{_libdir}/postgresql/*
%{_docdir}/postgresql/extension/*.example
%exclude %{_datadir}/postgresql/pg_service.conf.sample
%exclude %{_datadir}/postgresql/psqlrc.sample

%files docs
%defattr(-,root,root)
%{_docdir}/postgresql/*

%files libs
%{_bindir}/clusterdb
%{_bindir}/createdb
%{_bindir}/createuser
%{_bindir}/dropdb
%{_bindir}/dropuser
%{_bindir}/ecpg
%{_bindir}/pg_config
%{_bindir}/pg_dump
%{_bindir}/pg_dumpall
%{_bindir}/pg_isready
%{_bindir}/pg_restore
%{_bindir}/psql
%{_bindir}/reindexdb
%{_bindir}/vacuumdb
%{_libdir}/libecpg*.so.*
%{_libdir}/libpgtypes*.so.*
%{_libdir}/libpq*.so.*
%{_libdir}/libpgcommon_shlib.a
%{_libdir}/libpgport_shlib.a
%{_datadir}/postgresql/pg_service.conf.sample
%{_datadir}/postgresql/psqlrc.sample

%files devel
%defattr(-,root,root)
%{_includedir}/*
%{_libdir}/pkgconfig/*
%{_libdir}/libecpg*.so
%{_libdir}/libpgtypes*.so
%{_libdir}/libpq*.so
%{_libdir}/libpgcommon.a
%{_libdir}/libpgfeutils.a
%{_libdir}/libpgport.a
%{_libdir}/libpq.a
%{_libdir}/libecpg.a
%{_libdir}/libecpg_compat.a
%{_libdir}/libpgtypes.a

%changelog
* Mon May 19 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 14.18-1
- Auto-upgrade to 14.18 - for CVE-2025-4207

* Mon Feb 17 2025 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 14.16-1
- Auto-upgrade to 14.16 - to fix CVE-2025-1094

* Mon Nov 18 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 14.14-1
- Auto-upgrade to 14.14 - CVE-2024-10976, CVE-2024-10977, CVE-2024-10978, CVE-2024-10979

* Mon Aug 12 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 14.13-1
- Auto-upgrade to 14.13 - CVE-2024-7348

* Thu May 16 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 14.12-1
- Auto-upgrade to 14.12 - CVE-2024-4317

* Tue Feb 27 2024 Thien Trung Vuong <cblmargh@microsoft.com> - 14.11-1
- Update to version 14.11 to fix CVE-2024-0985
- Added the 'docs' subpackage.

* Fri Dec 29 2023 Neha Agarwal <nehaagarwal@microsoft.com> - 14.10-1
- Upgrade to 14.10 to fix CVE-2023-5868, CVE-2023-5869 and CVE-2023-5870

* Tue Jun 20 2023 Bala <balakumaran.kannan@microsoft.com> - 14.8-1
- Upgrade to 14.8 to fix CVE-2023-2454, CVE-2023-2455 and CVE-2022-41862

* Wed Sep 07 2022 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 14.5-1
- Upgrade to 14.5

* Fri Apr 29 2022 Olivia Crain <oliviacrain@microsoft.com> - 14.2-2
- Add provides, obsoletes for libpq and libpq-devel packages

* Wed Apr 13 2022 Henry Beberman <henry.beberman@microsoft.com> - 14.2-1
- Update package version to resolve CVE-2021-23214 and CVE-2021-23222
- Add pg_verifybackup and pg_amcheck, remove pg_standby

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.7-2
- Removing the explicit %%clean stage.

* Fri Jun 11 2021 Henry Beberman <henry.beberman@microsoft.com> - 12.7-1
- Update to version 12.7 to resolve CVE-2021-32027.

* Tue Mar 02 2021 Neha Agarwal <nehaagarwal@microsoft.com> - 12.6-1
- Update package version to resolve CVE-2021-20229 and CVE-2021-3393.

* Wed Dec 09 2020 Andrew Phelps <anphel@microsoft.com> - 12.5-2
- Add sudo package to resolve test issue.

* Mon Nov 23 2020 Henry Beberman <henry.beberman@microsoft.com> - 12.5-1
- Upgrading to 12.5 to fix CVE-2020-25695 and CVE-2020-25694.

* Tue Nov 03 2020 Pawel Winogrodzki <pawelwi@microsoft.com> - 12.4-1
- Upgrading to 12.4 to fix CVE-2020-14349 and CVE-2020-14350.

* Sat May 09 2020 Nick Samson <nisamson@microsoft.com> - 12.1-3
- Added %%license line automatically

* Thu Mar 26 2020 Henry Beberman <henry.beberman@microsoft.com> - 12.1-2
- Manually run header generation.

* Fri Mar 13 2020 Paul Monson <paulmon@microsoft.com> - 12.1-1
- Update to version 12.1. License verified.

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> - 10.5-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 21 2018 Dweep Advani <dadvani@vmware.com> - 10.5-1
- Updated to version 10.5

* Tue Mar 27 2018 Dheeraj Shetty <dheerajs@vmware.com> - 9.6.8-1
- Updated to version 9.6.8 to fix CVE-2018-1058

* Mon Feb 12 2018 Dheeraj Shetty <dheerajs@vmware.com> - 9.6.7-1
- Updated to version 9.6.7

* Mon Nov 27 2017 Xiaolin Li <xiaolinl@vmware.com> - 9.6.6-1
- Updated to version 9.6.6

* Fri Sep 08 2017 Xiaolin Li <xiaolinl@vmware.com> - 9.6.5-1
- Updated to version 9.6.5

* Tue Aug 15 2017 Xiaolin Li <xiaolinl@vmware.com> - 9.6.4-1
- Updated to version 9.6.4

* Thu Aug 10 2017 Rongrong Qiu <rqiu@vmware.com> - 9.6.3-3
- add sleep 5 when initdb in make check for bug 1900371

* Wed Jul 05 2017 Divya Thaluru <dthaluru@vmware.com> - 9.6.3-2
- Added postgresql-devel

* Tue Jun 06 2017 Divya Thaluru <dthaluru@vmware.com> - 9.6.3-1
- Upgraded to 9.6.3

* Mon Apr 03 2017 Rongrong Qiu <rqiu@vmware.com> - 9.6.2-1
- Upgrade to 9.6.2 for Photon upgrade bump

* Thu Dec 15 2016 Xiaolin Li <xiaolinl@vmware.com> - 9.5.3-6
- Applied CVE-2016-5423.patch

* Thu Nov 24 2016 Alexey Makhalov <amakhalov@vmware.com> - 9.5.3-5
- Required krb5-devel.

* Mon Oct 03 2016 ChangLee <changLee@vmware.com> - 9.5.3-4
- Modified %check

* Thu May 26 2016 Xiaolin Li <xiaolinl@vmware.com> - 9.5.3-3
- Add tzdata to buildrequires and requires.

* Tue May 24 2016 Priyesh Padmavilasom <ppadmavilasom@vmware.com> - 9.5.3-2
- GA - Bump release of all rpms

* Fri May 20 2016 Divya Thaluru <dthaluru@vmware.com> - 9.5.3-1
- Updated to version 9.5.3

* Wed Apr 13 2016 Michael Paquier <mpaquier@vmware.com> - 9.5.2-1
- Updated to version 9.5.2

* Tue Feb 23 2016 Xiaolin Li <xiaolinl@vmware.com> - 9.5.1-1
- Updated to version 9.5.1

* Thu Jan 21 2016 Xiaolin Li <xiaolinl@vmware.com> - 9.5.0-1
- Updated to version 9.5.0

* Thu Aug 13 2015 Divya Thaluru <dthaluru@vmware.com> - 9.4.4-1
- Update to version 9.4.4.

* Mon Jul 13 2015 Alexey Makhalov <amakhalov@vmware.com> - 9.4.1-2
- Exclude /usr/lib/debug

* Fri May 15 2015 Sharath George <sharathg@vmware.com> - 9.4.1-1
- Initial build. First version
