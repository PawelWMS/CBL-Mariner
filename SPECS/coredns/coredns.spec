%global debug_package %{nil}

Summary:        Fast and flexible DNS server
Name:           coredns
Version:        1.11.1
Release:        19%{?dist}
License:        Apache License 2.0
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          System Environment/Libraries
URL:            https://github.com/coredns/coredns
#Source0:       https://github.com/coredns/coredns/archive/v%%{version}.tar.gz
Source0:        %{name}-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/coredns/coredns/archive/v%%{version}.tar.gz -O %%{name}-%%{version}.tar.gz
#   2. tar -xf %%{name}-%%{version}.tar.gz
#   3. cd %%{name}-%%{version}
#   4. go mod vendor
#   5. tar  --sort=name \
#           --mtime="2021-04-26 00:00Z" \
#           --owner=0 --group=0 --numeric-owner \
#           --pax-option=exthdr.name=%d/PaxHeaders/%f,delete=atime,delete=ctime \
#           -cf %%{name}-%%{version}-vendor.tar.gz vendor
#
#   NOTES:
#       - You require GNU tar version 1.28+.
#       - The additional options enable generation of a tarball with the same hash every time regardless of the environment.
#         See: https://reproducible-builds.org/docs/archives/
#       - For the value of "--mtime" use the date "2021-04-26 00:00Z" to simplify future updates.
Source1:        %{name}-%{version}-vendor.tar.gz
Patch0:         makefile-buildoption-commitnb.patch
Patch1:         CVE-2023-44487.patch
Patch2:         CVE-2023-49295.patch
Patch3:         CVE-2024-22189.patch
Patch4:         CVE-2023-45288.patch
Patch5:         CVE-2024-0874.patch
Patch6:         CVE-2024-24786.patch
Patch7:         CVE-2025-22868.patch
# Patch to fix the package test suite due to external akamai update
# https://github.com/coredns/coredns/commit/d8ecde1080e7cbbeb98257ba4e03a271f16b4cd9
Patch8:         coredns-example-net-test.patch
Patch9:         CVE-2024-53259.patch
Patch10:        CVE-2025-30204.patch
Patch11:        CVE-2025-29786.patch
Patch12:        CVE-2024-51744.patch
Patch13:        CVE-2025-47950.patch

BuildRequires:  msft-golang

%description
CoreDNS is a fast and flexible DNS server.

%prep
%autosetup -N
# Apply vendor before patching
tar --no-same-owner -xf %{SOURCE1}
%autopatch -p1

%build
export BUILDOPTS="-mod=vendor -v"
# set commit number that correspond to the github tag for that version
export GITCOMMIT="ae2bbc29be1aaae0b3ded5d188968a6c97bb3144"
make

%check
# From go.test.yml
go install github.com/fatih/faillint@latest && \
(cd request && go test -v -mod=vendor -race ./...) && \
(cd core && go test -v -mod=vendor -race ./...) && \
(cd coremain && go test -v -mod=vendor -race ./...) && \
(cd plugin && go test -v -mod=vendor -race ./...) && \
(cd test && go test -v -mod=vendor -race ./...) && \
./coredns -version

%install
install -m 755 -d %{buildroot}%{_bindir}
install -p -m 755 -t %{buildroot}%{_bindir} %{name}

%files
%defattr(-,root,root)
%license LICENSE
%{_bindir}/%{name}

%changelog
* Tue Jun 17 2025 Aninda Pradhan <v-anipradhan@microsoft.com> - 1.11.1-19
- Fix CVE-2025-47950 with an upstream patch

* Fri Apr 11 2025 Archana Shettigar <v-shettigara@microsoft.com> - 1.11.1-18
- Patch CVE-2024-51744

* Mon Mar 31 2025 Kshitiz Godara <kgodara@microsoft.com> - 1.11.1-17
- Fix CVE-2025-29786 with an upstream patch

* Mon Mar 31 2025 Kshitiz Godara <kgodara@microsoft.com> - 1.11.1-16
- Fix CVE-2025-30204 with an upstream patch

