# RHEL has 0.6 and 0.10. but 0.10 has a prefix for SCL
# Fedora 18 and 19 has 0.10 as the default
%if 0%{?fedora}%{?rhel} <= 6
  %global scl nodejs010
  %global scl_prefix nodejs010-
%endif

%global cartridgedir %{_libexecdir}/openshift/cartridges/nodejs

Summary:       Provides Node.js support
Name:          openshift-origin-cartridge-nodejs
Version: 1.21.1
Release:       1%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://www.openshift.com
Source0:       http://mirror.openshift.com/pub/openshift-origin/source/%{name}/%{name}-%{version}.tar.gz

Requires:      facter
Requires:      rubygem(openshift-origin-node)
Requires:      openshift-origin-node-util

%if 0%{?fedora}%{?rhel} <= 6
Requires:      %{scl}
%endif

Requires:      %{?scl:%scl_prefix}npm
Requires:      %{?scl:%scl_prefix}nodejs-pg
Requires:      %{?scl:%scl_prefix}nodejs-options
Requires:      %{?scl:%scl_prefix}nodejs-supervisor
Requires:      %{?scl:%scl_prefix}nodejs-async

Requires:      %{?scl:%scl_prefix}nodejs-express
Requires:      %{?scl:%scl_prefix}nodejs-connect
Requires:      %{?scl:%scl_prefix}nodejs-mongodb
Requires:      %{?scl:%scl_prefix}nodejs-mysql
Requires:      %{?scl:%scl_prefix}nodejs-node-static

Requires:      nodejs
Requires:      nodejs-async
Requires:      nodejs-connect
Requires:      nodejs-express
Requires:      nodejs-mongodb
Requires:      nodejs-mysql
Requires:      nodejs-node-static
Requires:      nodejs-pg
Requires:      nodejs-supervisor
Requires:      nodejs-options

Obsoletes: openshift-origin-cartridge-nodejs-0.6

BuildArch:     noarch

%description
Provides Node.js support to OpenShift. (Cartridge Format V2)

%prep
%setup -q

%build
%__rm %{name}.spec

%install
%__mkdir -p %{buildroot}%{cartridgedir}
%__cp -r * %{buildroot}%{cartridgedir}

%if 0%{?rhel}
%__mv %{buildroot}%{cartridgedir}/metadata/manifest.yml.rhel %{buildroot}%{cartridgedir}/metadata/manifest.yml
%__mv %{buildroot}%{cartridgedir}/lib/nodejs_context.rhel %{buildroot}%{cartridgedir}/lib/nodejs_context
%endif
%if 0%{?fedora}
%__rm -f %{buildroot}%{cartridgedir}/versions/0.6
%__mv %{buildroot}%{cartridgedir}/metadata/manifest.yml.fedora %{buildroot}%{cartridgedir}/metadata/manifest.yml
%__mv %{buildroot}%{cartridgedir}/lib/nodejs_context.fedora %{buildroot}%{cartridgedir}/lib/nodejs_context
%endif
%__rm -f %{buildroot}%{cartridgedir}/lib/nodejs_context.*
%__rm -f %{buildroot}%{cartridgedir}/metadata/manifest.yml.*

%files
%dir %{cartridgedir}
%attr(0755,-,-) %{cartridgedir}/bin/
%{cartridgedir}
%doc %{cartridgedir}/README.md
%doc %{cartridgedir}/COPYRIGHT
%doc %{cartridgedir}/LICENSE

%changelog
* Thu Jan 30 2014 Adam Miller <admiller@redhat.com> 1.21.1-1
- Bug 1059374 - Sanity check pkill in nodejs control script
  (mfojtik@redhat.com)
- Bug 1059144 - Refactored nodejs control script (mfojtik@redhat.com)
- Merge pull request #4593 from mfojtik/card/89
  (dmcphers+openshiftbot@redhat.com)
- Card origin_cartridge_89 - Make npm optional and restrict hot_deploy to
  supervisor only (mfojtik@redhat.com)
- bump_minor_versions for sprint 40 (admiller@redhat.com)

* Thu Jan 23 2014 Adam Miller <admiller@redhat.com> 1.20.6-1
- Bump up cartridge versions (bparees@redhat.com)

* Fri Jan 17 2014 Adam Miller <admiller@redhat.com> 1.20.5-1
- Merge pull request #4462 from bparees/cart_data_cleanup
  (dmcphers+openshiftbot@redhat.com)
- remove unnecessary cart-data variable descriptions (bparees@redhat.com)

* Thu Jan 16 2014 Adam Miller <admiller@redhat.com> 1.20.4-1
- Bug 1048756 - 503 Service Temporarily Unavailable met when accessing after
  deploying pacman for nodejs-0.6/0.10 app (bparees@redhat.com)

* Thu Jan 09 2014 Troy Dawson <tdawson@redhat.com> 1.20.3-1
- Bug 1033581 - Adding upgrade logic to remove the unneeded
  jenkins_shell_command files (bleanhar@redhat.com)