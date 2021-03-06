%global cartridgedir %{_libexecdir}/openshift/cartridges/python
%global httpdconfdir /etc/openshift/cart.conf.d/httpd/python

Name:          openshift-origin-cartridge-python
Version: 1.20.1
Release:       1%{?dist}
Summary:       Python cartridge
Group:         Development/Languages
License:       ASL 2.0
URL:           https://www.openshift.com
Source0:       http://mirror.openshift.com/pub/openshift-origin/source/%{name}/%{name}-%{version}.tar.gz
Requires:      facter
Requires:      rubygem(openshift-origin-node)
Requires:      openshift-origin-node-util
%if 0%{?fedora}%{?rhel} <= 6
Requires:      python >= 2.6
Requires:      python < 2.7
Requires:      scl-utils
BuildRequires: scl-utils-build
#FIXME: Use %scl_require macro to properly define dependencies
Requires:      python27
Requires:      mod_wsgi >= 3.2
Requires:      mod_wsgi < 3.4
Requires:      httpd < 2.4
%endif
%if 0%{?fedora} >= 19
Requires:      python >= 2.7
Requires:      python < 2.8
Requires:      mod_wsgi >= 3.4
Requires:      mod_wsgi < 3.5
Requires:      httpd > 2.3
Requires:      httpd < 2.5
%endif

Requires:      MySQL-python
Requires:      pymongo
Requires:      pymongo-gridfs
Requires:      python-psycopg2
Requires:      python-virtualenv
Requires:      python-magic
%if 0%{?fedora}%{?rhel} <= 6
Requires:      python27-MySQL-python
Requires:      python27-python-psycopg2
Requires:      python27-mod_wsgi
Requires:      python27-python-pip-virtualenv
Requires:      python27-numpy
Requires:      python33-python-virtualenv
Requires:      python33-mod_wsgi
Requires:      python33-python-pymongo
Requires:      python33-python-psycopg2
Requires:      python33-numpy
%endif
Requires:      libjpeg
Requires:      libjpeg-devel
Requires:      libcurl
Requires:      libcurl-devel
Requires:      numpy
Requires:      numpy-f2py
Requires:      gcc-gfortran
Requires:      freetype-devel
Requires:      atlas-devel
Requires:      lapack-devel
Requires:      redhat-lsb-core
Requires:      ta-lib-devel
Requires:      symlinks
Requires:      libffi-devel

Obsoletes: openshift-origin-cartridge-community-python-2.7
Obsoletes: openshift-origin-cartridge-community-python-3.3
Obsoletes: openshift-origin-cartridge-python-2.6

BuildArch:     noarch

%description
Python cartridge for OpenShift. (Cartridge Format V2)


%prep
%setup -q

%build
%__rm %{name}.spec

%install
%__mkdir -p %{buildroot}%{cartridgedir}
%__cp -r * %{buildroot}%{cartridgedir}
%__mkdir -p %{buildroot}%{httpdconfdir}

%__mkdir -p %{buildroot}%{cartridgedir}/env

%if 0%{?fedora}%{?rhel} <= 6
%__mv %{buildroot}%{cartridgedir}/metadata/manifest.yml.rhel %{buildroot}%{cartridgedir}/metadata/manifest.yml
%endif
%if 0%{?fedora} == 19
%__mv %{buildroot}%{cartridgedir}/metadata/manifest.yml.f19 %{buildroot}%{cartridgedir}/metadata/manifest.yml
%endif
%__rm -f %{buildroot}%{cartridgedir}/metadata/manifest.yml.*


%__mkdir -p %{buildroot}%{cartridgedir}/usr/versions/{2.6,2.7,3.3}
%if 0%{?fedora}%{?rhel} <= 6
%__cp -anv %{buildroot}%{cartridgedir}/usr/versions/2.7-scl/* %{buildroot}%{cartridgedir}/usr/versions/2.7/
%__cp -anv %{buildroot}%{cartridgedir}/usr/versions/3.3-scl/* %{buildroot}%{cartridgedir}/usr/versions/3.3/
%endif
%__cp -anv %{buildroot}%{cartridgedir}/usr/versions/shared/* %{buildroot}%{cartridgedir}/usr/versions/2.6/
%__cp -anv %{buildroot}%{cartridgedir}/usr/versions/shared/* %{buildroot}%{cartridgedir}/usr/versions/2.7/
%__cp -anv %{buildroot}%{cartridgedir}/usr/versions/shared/* %{buildroot}%{cartridgedir}/usr/versions/3.3/

%__rm -rf %{buildroot}%{cartridgedir}/usr/versions/shared
%__rm -rf %{buildroot}%{cartridgedir}/usr/versions/2.7-scl
%__rm -rf %{buildroot}%{cartridgedir}/usr/versions/3.3-scl

%files
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%dir %{httpdconfdir}
%attr(0755,-,-) %{httpdconfdir}
%if 0%{?fedora}%{?rhel} <= 6
%attr(0755,-,-) %{cartridgedir}/usr/versions/2.6/bin/
%attr(0755,-,-) %{cartridgedir}/usr/versions/2.6/bin/*
%endif
%attr(0755,-,-) %{cartridgedir}/usr/versions/2.7/bin/*
%attr(0755,-,-) %{cartridgedir}/usr/versions/3.3/bin/*
%{cartridgedir}
%doc %{cartridgedir}/README.md
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Thu Jan 30 2014 Adam Miller <admiller@redhat.com> 1.20.1-1
- Remove community tag from Python manifests (ironcladlou@gmail.com)
- bump_minor_versions for sprint 40 (admiller@redhat.com)

* Thu Jan 23 2014 Adam Miller <admiller@redhat.com> 1.19.8-1
- Bump up cartridge versions (bparees@redhat.com)

* Mon Jan 20 2014 Adam Miller <admiller@redhat.com> 1.19.7-1
- <perl,python,phpmyadmin carts> bug 1055095 (lmeyer@redhat.com)

* Fri Jan 17 2014 Adam Miller <admiller@redhat.com> 1.19.6-1
- Merge pull request #4502 from sosiouxme/custom-cart-confs
  (dmcphers+openshiftbot@redhat.com)
- <python cart> enable providing custom gear server confs (lmeyer@redhat.com)

* Fri Jan 17 2014 Adam Miller <admiller@redhat.com> 1.19.5-1
- Merge pull request #4462 from bparees/cart_data_cleanup
  (dmcphers+openshiftbot@redhat.com)
- remove unnecessary cart-data variable descriptions (bparees@redhat.com)

* Tue Jan 14 2014 Adam Miller <admiller@redhat.com> 1.19.4-1
- Merge pull request #4464 from ironcladlou/bz/1052103
  (dmcphers+openshiftbot@redhat.com)
- Bug 1052103: Fix template app.py for Python 3.3 (ironcladlou@gmail.com)

* Mon Jan 13 2014 Adam Miller <admiller@redhat.com> 1.19.3-1
- Merge pull request #4461 from ironcladlou/bz/1052059
  (dmcphers+openshiftbot@redhat.com)
- Bug 1052059: Fix Python 3.3 venv path references (ironcladlou@gmail.com)
- Bug 1051910: Fix Python 2.6 regressions (ironcladlou@gmail.com)
- Merge pull request #4444 from ironcladlou/dev/python-scl
  (dmcphers+openshiftbot@redhat.com)
- Fixing double-slash in python and posgresql cartridge code
  (jhadvig@redhat.com)
- Convert Python 3.3 community cart to use SCL Python 3.3
  (ironcladlou@gmail.com)