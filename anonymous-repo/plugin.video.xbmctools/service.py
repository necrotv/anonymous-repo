# -*- coding: utf-8 -*-
import datetime,xbmc,xbmcplugin,xbmcgui,xbmcaddon
from resources.lib.lib import librtmp
librtmp = librtmp()

addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)

if selfAddon.getSetting('auto_update_librtmp') == "false": auto_update_librtmp = False
else: auto_update_librtmp = True

class service:
	def __init__(self):
		if xbmc.getCondVisibility('system.platform.Android'):
			librtmp_path = os.path.join(self.android_xbmc_path(), "lib", "librtmp.so")
			os.system("su -c 'chmod 755 "+librtmp_path+"'")
			
		if auto_update_librtmp and xbmc.getCondVisibility('system.platform.Android'):
			librtmp.librtmp_android(True)
	
	def __del__(self):
		if xbmc.getCondVisibility('system.platform.Android'):
			os.system("su -c 'chmod 000 "+librtmp_path+"'")
	
service()
