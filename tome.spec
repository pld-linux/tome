%define		file_version	%(echo %{version} | tr -d .)
Summary:	Troubles of Middle Earth - a roguelike game
Summary(pl):	Gra roguelike "Troubles of Middle Earth"
Name:		tome
Version:	2.0.0
Release:	2
License:	distributable
Group:		Applications/Games
Source0:	http://t-o-m-e.net/dl/src/%{name}-%{file_version}-src.tgz
Source1:	%{name}.png
Source2:	%{name}.desktop
Patch0:		%{name}-makefile.patch
Patch1:		%{name}-paths.patch
URL:		http://www.t-o-m-e.net
BuildRequires:	ncurses-devel
Requires:	applnk >= 1.5.13
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir		%{_prefix}/games

%description
Troubles of Middle Earth (formerly PernAngband) is a complex roguelike
game based on the world created by JRR Tolkien. ToME is one of many
Angband variants.

%description -l pl
"Troubles of Middle Earth" (dawniej PernAngband) to rozbudowana gra
roguelike osadzona w ¶wiecie stworzonym przez JRR Tolkiena. ToME jest
jednym z wielu dostepnych wariantów Angbandu.

%prep
%setup -q -n %{name}-%{file_version}-src
%patch0 -p1
%patch1 -p1

%build
# Only build ncurses version (see makefile patch), because I didn't
# manage to build any other working version
cd src
%{__make} -f makefile.org \
	COPTS="%{rpmcflags}" \
	CC="%{__cc}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_datadir}/games/tome
install -d $RPM_BUILD_ROOT%{_datadir}/games/tome/{cmov,dngn,edit,file,help,info,note,pref,scpt,user}
install -d $RPM_BUILD_ROOT/var/games/tome/{apex,save,data,bone}
install -d $RPM_BUILD_ROOT{%{_pixmapsdir},%{_applnkdir}/Games/RPG}

cp src/tome $RPM_BUILD_ROOT%{_bindir}
cp -r lib/{cmov,dngn,edit,file,help,info,note,pref,scpt,user} $RPM_BUILD_ROOT%{_datadir}/games/tome
# do not copy placeholders; bones are unnecessary
#cp -r lib/{apex,save,data} $RPM_BUILD_ROOT/var/games/tome

install %{SOURCE1} $RPM_BUILD_ROOT%{_pixmapsdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_applnkdir}/Games/RPG/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(2755,root,games) %{_bindir}/%{name}
%{_datadir}/games/tome
%attr(775,root,games) /var/games/tome
%{_pixmapsdir}/*
%{_applnkdir}/Games/RPG/*