* Wed Mar 19 2025 Mayank Singh <mayansingh@microsoft.com> - 1.11.1-15
- Fix CVE-2024-53259 with an upstream patch

* Mon Mar 03 2025 Sam Meluch <sammeluch@microsoft.com> - 1.11.1-14
- Fix package test with upstream patch

* Mon Mar 03 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.11.1-13
- Fix CVE-2025-22868 with an upstream patch

* Mon Dec 09 2024 Kavya Sree Kaitepalli <kkaitepalli@microsoft.com> - 1.11.1-12
- Patch for CVE-2024-24786

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.1-11
- Bump release to rebuild with go 1.22.7

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 1.11.1-10
- Drop requirement on a specific version of golang

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.11.1-9
- Bump release to rebuild with go 1.21.11

* Mon May 06 2024 Archana Choudhary <archana1@microsoft.com> - 1.11.1-8
- Patched cache plugin to address CVE-2024-0874

* Thu Apr 18 2024 Chris Gunn <chrisgun@microsoft.com> - 1.11.1-7
- Fix for CVE-2023-45288

* Wed Apr 17 2024 Bala <balakumaran.kannan@microsoft.com> - 1.11.1-6
- Patched vendored quic-go package to address CVE-2024-22189

* Sat Feb 10 2024 Mykhailo Bykhovtsev <mbykhovtsev@microsoft.com> - 1.11.1-5
- patched vendored quic-go package to address CVE-2023-49295

* Thu Feb 08 2024 Muhammad Falak <mwani@microsoft.com> - 1.11.1-4
- Bump release to rebuild with go 1.21.6

* Mon Feb 05 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.11.1-3
- Refactor vendor patch application
- Force vendored components during test

* Mon Jan 29 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.11.1-2
- Address CVE-2023-44487 by patching vendored golang.org/x/net

* Wed Oct 18 2023 Nicolas Guibourge <nicolasg@microsoft.com> - 1.11.1-1
- Upgrade to 1.11.1 to match version required by kubernetes

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-10
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.9.3-9
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-8
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-7
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-6
- Bump release to rebuild with go 1.19.10

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-5
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-4
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-3
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-2
- Bump release to rebuild with go 1.19.5

* Thu Jan 19 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.9.3-1
- Auto-upgrade to 1.9.3 - version required by Kubernetes

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.8.6-6
- Bump release to rebuild with go 1.19.4

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 1.8.6-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.6-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 1.8.6-3
- Bump release to rebuild against Go 1.18.5

* Tue Jun 14 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.6-2
- Bump release to rebuild with golang 1.18.3

* Fri Apr 22 2022 Nicolas Guibourge <nicolasg@microsoft.com> - 1.8.6-1
- Update to version  "1.8.6".
- Remove clean section
- License verified

* Tue Mar 15 2022 Muhammad Falak <mwani@microsoft.com> - 1.8.4-4
- Bump release to force rebuild with golang 1.16.15

* Fri Feb 18 2022 Thomas Crain <thcrain@microsoft.com> - 1.8.4-3
- Bump release to force rebuild with golang 1.16.14

* Wed Jan 19 2022 Henry Li <lihl@microsoft.com> - 1.8.4-2
- Increment release for force republishing using golang 1.16.12

* Tue Dec 28 2021 Nicolas Guibourge <nicolasg@microsoft.com> - 1.8.4-1
- Update to version  "1.8.4".

* Tue Nov 02 2021 Thomas Crain <thcrain@microsoft.com> - 1.8.0-2
- Increment release for force republishing using golang 1.16.9

* Fri Aug 20 2021 CBL-Mariner Service Account <cblmargh@microsoft.com> - 1.8.0-1
- Update to version  "1.8.0".

* Tue Jun 08 2021 Henry Beberman <henry.beberman@microsoft.com> 1.7.0-3
- Increment release to force republishing using golang 1.15.13.
* Mon Apr 26 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.7.0-2
- Increment release to force republishing using golang 1.15.11.
* Wed Jan 20 2021 Nicolas Guibourge <nicolasg@microsoft.com> 1.7.0-1
- Original version for CBL-Mariner.
