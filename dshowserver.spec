# Conditional build:
%bcond_with	static	# static package for use with x86_64 systems
#

%define		svn			101
%define		rel			0.1
Summary:	Win32 CoreAVC H.264 codec helper
Summary(pl.UTF-8):	Serwer windowsowego kodeka CoreAVC H.264.
Name:		dshowserver
Version:	0.1
Release:	0.%{svn}.%{rel}
License:	GPL
Group:		X11/Applications/Multimedia
Source0:	%{name}-0.svn%{svn}.tar.bz2
# Source0-md5:	9fa17ea92a3d78c34f251a4c56bbd750
Patch0:		%{name}-codecspath.patch
Patch1:		%{name}-optflags.patch
URL:		http://code.google.com/p/coreavc-for-linux/
%ifarch %{x8664}
BuildRequires:	gcc-multilib
%{?with_static:BuildRequires:     glibc-static(i686)}
%else
%{?with_static:BuildRequires:     glibc-static}
%endif
BuildRequires:	rpmbuild(macros) >= 1.453
BuildRequires:	sed >= 4.0
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		x8664_flags	-m32
%define		specflags_x86_64 %{x8664_flags}
%define		specflags_amd64	%{x8664_flags}
%define		specflags_ia32e	%{x8664_flags}

%description
CoreAVC is a proprietary Windows codec for H.264 video decoding. It is
much faster than any currently available open-source codecs. Being
multi-threaded, and able to play PAFF streams, it can handle HD
H.264/AVC streams that no freely available codecs can. CoreAVC is
reasonably priced, but it is Windows only. Dshowserver serves CoreAVC
for mythtv, mplayer and xine. Dshowserver can work under 32 or 64 bits
linux system. For 64 bits use static binary compiled in 32 bits
environement.

%description -l pl.UTF-8
CoreAVC to komercyjny kodek H.264 dla systemu Windows. Jest znacznie
szybszy od dowolnego wolnego kodeka. Obsługujac wielowatkowosc moze
odtwarzac strumienie zakodowane z uzyciem interlacingu PAFF. Odtwarza
strumienie HD H.264/AVC. Kosztuje rozsadnie, ale dostepny jest tylko
dla Windows. Dhowserevr implementuje obsluge tego kodeka przez mythtv,
mplayer i xine. Dshowserver moze byc uzyty w architekturach x86 i
x86_64. Jezeli twoj system jest 64 bitowy. Uzyj statycznych binariow
zbudowanych w 32 bitowym srodowisku.

%package -n registercodec
Summary:	Utility to register win32 CoreAVC H.264 codec
Summary(pl.UTF-8):	Narzedzie do rejestracji windowsowego kodeka CoreAVC H.264.
Group:		X11/Applications/Multimedia

%description -n registercodec
Utility to register win32 CoreAVC H.264 codec for usage with
mythtv/mplayer/xine.

%description -n registercodec -l pl.UTF-8
Narzedzie do przeprowadzenia rejestracji komercyjnego kodeka CoreAVC
H.264.

%prep
%setup -q -n %{name}-svn%{svn}
%patch0 -p1
%patch1 -p1

%if "%{cc_version}" < "3.4"
# CC version is arbitary (just to be > 3.3)
%{__sed} -i -e 's/-Wno-pointer-sign//;s/-Wdeclaration-after-statement//' {loader,dshowserver}/Makefile
%endif

%build
cat << 'EOF' > config.mak
override CC = %{__cc}
override OPTFLAGS = %{rpmcflags}
override LDFLAGS = %{rpmldflags}

%{?with_static:STATIC = 1}

AR = ar
RANLIB = ranlib
OBJDIR = ../objs
EOF

%{__make} -C dshowserver

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir}/man1}
install dshowserver/dshowserver $RPM_BUILD_ROOT%{_bindir}/dshowserver
install dshowserver/registercodec $RPM_BUILD_ROOT%{_bindir}/registercodec
cp -a man/* $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,video) %{_bindir}/dshowserver
%{_mandir}/man1/ds*

%files -n registercodec
%defattr(644,root,root,755)
%attr(755,root,video) %{_bindir}/registercodec
%{_mandir}/man1/re*
