%define		file_version	%(echo %{version} | tr -d .)
Summary:	Troubles of Middle Earth - a roguelike game
Summary(pl):	Gra roguelike "Troubles of Middle Earth"
Name:		tome
Version:	2.2.5
Release:	3
License:	distributable
Group:		Applications/Games
Source0:	http://t-o-m-e.net/dl/src/%{name}-%{file_version}-src.tgz
# Source0-md5:	b1a340a6092fd53b07be9d107b16e16b
Source1:	%{name}.png
Source2:	%{name}.desktop
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-paths.patch
URL:		http://www.t-o-m-e.net/
BuildRequires:	ncurses-devel
Conflicts:	applnk < 1.5.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Troubles of Middle Earth (formerly PernAngband) is a complex roguelike
game based on the world created by JRR Tolkien. ToME is one of many
Angband variants.

%description -l pl
"Troubles of Middle Earth" (dawniej PernAngband) to rozbudowana gra
roguelike osadzona w ¶wiecie stworzonym przez JRR Tolkiena. ToME jest
jednym z wielu dostêpnych wariantów Angbandu.

%prep
%setup -q -n %{name}-%{file_version}-src
%patch0 -p1
%patch1 -p1

%build
# Only build ncurses version (see makefile patch), because I didn't
# manage to build any other working version
cd src
%{__make} -f makefile.std \
	COPTS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir}/games/tome/{cmov,dngn,edit,file,help,info,note,pref,scpt,user,mods},/var/games/tome/{apex,save,data,bone},%{_pixmapsdir},%{_desktopdir}}

install -D src/tome $RPM_BUILD_ROOT%{_bindir}/%{name}
cp -r lib/{cmov,core,dngn,edit,file,help,info,note,pref,scpt,user,mods,module.lua} $RPM_BUILD_ROOT%{_datadir}/games/tome
# do not copy placeholders; bones are unnecessary
#cp -r lib/{apex,save,data} $RPM_BUILD_ROOT/var/games/tome

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_desktopdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README *.txt
%attr(2755,root,games) %{_bindir}/%{name}
%{_datadir}/games/tome
%attr(775,root,games) /var/games/tome
%{_pixmapsdir}/*
%{_desktopdir}/*
