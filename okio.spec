%{?scl:%scl_package okio}
%{!?scl:%global pkg_name %{name}}
%{?java_common_find_provides_and_requires}

%global baserelease 2

Name:           %{?scl_prefix}okio
Version:        1.6.0
Release:        2.%{baserelease}%{?dist}
Summary:        Java I/O library
License:        ASL 2.0
URL:            http://square.github.io/%{pkg_name}/
BuildArch:      noarch

Source0:        https://github.com/square/%{pkg_name}/archive/%{pkg_name}-parent-%{version}.tar.gz

BuildRequires:  %{?scl_prefix_maven}maven-local
BuildRequires:  %{?scl_prefix_maven}mvn(org.apache.maven.plugins:maven-shade-plugin)
BuildRequires:  %{?scl_prefix_maven}mvn(org.sonatype.oss:oss-parent:pom:)

%description
Okio is a new library that complements java.io and java.nio to make it
much easier to access, store, and process data.

%package javadoc
Summary:        API documentation for %{pkg_name}

%description javadoc
this package provides %{summary}.

%prep
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%setup -q -n %{pkg_name}-%{pkg_name}-parent-%{version}

%pom_disable_module benchmarks

# Remove dependency on Animal Sniffer (not usable in Fedora)
%pom_remove_plugin :animal-sniffer-maven-plugin okio
%pom_remove_dep :animal-sniffer-annotations okio
sed -i /IgnoreJRERequirement/d okio/src/main/java/okio/{DeflaterSink,Okio}.java

# Skip one test which fails on ARM due to poor JVM performance.
sed -i /writeWithTimeout/s/./@org.junit.Ignore/ okio/src/test/java/okio/SocketTimeoutTest.java
%{?scl:EOF}


%build
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
# Tests require networking
%mvn_build -f
%{?scl:EOF}


%install
%{?scl:scl enable %{scl_maven} %{scl} - << "EOF"}
set -e -x
%mvn_install
%{?scl:EOF}


%files -f .mfiles
%doc README.md LICENSE.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt

%changelog
* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 1.6.0-2.2
- Don't build benchmarks

* Thu Jan 19 2017 Mat Booth <mat.booth@redhat.com> - 1.6.0-2.1
- Auto SCL-ise package for rh-eclipse46 collection

* Wed Jun 15 2016 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.6.0-2
- Add missing build-requires

* Tue Feb 16 2016 Gerard Ryan <galileo@fedoraproject.org> - 1.6.0-1
- Update to version 1.6.0 for okhttp-2.7.4

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Wed Mar 11 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2.0-1
- Update to upstream version 1.2.0

* Fri Sep 26 2014 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.0.1-1
- Initial packaging
