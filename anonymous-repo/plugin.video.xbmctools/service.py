# -*- coding: utf-8 -*-
import datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon,os
from resources.lib.lib import librtmp
librtmp = librtmp()

addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)

if selfAddon.getSetting('auto_update_librtmp') == "false": auto_update_librtmp = False
else: auto_update_librtmp = True
if selfAddon.getSetting('android_hack') == "false": android_hack = False
else: android_hack = True

class service:
	def __init__(self):
		if xbmc.getCondVisibility('system.platform.Android'):
			if android_hack:
				my_librtmp = os.path.join(addonfolder,"resources","android_hack","librtmp.so")
				librtmp_path = os.path.join(self.android_xbmc_path(), "lib", "librtmp.so")
				os.system("su -c 'cat "+my_librtmp+" > "+librtmp_path+"'")
				os.system("su -c 'chmod 755 "+librtmp_path+"'")
			if auto_update_librtmp: librtmp.librtmp_android(True)

service()
