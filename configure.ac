#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ([2.59])
AC_INIT([pm_logconv-cs], [1.0])
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

CONFIG_DIR="$config_dir"
AC_SUBST(CONFIG_DIR)
HA_DATADIR="$datadir"
AC_SUBST(HA_DATADIR)
HA_NOARCHDATAHBDIR="$HA_DATADIR/$PM_PKG"
AC_SUBST(HA_NOARCHDATAHBDIR)
AC_PROG_LN_S

AC_CONFIG_FILES([Makefile])
AC_OUTPUT

