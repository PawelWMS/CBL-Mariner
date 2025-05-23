Summary:        agent for collecting, processing, aggregating, and writing metrics.
Name:           telegraf
Version:        1.29.4
Release:        16%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Development/Tools
URL:            https://github.com/influxdata/telegraf
Source0:        %{url}/archive/v%{version}.tar.gz#/%{name}-%{version}.tar.gz
# Use the generate_source_tarball.sh script to get the vendored sources.
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         CVE-2023-45288.patch
Patch1:         CVE-2024-28110.patch
Patch2:         CVE-2024-27289.patch
Patch3:         CVE-2024-35255.patch
Patch4:         CVE-2024-37298.patch
Patch5:         CVE-2024-24786.patch
Patch6:         CVE-2024-28180.patch
Patch7:         CVE-2024-45337.patch
Patch8:         CVE-2024-45338.patch
Patch9:         CVE-2025-22868.patch
Patch10:        CVE-2025-22869.patch
Patch11:        CVE-2025-27144.patch
Patch12:        CVE-2025-30204.patch
Patch13:        CVE-2025-22870.patch
Patch14:        CVE-2024-51744.patch
Patch15:        CVE-2025-30215.patch
Patch16:        CVE-2025-22872.patch
BuildRequires:  golang
BuildRequires:  iana-etc
BuildRequires:  systemd-devel
BuildRequires:  tzdata
Requires:       iana-etc
Requires:       logrotate
Requires:       procps-ng
Requires:       shadow-utils
Requires:       systemd
Requires:       tzdata
Requires(postun): %{_sbindir}/groupdel
Requires(postun): %{_sbindir}/userdel
Requires(pre):  %{_sbindir}/groupadd
Requires(pre):  %{_sbindir}/useradd

%description
Telegraf is an agent written in Go for collecting, processing, aggregating, and writing metrics.

Design goals are to have a minimal memory footprint with a plugin system so that developers in
the community can easily add support for collecting metrics from well known services (like Hadoop,
Postgres, or Redis) and third party APIs (like Mailchimp, AWS CloudWatch, or Google Analytics).

%prep
%autosetup -a1 -p1

%build
go build -buildvcs=false -mod=vendor ./cmd/telegraf

%install
mkdir -pv %{buildroot}%{_sysconfdir}/%{name}/%{name}.d
install -m 755 -D %{name} %{buildroot}%{_bindir}/%{name}
install -m 755 -D scripts/%{name}.service %{buildroot}%{_unitdir}/%{name}.service
install -m 755 -D etc/logrotate.d/%{name} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Provide empty config file.
./%{name} config > telegraf.conf
install -m 755 -D telegraf.conf %{buildroot}%{_sysconfdir}/%{name}/telegraf.conf

%check
make test

%pre
getent group telegraf >/dev/null || groupadd -r telegraf
getent passwd telegraf >/dev/null || useradd -c "Telegraf" -d %{_localstatedir}/lib/%{name} -g %{name} \
        -s /sbin/nologin -M -r %{name}

%post
chown -R telegraf:telegraf %{_sysconfdir}/telegraf
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
if [ $1 -eq 0 ] ; then
    getent passwd telegraf >/dev/null && userdel telegraf
    getent group telegraf >/dev/null && groupdel telegraf
fi
%systemd_postun_with_restart %{name}.service

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/telegraf.conf
%license LICENSE
%{_bindir}/telegraf
%{_unitdir}/telegraf.service
%{_sysconfdir}/logrotate.d/%{name}
%dir %{_sysconfdir}/%{name}/telegraf.d

%changelog
* Tue Apr 22 2025 Mayank Singh <mayansingh@microsoft.com> - 1.29.4-16
- Fix CVE-2025-22872 with an upstream patch

* Thu Apr 17 2025 Sudipta Pandit <sudpandit@microsoft.com> - 1.29.4-15
- Patch CVE-2025-30215

* Mon Mar 31 2025 Sreeniavsulu Malavathula <v-smalavathu@microsoft.com> - 1.29.4-14
- Patch to fix CVE-2025-22870, CVE-2024-51744 with an upstream patch

* Mon Mar 31 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.29.4-13
- Patch CVE-2025-30204

* Tue Mar 11 2025 Mayank Singh <mayansingh@microsoft.com> - 1.29.4-12
- Fix CVE-2025-27144 with an upstream patch

* Wed Mar 05 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.29.4-11
- Patch CVE-2025-22868, CVE-2025-22869

* Mon Jan 06 2025 Sumedh Sharma <sumsharma@microsoft.com> - 1.29.4-10
- Add patch for CVE-2024-45337 & CVE-2024-45338.

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.4-9
- Bump release to rebuild with go 1.22.7

* Wed Aug 21 2024 Muhammad Falak <mwani@microsoft.com> - 1.29.4-8
- Address CVE-2024-24786 & CVE-2024-28180

* Thu Jul 11 2024 Sumedh Sharma <sumsharma@microsoft.com> - 1.29.4-7
- Add patch for CVE-2024-37298

