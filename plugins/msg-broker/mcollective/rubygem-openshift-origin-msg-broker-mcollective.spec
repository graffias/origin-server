%if 0%{?fedora}%{?rhel} <= 6
    %global scl ruby193
    %global scl_prefix ruby193-
    %global scl_root /opt/rh/ruby193/root
%endif
%{!?scl:%global pkg_name %{name}}
%{?scl:%scl_package rubygem-%{gem_name}}
%global gem_name openshift-origin-msg-broker-mcollective
%global rubyabi 1.9.1

Summary:       OpenShift plugin for mcollective service
Name:          rubygem-%{gem_name}
Version: 1.20.1
Release:       1%{?dist}
Group:         Development/Languages
License:       ASL 2.0
URL:           http://www.openshift.com
Source0:       http://mirror.openshift.com/pub/openshift-origin/source/%{name}/rubygem-%{gem_name}-%{version}.tar.gz
%if 0%{?fedora} >= 19
Requires:      ruby(release)
%else
Requires:      %{?scl:%scl_prefix}ruby(abi) >= %{rubyabi}
%endif
Requires:      %{?scl:%scl_prefix}rubygems
Requires:      %{?scl:%scl_prefix}rubygem(json)
Requires:      rubygem(openshift-origin-common)
Requires:      %{?scl:%scl_prefix}mcollective-client
Requires:      selinux-policy-targeted
Requires:      policycoreutils-python
Requires:      openshift-origin-msg-common
%if 0%{?fedora}%{?rhel} <= 6
BuildRequires: %{?scl:%scl_prefix}build
BuildRequires: scl-utils-build
%endif
%if 0%{?fedora} >= 19
BuildRequires: ruby(release)
%else
BuildRequires: %{?scl:%scl_prefix}ruby(abi) >= %{rubyabi}
%endif
BuildRequires: %{?scl:%scl_prefix}rubygems
BuildRequires: %{?scl:%scl_prefix}rubygems-devel
BuildArch:     noarch

%description
OpenShift plugin for mcollective based node/gear manager

%prep
%setup -q

%build
%{?scl:scl enable %scl - << \EOF}
mkdir -p .%{gem_dir}
# Build and install into the rubygem structure
gem build %{gem_name}.gemspec
gem install -V \
        --local \
        --install-dir ./%{gem_dir} \
        --bindir ./%{_bindir} \
        --force %{gem_name}-%{version}.gem
%{?scl:EOF}

%install
mkdir -p %{buildroot}%{gem_dir}

cp -a ./%{gem_dir}/* %{buildroot}%{gem_dir}/

mkdir -p %{buildroot}/etc/openshift/plugins.d
cp %{buildroot}/%{gem_dir}/gems/%{gem_name}-%{version}/conf/openshift-origin-msg-broker-mcollective.conf.example %{buildroot}/etc/openshift/plugins.d/openshift-origin-msg-broker-mcollective.conf.example

%if 0%{?rhel} <= 6
sed -i -e "s|\(/etc/mcollective/client.cfg\)|%{scl_root}/\1|" %{buildroot}/etc/openshift/plugins.d/openshift-origin-msg-broker-mcollective.conf.example
%endif

%files
%dir %{gem_instdir}
%dir %{gem_dir}
%doc Gemfile LICENSE
%{gem_dir}/doc/%{gem_name}-%{version}
%{gem_dir}/gems/%{gem_name}-%{version}
%{gem_dir}/cache/%{gem_name}-%{version}.gem
%{gem_dir}/specifications/%{gem_name}-%{version}.gemspec
/etc/openshift/plugins.d/openshift-origin-msg-broker-mcollective.conf.example

%defattr(-,root,apache,-)
%attr(0644,-,-) %ghost %{?scl:%scl_root}/etc/mcollective/client.cfg

%changelog
* Thu Jan 30 2014 Adam Miller <admiller@redhat.com> 1.20.1-1
- Card #185: sending app alias to all web_proxy gears (abhgupta@redhat.com)
- Allow gemspecs to be parsed on non RPM systems (like the rest of cartridges)
  (ccoleman@redhat.com)
- bump_minor_versions for sprint 40 (admiller@redhat.com)

* Thu Jan 23 2014 Adam Miller <admiller@redhat.com> 1.19.12-1
- Merge pull request #4568 from danmcp/bug1049044
  (dmcphers+openshiftbot@redhat.com)
- Bug 1049044: Creating a single sshkey for each scalable application
  (abhgupta@redhat.com)
- Bug 1055371 (dmcphers@redhat.com)

* Wed Jan 22 2014 Adam Miller <admiller@redhat.com> 1.19.11-1
- Merge pull request #4551 from pravisankar/dev/ravi/bug1049626
  (dmcphers+openshiftbot@redhat.com)
- Bug 1049626 - Only allow gear move between districted nodes Rationale:
  districted to non-districted nodes not allowed: gear uids on non-districted
  nodes may not be in the range of uids supported by the district between non-
  districted nodes not allowed:: gear uids are not set in mongo and we can not
  guarantee same uid for both source and destination (rpenta@redhat.com)
- Bug 1055878: calling tidy once per gear instead of per gear per cart
  (abhgupta@redhat.com)

* Tue Jan 21 2014 Adam Miller <admiller@redhat.com> 1.19.10-1
- Merge pull request #4531 from abhgupta/abhgupta-dev
  (dmcphers+openshiftbot@redhat.com)
- Bug 1040113: Handling edge cases in cleaning up downloaded cart map Also,
  fixing a couple of minor issues (abhgupta@redhat.com)
- Bug 1049626 - Allow move gear with districts, with-out districts, across
  districted nodes to non-districted nodes and vice versa. (rpenta@redhat.com)

* Mon Jan 20 2014 Adam Miller <admiller@redhat.com> 1.19.9-1
- Typo fix: Method name find_available_impl changed to find_all_available_impl
  (rpenta@redhat.com)

* Fri Jan 17 2014 Adam Miller <admiller@redhat.com> 1.19.8-1
- Merge pull request #4497 from danmcp/master
  (dmcphers+openshiftbot@redhat.com)
- cleanup (dmcphers@redhat.com)
- Allow multiple keys to added or removed at the same time (lnader@redhat.com)

* Thu Jan 16 2014 Adam Miller <admiller@redhat.com> 1.19.7-1
- Separating out node selection algorithm (abhgupta@redhat.com)

* Tue Jan 14 2014 Adam Miller <admiller@redhat.com> 1.19.6-1
- Bug 1052928 - plugin: make the exception clear in case of a conflicting uuid
  during a move (mmahut@redhat.com)

* Mon Jan 13 2014 Adam Miller <admiller@redhat.com> 1.19.5-1
- Use mongoid 'save\!' instead of 'save' to raise an exception in case of
  failures (rpenta@redhat.com)

* Thu Jan 09 2014 Troy Dawson <tdawson@redhat.com> 1.19.4-1
- Merge pull request #4414 from abhgupta/abhgupta-scheduler
  (dmcphers+openshiftbot@redhat.com)
- Fix for bug 1046091 (abhgupta@redhat.com)
- Fix for bug 1047957 (abhgupta@redhat.com)