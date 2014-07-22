MAINTAINERCLEANFILES = Makefile.in

# BUILD

if SUPPORT_UPSTART
upstartdir		= /etc/init
upstart_DATA		= pm_logconv_init.conf
endif

if SUPPORT_SYSTEMD
systemddir		= /usr/lib/systemd/system
systemd_DATA		= pm_logconv.service
endif
