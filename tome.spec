# TODO:
#	- move tome.cfg to proper /etc directory
#	- fix putting scores into /var/games/tome
#
%define		file_version	%(echo %{version} | tr -d .)
%define		_alpha		alpha17
Summary:	Troubles of Middle Earth - a roguelike game
Summary(pl.UTF-8):	Gra roguelike "Troubles of Middle Earth"
Name:		tome
Version:	3.0.0
Release:	0.%{_alpha}.1
License:	distributable
Group:		Applications/Games
Source0:	http://t-o-m-e.net/dl/src/%{name}-%{file_version}%{_alpha}-src.tar.bz2
# Source0-md5:	9e33b9c4fe4c79319e9523b06ddbbd15
Source1:	%{name}.png
Source2:	%{name}.desktop
Patch0:		%{name}-makefile.patch
#to be fixed
#Patch1:		%{name}-paths.patch
URL:		http://www.t-o-m-e.net/
BuildRequires:	lua51-devel
BuildRequires:	ncurses-devel
Conflicts:	applnk < 1.5.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Troubles of Middle Earth (formerly PernAngband) is a complex roguelike
game based on the world created by JRR Tolkien. ToME is one of many
Angband variants.

%description -l pl.UTF-8
"Troubles of Middle Earth" (dawniej PernAngband) to rozbudowana gra
roguelike osadzona w świecie stworzonym przez JRR Tolkiena. ToME jest
jednym z wielu dostępnych wariantów Angbandu.

%prep
%setup -q -n %{name}-%{file_version}%{_alpha}-src
%patch0 -p1
#%%patch1 -p1

%build
# Only build ncurses version (see makefile patch), because I didn't
# manage to build any other working version
cd src
%{__make} -f makefile.std \
	COPTS="%{rpmcflags}" \
	CC="%{__cc}" \
	PREFIX="%{_prefix}" \
	TOMENAME="%{name}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/games/tome,%{_pixmapsdir},%{_desktopdir}}

install src/tome $RPM_BUILD_ROOT%{_bindir}/%{name}
install tome.cfg $RPM_BUILD_ROOT%{_datadir}/games/%{name}
cp -r game $RPM_BUILD_ROOT%{_datadir}/games/%{name}
# do not copy placeholders; bones are unnecessary
#cp -r lib/{apex,save,data} $RPM_BUILD_ROOT/var/games/tome

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.txt
%attr(755,root,root) %{_bindir}/%{name}
%{_datadir}/games/%{name}
#%%attr(775,root,games) /var/games/tome
%{_desktopdir}/tome.desktop
%{_pixmapsdir}/tome.png