* Tue Jun 18 2024 Saul Paredes <saulparedes@microsoft.com> - 1.29.4-6
- Patch CVE-2024-35255

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.4-5
- Bump release to rebuild with go 1.21.11

* Fri May 24 2024 Henry Li <lihl@microsoft.com> - 1.29.4-4
- Add patch to resolve CVE-2024-27289

* Mon May 06 2024 Henry Li <lihl@microsoft.com> - 1.29.4-3
- Re-add patch for CVE-2024-28110

* Thu Apr 18 2024 Chris Gunn <chrisgun@microsoft.com> - 1.29.4-2
- Fix for CVE-2023-45288

* Tue Apr 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.29.4-1
- Auto-upgrade to 1.29.4 - CVE-2023-50658

* Mon Mar 18 2024 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.28.5-5
- Patching CVE-2024-27304 in vendor/github.com/jackc/pgproto3.

* Wed Mar 13 2024 Zhichun Wan <zhichunwan@microsoft.com> - 1.28.5-4
- Address CVE-2024-28110 by patching vendored github.com/cloudevents

* Thu Feb 15 2024 Nan Liu <liunan@microsoft.com> - 1.28.5-3
- Address CVE-2023-48795 by patching vendored golang.org/x/crypto

* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.28.5-2
- Bump release to rebuild with go 1.21.6

* Tue Dec 05 2023 Osama Esmail <osamaesmail@microsoft.com> - 1.28.5-1
- Updating to version 1.28.5 to address critical CVEs
- Fix testing

* Thu Nov 09 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.27.4-1
- Backporting patch for CVE-2023-46129.
- Updating to version 1.27.4.
- Removed invalid, outdated patch.

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.3-4
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.27.3-3
- Bump release to rebuild with updated version of Go.

* Mon Aug 28 2023 Cameron Baird <cameronbaird@microsoft.com> - 1.27.3-2
- Bump release to rebuild with go 1.20.7

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.3-1
- Auto-upgrade to 1.27.3 - resolve vulnerability with jaeger v1.38.0

* Fri Jul 14 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.27.2-1
- Auto-upgrade to 1.27.2 to fix CVE-2023-34231, CVE-2023-25809, CVE-2023-28642

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.0-4
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.0-3
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.26.0-2
- Bump release to rebuild with go 1.19.8

* Wed Mar 29 2023 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.26.0-1
- Updating to version 1.26.0 to address CVEs in vendored sources for "containerd".

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.25.2-3
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.25.2-2
- Bump release to rebuild with go 1.19.6

* Fri Feb 24 2023 Olivia Crain <oliviacrain@microsoft.com> - 1.25.2-1
- Upgrade to latest upstream version to fix the following CVEs in vendored packages:
  CVE-2019-3826, CVE-2022-1996, CVE-2022-29190, CVE-2022-29222, CVE-2022-29189, 
  CVE-2022-32149, CVE-2022-23471

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-6
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.23.0-5
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.23.0-4
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-3
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.23.0-2
- Bump release to rebuild against Go 1.18.5

* Thu Jun 16 2022 Muhammad Falak <mwani@microsoft.com> 1.23.0-1
- Bump version to 1.23.0

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.21.2-2
- Bump release to rebuild with golang 1.18.3

* Tue Jan 18 2022 Neha Agarwal <nehaagarwal@microsoft.com> - 1.21.2-1
- Update to version 1.21.2.
- Modified patch to apply to new version.

* Thu Dec 16 2021 Pawel Winogrodzki <pawelwi@microsoft.com> - 1.14.5-8
- Removing the explicit %%clean stage.

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.14.5-7
- Increment release to force republishing using golang 1.15.13.

* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.14.5-6
- Increment release to force republishing using golang 1.15.11.

* Thu Dec 10 2020 Andrew Phelps <anphel@microsoft.com> 1.14.5-5
- Increment release to force republishing using golang 1.15.

* Thu Oct 15 2020 Pawel Winogrodzki <pawelwi@microsoft.com> 1.14.5-4
- License verified.
- Added %%license macro.
- Fixed source URL.
- Switched to %%autosetup.

* Fri Aug 21 2020 Suresh Babu Chalamalasetty <schalam@microsoft.com> 1.14.5-3
- Add runtime required procps-ng and shadow-utils

* Tue Jul 14 2020 Jonathan Chiu <jochi@microsoft.com> 1.14.5-1
- Update to version 1.14.5

* Tue Sep 03 2019 Mateusz Malisz <mamalisz@microsoft.com> 1.7.4-2
- Initial CBL-Mariner import from Photon (license: Apache2).

* Fri Sep 07 2018 Michelle Wang <michellew@vmware.com> 1.7.4-1
- Update version to 1.7.4 and its plugin version to 1.4.0.

* Mon Sep 18 2017 Alexey Makhalov <amakhalov@vmware.com> 1.3.4-2
- Remove shadow from requires and use explicit tools for post actions

* Tue Jul 18 2017 Dheeraj Shetty <dheerajs@vmware.com> 1.3.4-1
- first version
