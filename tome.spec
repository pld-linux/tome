
%define		file_version	%(echo %{version} | tr -d .)
Summary:	Troubles of Middle Earth - a roguelike game
Summary(pl):	Gra roguelike "Troubles of Middle Earth"
Name:		tome
Version:	1.0.0
Release:	1
License:	Distributable
Group:		Applications/Games
Source0:	http://t-o-m-e.net/pernangband/dl/%{name}-%{file_version}-src.tar.gz
Patch0:		%{name}-makefile.patch
URL:		http://www.t-o-m-e.net
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Troubles of Middle Earth (formerly PernAngband) is a complex roguelike
game based on the world created by JRR Tolkien. ToME is one of many
Angband variants.

%description -l pl
"Troubles of Middle Earth" (dawniej PernAngband) to rozbudowana gra
roguelike osadzona w ¶wiecie stworzonym przez JRR Tolkiena. ToME jest
jednym z wielu dostepnych wariantów Angbandu.

%prep
%setup -q -n %{name}%{file_version}-src
%patch0 -p1

%build
# Only build ncurses version (see patch), because I didn't manage to
# build any other working version
cd src
%{__make} -f makefile.org

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/games/tome
install -d $RPM_BUILD_ROOT/var/games/tome/{apex,save,data}

cd src
%{__make} install -f makefile.org DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_datadir}/games/tome/save
rm -rf $RPM_BUILD_ROOT%{_datadir}/games/tome/apex
rm -rf $RPM_BUILD_ROOT%{_datadir}/games/tome/data
# It doesn't look like files in this directory are currently used - 
# greatly reduces disk usage.
rm -rf $RPM_BUILD_ROOT%{_datadir}/games/tome/xtra

# According to FHS "save" and "apex" directories should be placed in
# /var/games, but ToME expects them to be in /usr/share/games/tome.
# We can modify sources, but it's not trivial, so I decided to use
# symlinks...
ln -sf /var/games/tome/save $RPM_BUILD_ROOT%{_datadir}/games/tome/save
ln -sf /var/games/tome/apex $RPM_BUILD_ROOT%{_datadir}/games/tome/apex
# This is another story - contents of this directory are generated
# from files in 'edit" directory during the first ToME run, and may be
# later regenerated (when orginal file in "edit" changes), so it
# belongs to /var
ln -sf /var/games/tome/data $RPM_BUILD_ROOT%{_datadir}/games/tome/data


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
#%doc *.gz
%attr(2755,root,games) %{_prefix}/games/%{name}
%{_datadir}/games/tome
%attr(775,root,games) /var/games/tome
