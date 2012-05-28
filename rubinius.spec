%global git     6ec606d

# Currently Rubinius binaries conflict with original MRI binaries.
# This prefix will be used to avoid conflicts
%global rbx_prefix rbx-

Name:		rubinius
Version:	2.0.0
Release:	2.%{git}git%{?dist}
Summary:	Implementation of the Ruby programming language

Group:		Development/Languages
License:	BSD
URL:		http://rubini.us
Source0:	https://nodeload.github.com/%{name}/rubinius/tarball/%{git}

Requires:	llvm
Requires:	ncurses
Requires:	openssl
Requires:	libyaml
BuildRequires:	gcc
BuildRequires:	make
BuildRequires:	ncurses
BuildRequires:	bison
BuildRequires:	ruby
BuildRequires:	llvm
BuildRequires:	libffi
BuildRequires:	libffi-devel
BuildRequires:	llvm-devel
BuildRequires:	ncurses-devel
BuildRequires:	zlib-devel
BuildRequires:	libyaml-devel
BuildRequires:	readline-devel
BuildRequires:	ruby-devel
BuildRequires:  openssl-devel
BuildRequires:  doxygen
BuildRequires:	rubygem(rake)

%description
Rubinius includes a bytecode virtual machine, parser, bytecode compiler,
garbage collector, and just-in-time (JIT) native machine code compiler. The
Ruby core library is written almost entirely in Ruby. Rubinius provides the
same standard libraries as Matz's Ruby implementation (MRI). Rubinius also
provides C-API compatibility for native C extensions.

%package doc
Summary: Documentation for %{name}
Group: Documentation
Requires:%{name} = %{version}-%{release}

%description doc
Documentation for %{name}

%package devel
Summary: Development files for %{name}
Group: Development
Requires:%{name} = %{version}-%{release}

%description devel
Development files for %{name}

%prep
%setup -q -n %{name}-%{name}-%{git}

%build
# FIXME: Rubinius threat warnings as errors. Is it safe to turn it off
CFLAGS="$CFLAGS -w" ./configure --without-vendor-zlib --default-version 19 \
	-B %{_bindir} \
	-L %{_libdir} \
	-M %{_mandir} \
	-G %{_libdir}/%{name}/gems \
	-I %{_includedir}/%{name} \
	--sitedir %{_libdir}/%{name}/sitelib \
	--vendordir %{_libdir}/%{name}/vendor

# Display the current configuration to stdout for debugging
./configure --show
# Build rubinius
rake build
rake doc:doxygen:generate

%check
# Execute compatibility tests
# rake spec18
# rake spec19

%install
rm -rf %{buildroot}

FAKEROOT=%{buildroot} rake install:files
# Fix shebang and wrong interpreter
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/bin/rdoc
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/bin/rake
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/bin/rake-compiler
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/bin/ri
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/bin/gem.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/abbrev.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/rubygems/digest/sha2.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/rubygems/digest/md5.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/rubygems/digest/sha1.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/set.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/19/set.rb 
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/tsort.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/irb/ext/save-history.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/irb/cmd/subirb.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/19/bigdecimal/sample/linear.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/bin/irb.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/bin/rar.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/generator.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/19/bigdecimal/sample/pi.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/bigdecimal/sample/pi.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/19/bigdecimal/sample/linear.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/bigdecimal/sample/linear.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/18/bigdecimal/sample/nlsolve.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/2.0/lib/19/bigdecimal/sample/nlsolve.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/ruby-debug-0.10.47/Rakefile
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/rake-0.9.2.2/bin/rake
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/rdoc-2.5.1/bin/ri
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/ffi-1.0.9/Rakefile
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/rake-compiler-0.7.9/lib/rake/javaextensiontask.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/rake-compiler-0.7.9/lib/rake/extensioncompiler.rb
sed -ie '1d' %{buildroot}/%{_libdir}/%{name}/gems/rubinius/preinstalled/gems/rake-compiler-0.7.9/lib/rake/baseextensiontask.rb

# Prefix all Rubinius binaries to avoid conflict with MRI
mv %{buildroot}/%{_bindir}/gem %{buildroot}/%{_bindir}/%{rbx_prefix}gem
mv %{buildroot}/%{_bindir}/ruby %{buildroot}/%{_bindir}/%{rbx_prefix}ruby
mv %{buildroot}/%{_bindir}/irb %{buildroot}/%{_bindir}/%{rbx_prefix}irb
mv %{buildroot}/%{_bindir}/rdoc %{buildroot}/%{_bindir}/%{rbx_prefix}rdoc
mv %{buildroot}/%{_bindir}/ri %{buildroot}/%{_bindir}/%{rbx_prefix}ri
mv %{buildroot}/%{_bindir}/testrb %{buildroot}/%{_bindir}/%{rbx_prefix}testrb
mv %{buildroot}/%{_bindir}/rake %{buildroot}/%{_bindir}/%{rbx_prefix}rake
# Install documentation files
mkdir -p %{buildroot}/%{_docdir}/%{name}
mv %{buildroot}/%{_libdir}/%{name}/2.0/lib/%{name}/documentation %{buildroot}/%{_docdir}/%{name}/
cp -rv doc/* %{buildroot}/%{_docdir}/%{name}/
cp -v README %{buildroot}/%{_docdir}/%{name}/
cp -v AUTHORS %{buildroot}/%{_docdir}/%{name}/
cp -v THANKS %{buildroot}/%{_docdir}/%{name}/
cp -v LICENSE %{buildroot}/%{_docdir}/%{name}/

%files
%defattr(-, root, root, -)
%{_bindir}/rbx
%{_bindir}/%{rbx_prefix}gem
%{_bindir}/%{rbx_prefix}ruby
%{_bindir}/%{rbx_prefix}irb
%{_bindir}/%{rbx_prefix}ri
%{_bindir}/%{rbx_prefix}rdoc
%{_bindir}/%{rbx_prefix}testrb
%{_bindir}/%{rbx_prefix}rake
%{_libdir}/%{name}

%files devel
%defattr(-, root, root, -)
%{_includedir}/%{name}

%files doc
%defattr(-, root, root, -)
%{_docdir}/%{name}

%changelog

* Thu Apr 6 2012 Michal Fojtik <mfojtik@redhat.com> 2.0.0-2.g29b8044git
- Fixed runtime dependencies
- Fixed build requires

* Thu Apr 5 2012 Michal Fojtik <mfojtik@redhat.com> 2.0.0-1.g29b8044git
- Initial RPM release
