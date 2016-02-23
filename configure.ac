#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.59])
AC_INIT([pm_logconv-cs], [2.2])
AM_INIT_AUTOMAKE
AC_PREFIX_DEFAULT(/usr)
PM_PKG="pacemaker"

#
# check for python
#
AM_PATH_PYTHON(2.4,,:)
AC_PATH_PROGS(PYTHON, python)
AC_MSG_CHECKING(where is python installed)
if test "x${PYTHON}" = x; then
        PYTHON="/usr/bin/env python";
fi
AC_MSG_RESULT(using $PYTHON);

# use when make rpm
AC_SUBST(WITH_LIST, [""])

prefix_orig="$prefix"
prefix=`eval echo "$prefix"`
case $prefix in
        NONE)   prefix=/usr;;
esac
var(){
        case $1 in
                *'${'*)         res=`eval echo "$1"`;;
                *)                      res="$1";;
        esac
        case "$res" in
                ""|NONE)        echo "$2";;
                *)                      echo "$res";;
        esac
}

#
# Keep copy of original (default) localstatedir
#
localstatedir_orig="$localstatedir"

exec_prefix=`var "$exec_prefix" "$prefix"`
datadir=`var "$datadir" "$prefix/share"`
config_dir=`var "$config_dir" "/etc/"`

AC_ARG_ENABLE([upstart],
        [AS_HELP_STRING([--enable-upstart],
                [support for the Upstart (default is auto)])],
        [],
        [enable_upstart=auto]
        )
AM_CONDITIONAL(SUPPORT_UPSTART, [test x"${enable_upstart}" = x"yes"])

AC_ARG_ENABLE([systemd],
        [AS_HELP_STRING([--enable-systemd],
                [support for the Systemd (default is auto)])],
        [],
        [enable_systemd=auto]
        )
AM_CONDITIONAL(SUPPORT_SYSTEMD, [test x"${enable_systemd}" = x"yes"])

AC_CHECK_PROG([UPSTART], [initctl], [yes], [no])
if test "x${UPSTART}" = x"yes"; then
        if test "x${enable_upstart}" = x"yes" -o "x${enable_upstart}" = x"auto"; then
                WITH_LIST="${WITH_LIST} --with upstart"
                PACKAGE_FEATURES="$PACKAGE_FEATURES upstart"
        fi
elif test "x${enable_upstart}" = x"yes"; then
        AC_MSG_ERROR("Not found initctl")
fi

AC_CHECK_PROG([SYSTEMD], [systemctl], [yes], [no])
if test "x${SYSTEMD}" = x"yes"; then
        if test "x${enable_systemd}" = x"yes" -o "x${enable_systemd}" = x"auto"; then
                WITH_LIST="${WITH_LIST} --with systemd"
                PACKAGE_FEATURES="$PACKAGE_FEATURES systemd"
        fi
elif test "x${enable_systemd}" = x"yes"; then
        AC_MSG_ERROR("Not found systemctl")
fi

AC_MSG_RESULT([  WITH_LIST        = ${WITH_LIST}])
AC_MSG_RESULT([  PACKAGE_FEATURES = ${PACKAGE_FEATURES}])

CONFIG_DIR="$config_dir"
AC_SUBST(CONFIG_DIR)
HA_DATADIR="$datadir"
AC_SUBST(HA_DATADIR)
HA_NOARCHDATAHBDIR="$HA_DATADIR/$PM_PKG"
AC_SUBST(HA_NOARCHDATAHBDIR)
AC_PROG_LN_S

AC_CONFIG_FILES(Makefile	\
		init/Makefile
		)
AC_OUTPUT

