%global debug_package %{nil}
%define upstream_name containerd-cc
%define upstream_repo confidential-containers-containerd
%define commit_hash e55e17bb9c75834c863d422bc38b54b0056e467a

Summary: Industry-standard container runtime for confidential containers
Name: moby-%{upstream_name}
Version: 1.7.7
Release: 11%{?dist}
License: ASL 2.0
Group: Tools/Container
URL: https://www.containerd.io
Vendor: Microsoft Corporation
Distribution: Mariner

Source0:  https://github.com/microsoft/confidential-containers-containerd/archive/refs/tags/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1: containerd.service
Source2: containerd.toml
Patch0: CVE-2023-47108.patch
Patch1: CVE-2023-44487.patch
Patch2: fix_cc_tests_for_golang1.21.patch
Patch4: CVE-2023-45288.patch
Patch5: CVE-2024-24786.patch
Patch6: CVE-2024-28180.patch
Patch7: CVE-2025-27144.patch
Patch8: CVE-2024-40635.patch

%{?systemd_requires}

BuildRequires: git
BuildRequires: golang
BuildRequires: go-md2man
BuildRequires: make
BuildRequires: systemd-rpm-macros

Requires: moby-runc >= 1.1.0

Conflicts: moby-containerd
Conflicts: moby-engine <= 3.0.10

Obsoletes: containerd
Obsoletes: containerd-io

%description
This is the containerd runtime meant for use with confidential containers

%prep
%autosetup -p1 -n %{upstream_repo}-%{version}

%build
export BUILDTAGS="-mod=vendor"
make VERSION="%{version}" REVISION="%{commit_hash}" binaries man

%check
export BUILDTAGS="-mod=vendor"
make VERSION="%{version}" REVISION="%{commit_hash}" test

%install
make VERSION="%{version}" REVISION="%{commit_hash}" DESTDIR="%{buildroot}" PREFIX="/usr" install install-man

mkdir -p %{buildroot}/%{_unitdir}
install -D -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}/containerd.service
install -D -p -m 0644 %{SOURCE2} %{buildroot}%{_sysconfdir}/containerd/config.toml

%post
%systemd_post containerd.service

if [ $1 -eq 1 ]; then # Package install
	systemctl enable containerd.service > /dev/null 2>&1 || :
	systemctl start containerd.service > /dev/null 2>&1 || :
fi

%preun
%systemd_preun containerd.service

%postun
%systemd_postun_with_restart containerd.service

%files
%license LICENSE NOTICE
%{_bindir}/*
%{_mandir}/*
%config(noreplace) %{_unitdir}/containerd.service
%config(noreplace) %{_sysconfdir}/containerd/config.toml

%changelog
* Wed Apr 16 2025 Manuel Huber <mahuber@microsoft.com> - 1.7.7-11
- Fix CVE-2024-40635

* Tue Apr 08 2025 Manuel Huber <mahuber@microsoft.com> - 1.7.7-10
- Fix CVE-2025-27144 with an upstream patch

* Thu Jan 30 2025 Kanishk Bansal <kanbansal@microsoft.com> - 1.7.7-9
- Fix CVE-2024-28180 with an upstream patch

* Thu Dec 05 2024 sthelkar <sthelkar@microsoft.com> - 1.7.7-8
- Patch CVE-2024-24786

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.7-7
- Bump release to rebuild with go 1.22.7

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 1.7.7-6
- Drop requirement on a specific version of golang

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.7-5
- Bump release to rebuild with go 1.21.11

* Thu Apr 18 2024 Chris Gunn <chrisgun@microsoft.com> - 1.7.7-4
- Fix for CVE-2023-45288

* Mon Apr 08 2024 Mitch Zhu <mitchzhu@microsoft.com> - 1.7.7-3
- Drop obsolete btrfs-progs-devel build dependency

* Wed Feb 21 2024 Henry Beberman <henry.beberman@microsoft.com> - 1.7.7-2
- Backport upstream patch for no-inlining seccomp and apparmor functions to fix tests.

* Tue Feb 20 2024 Mitch Zhu <mitchzhu@microsoft.com> - 1.7.7-1
- Upgrade to upstream containerd v1.7.7.

* Fri Feb 02 2024 Daniel McIlvaney <damcilva@microsoft.com> - 1.7.2-4
- Address CVE-2023-44487 by patching vendored golang.org/x/net

* Wed Dec 20 2023 Manuel Huber <mahuber@microsoft.com> - 1.7.2-3
- Set oom_score_adj of containerd to -999

* Wed Nov 23 2023 Bala <balakumaran.kannan@gmail.com> - 1.7.2-2
- Fix CVE-2023-47108 by backporting the fix made for otel-grpc-0.40.0

* Fri Nov 08 2023 Saul Paredes <saulparedes@microsoft.com> - 1.7.2-1
- Always add TargetLayerDigestLabel label to snapshots

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.1-6
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 1.7.1-5
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.1-4
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.1-3
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 1.7.1-2
- Bump release to rebuild with go 1.19.10

* Mon May 22 2023 Dallas Delaney <dadelan@microsoft.com> - 1.7.1-1
- Fix unit test arguments for TestSnapshotterFromPodSandboxConfig

* Wed May 17 2023 Dallas Delaney <dadelan@microsoft.com> - 1.7.0-2
- Add build version dependency on golang

* Tue Apr 25 2023 Dallas Delaney <dadelan@microsoft.com> - 1.7.0-1
- Add initial spec
- License verified.
- Original version for CBL-Mariner
