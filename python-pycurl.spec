# PycURL checks that the actual libcurl version is not lower
# than the one used when PycURL was built during its initialization.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)

Name:           python-pycurl
Version:        7.43.0.3
Release:        2
Summary:        A Python interface to libcurl
License:        LGPLv2+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        https://dl.bintray.com/pycurl/pycurl/pycurl-%{version}.tar.gz
# drop link-time vs. run-time TLS backend check (#1446850)
Patch0:         0002-python-pycurl-7.43.0-tls-backend.patch

BuildRequires:  gcc libcurl-devel openssl-devel vsftpd

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains development files for %{name}

%package_help

%package -n python3-pycurl
Summary:        Python interface to libcurl for Python 3
%{?python_provide:%python_provide python3-pycurl}
BuildRequires:  python3-devel python3-bottle python3-pyflakes
Requires:       libcurl >= %{libcurl_ver}

%description -n python3-pycurl
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.
This package is for Python3.

%prep
%autosetup -n pycurl-%{version} -p1

# remove binaries packaged by upstream
rm -f tests/fake-curl/libcurl/*.so
# remove a failed test-case that relies on sftp://web.sourceforge.net being available
rm -f tests/ssh_key_cb_test.py
# remove a failed test-case
rm -f tests/seek_cb_test.py
# remove tests depending on the 'flaky' nose plug-in
grep '^import flaky' -r tests | cut -d: -f1 | xargs rm -fv
# drop options that are not supported
sed -e 's/ --show-skipped//' \
    -e 's/ --with-flaky//' \
    -i tests/run.sh

%build
%py3_build -- --with-openssl

%install
export PYCURL_SSL_LIBRARY=openssl
%py3_install
rm -rf %{buildroot}%{_datadir}/doc/pycurl

%files devel
%defattr(-,root,root)
%doc examples tests

%files help
%defattr(-,root,root)
%doc ChangeLog README.rst doc

%files -n python3-pycurl
%defattr(-,root,root)
%license COPYING-LGPL COPYING-MIT
%{python3_sitearch}/curl/
%{python3_sitearch}/pycurl.*.so
%{python3_sitearch}/pycurl-%{version}-*.egg-info

%changelog
* Wed Jan 26 2022 zhangy1317<zhangy1317@chinaunicom.cn> - 7.43.0.3-2
- Remove python2

* Mon Aug 10 2020 shixuantong <shixuantong@huawei.com> - 7.43.0.3-1
- update to 7.43.0.3

* Fri Oct 25 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.43.0.2-6
- optimize spec file.

* Fri Sep 27 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.43.0.2-5
- del unnecessary statement

* Tue Sep 24 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.43.0.2-4
- add with_python2 for python2

* Thu Sep 19 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.43.0.2-3
- rebuild package

* Mon Sep 16 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.43.0.2-2
- modify content format

* Sat Sep 14 2019 openEuler Buildteam <buildteam@openeuler.org> - 7.43.0.2-1
- Package init
