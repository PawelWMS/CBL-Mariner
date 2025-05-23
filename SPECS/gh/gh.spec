Summary:        GitHub official command line tool
Name:           gh
Version:        2.13.0
Release:        24%{?dist}
License:        MIT
Vendor:         Microsoft Corporation
Distribution:   Mariner
Group:          Applications/Tools
URL:            https://github.com/cli/cli
Source0:        https://github.com/cli/cli/archive/refs/tags/v%{version}.tar.gz#/cli-%{version}.tar.gz
# Below is a manually created tarball, no download link.
# We're using pre-populated Go modules from this tarball, since network is disabled during build time.
# How to re-build this file:
#   1. wget https://github.com/cli/cli/archive/refs/tags/v%{version}.tar.gz -O cli-%%{version}.tar.gz
#   2. tar -xf cli-%%{version}.tar.gz
#   3. cd cli-%%{version}
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
# Available upstream in 2.16.0
Patch0:         fix-relative-time-search-tests.patch
Patch1:         CVE-2021-43565.patch
Patch2:         CVE-2022-32149.patch
Patch3:         CVE-2024-54132.patch
Patch4:         CVE-2024-45338.patch

BuildRequires:  golang
BuildRequires:  git
Requires:       git
%global debug_package %{nil}
%define our_gopath %{_topdir}/.gopath

%description
GitHub official command line tool.

%prep
%setup -q -n cli-%{version}
tar --no-same-owner -xf %{SOURCE1}
%autopatch -p1

%build
export GOPATH=%{our_gopath}
# No mod download use vednor cache locally
export GOFLAGS="-buildmode=pie -trimpath -mod=vendor -modcacherw -ldflags=-linkmode=external"
make GH_VERSION="v%{version}" bin/gh manpages

%install
./bin/gh completion -s bash | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/bash-completion/completions/gh
./bin/gh completion -s fish | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/fish/vendor_completions.d/gh.fish
./bin/gh completion -s zsh | install -Dm644 /dev/stdin %{buildroot}%{_datadir}/zsh/site-functions/_gh

install -Dm755 bin/gh %{buildroot}%{_bindir}/gh
install -d %{buildroot}%{_mandir}/man1/
cp share/man/man1/* %{buildroot}%{_mandir}/man1

%check
make test

%files
%defattr(-,root,root)
%license LICENSE
%doc README.md
%{_bindir}/gh
%{_mandir}/man1/*
%{_datadir}/bash-completion/completions/gh
%{_datadir}/fish/vendor_completions.d/gh.fish
%{_datadir}/zsh/site-functions/_gh

%changelog
* Fri Jan 03 2025 Sumedh Sharma <sumsharma@microsoft.com> - 2.13.0-24
- Add patch for CVE-2024-45338.

* Fri Dec 13 2024 Sandeep Karambelkar <skarambelkar@microsoft.com> - 2.13.0-23
- Patch CVE-2024-54132

* Thu Sep 19 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 2.13.0-22
- Patch CVE-2022-32149

* Mon Sep 09 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-21
- Bump release to rebuild with go 1.22.7

* Wed Jul 17 2024 Muhammad Falak R Wani <mwani@microsoft.com> - 2.13.0-20
- Drop requirement on a specific version of golang

* Fri Jul 19 2024 Archana Choudhary <archana1@microsoft.com> - 2.13.0-19
- Patch for CVE-2021-43565

* Thu Jun 06 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-18
- Bump release to rebuild with go 1.21.11

* Fri Feb 02 2024 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-17
- Bump release to rebuild with go 1.21.6

* Mon Oct 16 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-16
- Bump release to rebuild with go 1.20.9

* Tue Oct 10 2023 Dan Streetman <ddstreet@ieee.org> - 2.13.0-15
- Bump release to rebuild with updated version of Go.

* Mon Aug 07 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-14
- Bump release to rebuild with go 1.19.12

* Thu Jul 13 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-13
- Bump release to rebuild with go 1.19.11

* Thu Jun 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-12
- Bump release to rebuild with go 1.19.10

* Wed Apr 26 2023 Olivia Crain <oliviacrain@microsoft.com> - 2.13.0-11
- Add upstream patch to fix search tests involving relative time

* Wed Apr 05 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-10
- Bump release to rebuild with go 1.19.8

* Tue Mar 28 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-9
- Bump release to rebuild with go 1.19.7

* Wed Mar 15 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-8
- Bump release to rebuild with go 1.19.6

* Fri Feb 03 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-7
- Bump release to rebuild with go 1.19.5

* Wed Jan 18 2023 CBL-Mariner Servicing Account <cblmargh@microsoft.com> - 2.13.0-6
- Clean up dependencies (remove fish, bash-completion and zsh and add git)

* Fri Dec 16 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.13.0-5
- Bump release to rebuild with go 1.18.8 with patch for CVE-2022-41717

* Tue Nov 01 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.13.0-4
- Bump release to rebuild with go 1.18.8

* Mon Aug 22 2022 Olivia Crain <oliviacrain@microsoft.com> - 2.13.0-3
- Bump release to rebuild against Go 1.18.5

* Mon Jul 05 2022 Daniel McIlvaney <damcilva@microsoft.com> - 2.13.0-2
- Bump release due to bump in fish to 3.5.0.

* Thu Jun 30 2022 Suresh Babu Chalamalasetty <schalam@microsoft.com> - 2.13.0-1
- Original version for CBL-Mariner.
- License verified.
