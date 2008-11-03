
# Conditional build:
%bcond_with	static	# static package for use with x86_64 systems

%define		pname		dshowserver
%define 	_snap		svn
%define		_rel		82

Summary:	Win32 CoreAVC H.264 codec helper.
Summary(pl.UTF-8):	Serwer windowsowego kodeka CoreAVC H.264.
Name:		%{pname}%{?with_static:-static}
Version:	%{_snap}%{_rel}
Release:	0.1
License:	GPL
Group:		X11/Multimedia
Source0:	%{pname}-%{version}.tar.bz2
# Source0-md5:
Patch0:		%{pname}-codecspath.patch
URL:		http://code.google.com/		
BuildRequires:	glibc-static

%description
CoreAVC is a proprietary Windows codec for H.264 video decoding. 
It is much faster than any currently available open-source codecs. 
Being multi-threaded, and able to play PAFF streams, 
it can handle HD H.264/AVC streams that no freely available codecs can. 
CoreAVC is reasonably priced, but it is Windows only. 
Dshowserver serves CoreAVC for mythtv, mplayer and xine.
Dshowserver can work under 32 or 64 bits linux system.
For 64 bits use static binary compiled in 32 bits environement.

%description -l pl.UTF-8
CoreAVC to komercyjny kodek H.264 dla systemu Windows. Jest znacznie szybszy
od dowolnego wolnego kodeka. Obsługujac wielowatkowosc moze odtwarzac
strumienie zakodowane z uzyciem interlacingu PAFF.
Odtwarza strumienie HD H.264/AVC.
Kosztuje rozsadnie, ale dostepny jest tylko dla Windows.
Dhowserevr implementuje obsluge tego kodeka przez mythtv, mplayer i xine.
Dshowserver moze byc uzyty w architekturach x86 i x86_64.
Jezeli twoj system jest 64 bitowy. Uzyj statycznych binariow 
zbudowanych w 32 bitowym srodowisku.


%package -n registercodec%{?with_static:-static}
Summary:        Utility to register win32 CoreAVC H.264 codec.
Summary(pl.UTF-8):      Narzedzie do rejestracji windowsowego kodeka CoreAVC H.264.
Group:          X11/Multimedia

%description -n registercodec%{?with_static:-static}
Utility to register win32 CoreAVC H.264 codec for usage with mythtv/mplayer/xine.

%description -l pl.UTF-8 -n registercodec%{?with_static:-static}
Narzedzie do przeprowadzenia rejestracji komercyjnego  kodeka CoreAVC H.264.

%prep
cd %{_builddir}
rm -rf %{pname}-%{version}
tar jxvf %{SOURCE0}
cd %{pname}-%{version}

%patch0 -p1

%build
cd %{pname}-%{version}
make -C dshowserver %{?with_static:STATIC=1} 

%install
rm -rf $RPM_BUILD_ROOT
cd %{pname}-%{version}

install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1

install dshowserver/dshowserver $RPM_BUILD_ROOT%{_bindir}/dshowserver
install dshowserver/registercodec $RPM_BUILD_ROOT%{_bindir}/registercodec

install man/* $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%files
%attr(755,root,video) %{_bindir}/dshowserver
%attr(644,root,root) %{_mandir}/man1/ds*

%files -n registercodec%{?with_static:-static}
%attr(755,root,video) %{_bindir}/registercodec
%attr(644,root,root) %{_mandir}/man1/re*
