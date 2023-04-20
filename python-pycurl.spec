# PycURL checks that the actual libcurl version is not lower
# than the one used when PycURL was built during its initialization.
%global libcurl_sed '/^#define LIBCURL_VERSION "/!d;s/"[^"]*$//;s/.*"//;q'
%global curlver_h /usr/include/curl/curlver.h
%global libcurl_ver %(sed %{libcurl_sed} %{curlver_h} 2>/dev/null || echo 0)
%global srcname pycurl

Name:           python-%{srcname}
Version:        7.45.2
Release:        2
Summary:        A Python interface to libcurl
License:        LGPL-2.0+ or MIT
URL:            http://pycurl.sourceforge.net/
Source0:        %{pypi_source}
Patch0:         python-pycurl-fix-cc.patch
# drop link-time vs. run-time TLS backend check (#1446850)

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
BuildRequires:  python3-devel python3-bottle python3-pyflakes python3-pytest
Requires:       libcurl >= %{libcurl_ver}

%description -n python3-pycurl
PycURL is a Python interface to libcurl. PycURL can be used to fetch
objects identified by a URL from a Python program, similar to the
urllib Python module. PycURL is mature, very fast, and supports a lot
of features.
This package is for Python3.

%prep
%autosetup -n pycurl-%{version} -p1
rm -f winbuild.py
sed -e 's| winbuild.py||' -i Makefile
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

%check
# relax crypto policy for the test-suite to make it pass again (#1863711)
export OPENSSL_SYSTEM_CIPHERS_OVERRIDE=XXX
export OPENSSL_CONF=

export PYTHONPATH=%{buildroot}%{python3_sitearch}
export PYCURL_SSL_LIBRARY=openssl
export PYCURL_VSFTPD_PATH=vsftpd
export PYTEST_ADDOPTS="--ignore examples -m 'not online'"
make test PYTHON=%{__python3} NOSETESTS="nosetests-%{python3_version} -v" PYFLAKES=true
rm -fv tests/fake-curl/libcurl/*.so

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
* Mon Apr 17 2023 Xiaoya Huang <huangxiaoya@iscas.ac.cn> - 7.45.2-2
- Fix CC compiler support

* Thu Jan 19 2023 chendonghui6 <chendonghui6@huawei.com> - 7.45.2-1
- update version to 7.45.2

* Fri Aug 05 2022 yanglongkang <yanglongkang@h-partners.com> - 7.44.1-2
- Add release for rebuild

* Wed Dec 29 2021 guozhaorui <guozhaorui1@huawei.com> - 7.44.1-1
- update version to 7.44.1

* Sat Jul 24 2021 shixuantong <shixuantong@huawei.com> - 7.43.0.6-2
- fix test fail for test_sslversion_options, test_failonerror and test_failonerror_status_line_invalid_utf8_python3

* Tue Feb 2 2021 shangyibin <shangyibin1@huawei.com> - 7.43.0.6-1
- Upgrade to version 7.43.0.6

* Mon Nov 9 2020 wangjie<wangjie294@huawei.com> -7.43.0.5-2
- Type:bugfix
- ID:NA
- SUG:NA
- DESC:fix compile error

* Tue Aug 4 2020 shixuantong <shixuantong@huawei.com> - 7.43.0.5-1
- update to 7.43.0.5

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
