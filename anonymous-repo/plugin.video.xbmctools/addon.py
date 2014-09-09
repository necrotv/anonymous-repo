#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2014 Anonymous
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


##############BIBLIOTECAS A IMPORTAR E DEFINICOES####################

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time
h = HTMLParser.HTMLParser()

versao = '1.0.0'
addon_id = 'plugin.video.xbmctools'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
dialog = xbmcgui.Dialog()

xbmc_folder = selfAddon.getSetting('xbmc-folder')

################################################## 

#MENUS############################################

def CATEGORIES():
	if xbmc.getCondVisibility('system.platform.windows'):
	#WINDOWS
		mensagem_os("Windows")
		dialog.ok("IMPORTANTE!", "Estas modificações apenas funcionam se o XBMC for executado como administrador.")
		if xbmc_folder == "": 
			mensagem_aviso("Por favor defina a pasta do XBMC nas configurações.")
			selfAddon.openSettings()
		addDir("Teclado","windows",1,artfolder + "keyboard.png")
		addDir("Actualizar librtmp","-",3,artfolder + "dll.png",False)
	#-----------------------------------------------------------------------
	elif xbmc.getCondVisibility('System.Platform.OSX'): erro_os()
	elif xbmc.getCondVisibility('system.platform.linux') and not xbmc.getCondVisibility('system.platform.Android'):
		if os.uname()[4] == 'armv6': erro_os()
		elif os.uname()[4] == 'armv7': erro_os()
		else: erro_os()
	elif xbmc.getCondVisibility('system.platform.Android'): 
	#ANDROID
		mensagem_os("Android")
		addDir("Teclado","android",1,artfolder + "keyboard.png")
	#-------------------------------------------------------------------
	elif xbmc.getCondVisibility('system.platform.IOS'): erro_os()
	else: erro_os()
	
	addLink('','','nothing')
	disponivel=versao_disponivel() # nas categorias
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def keyboard(url):
	dialog.ok("Atenção!", "Estas modificações apenas funcionam no tema confluence (original).")
	if url == "windows":
		addDir("QWERTY","qwerty",2,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde",2,artfolder + "keyboard.png",False)
	elif url == "android":
		addDir("QWERTY","qwerty",4,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde",4,artfolder + "keyboard.png",False)
#########################################	ANDROID
	
def change_keyboard_android(url):
	#dialog.ok("Aviso:",url)
	android_xbmc_path()
	
def android_xbmc_path():
	xbmcfolder=xbmc.translatePath(addonfolder).split("/")
	i = 0
	found = False
	
	for folder in xbmcfolder:
		if folder.count('.') >= 2 and folder != addon_id :
			found = True
			break
		else:
			i+=1

	if found == True:
		uid = os.getuid()
		app_id = xbmcfolder[i]
		xbmc_data_path = os.path.join("/data", "data", app_id)
		dialog.ok("Aviso:",xbmc_data_path,uid)
		return
	dialog.ok("Aviso:","Erro")
#########################################	WINDOWS
	
def librtmp_windows():
	librtmp_path = os.path.join(xbmc_folder, "system/players/dvdplayer")
	if os.path.exists(librtmp_path) is False:
		dialog.ok("Erro:", "Impossível aceder à pasta do librtmp!")
		return
		
	if remove_ficheiro(os.path.join(librtmp_path, "librtmp.dll")):
		download(os.path.join(librtmp_path, "librtmp.dll"),"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Windows/librtmp.dll")
		dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
	
def change_keyboard_windows(url):
	keyboard_path = os.path.join(xbmc_folder, "addons/skin.confluence/720p")
	if os.path.exists(keyboard_path) is False:
		dialog.ok("Erro:", "Impossível aceder à pasta do teclado!")
		return
		
	if url == "qwerty":
		if remove_ficheiro(os.path.join(keyboard_path, "DialogKeyboard.xml")):
			download(os.path.join(keyboard_path, "DialogKeyboard.xml"),"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml")
			dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
	elif url == "abcde":
		if remove_ficheiro(os.path.join(keyboard_path, "DialogKeyboard.xml")):
			download(os.path.join(keyboard_path, "DialogKeyboard.xml"),"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml")
			dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
	
#########################################

def remove_ficheiro(file_path):
	while os.path.exists(file_path): 
			try: os.remove(file_path); break 
			except:	
				dialog = xbmcgui.Dialog()
				if dialog.yesno("Erro!", "Tentar outra vez?", "Caso o erro persista, certifique-se que iniciou o XBMC como administrador."): pass
				else: 
					return False
	return True
	
def mensagem_aviso(aviso):
	dialog.ok("Aviso:", aviso)
	
def mensagem_os(so_name):
	dialog.ok("Aviso:", "O XBMC está a detectar o sistema operativo " + so_name +".","Caso este não seja o seu sistema, por favor saia do addon.")

def erro_os():
	dialog.ok("Erro:", "Sistema operativo não suportado!")
	
	
def download(mypath,url):
	if os.path.isfile(mypath) is True:
		dialog = xbmcgui.Dialog()
		dialog.ok('Erro','Já existe um ficheiro com o mesmo nome')
		return
			  
	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	start_time = time.time()		# url - url do ficheiro    mypath - localizacao ex: c:\file.mp3
	try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
	except:
		while os.path.exists(mypath): 
			try: os.remove(mypath); break 
			except: pass
		dp.close()
		return
	dp.close()

def dialogdown(numblocks, blocksize, filesize, dp, start_time):
      try:
            percent = min(numblocks * blocksize * 100 / filesize, 100)
            currently_downloaded = float(numblocks) * blocksize / (1024 * 1024) 
            kbps_speed = numblocks * blocksize / (time.time() - start_time) 
            if kbps_speed > 0: eta = (filesize - numblocks * blocksize) / kbps_speed 
            else: eta = 0 
            kbps_speed = kbps_speed / 1024 
            total = float(filesize) / (1024 * 1024) 
            mbs = '%.02f MB de %.02f MB' % (currently_downloaded, total) 
            e = ' (%.0f Kb/s) ' % kbps_speed 
            tempo = 'Tempo estimado:' + ' %02d:%02d' % divmod(eta, 60) 
            dp.update(percent, mbs + e,tempo)
      except: 
            percent = 100 
            dp.update(percent) 
      if dp.iscanceled(): 
            dp.close()
            raise StopDownloading('Stopped Downloading')

class StopDownloading(Exception):
      def __init__(self, value): self.value = value 
      def __str__(self): return repr(self.value)

def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.xbmctools/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.xbmctools" name="XBMC Tools" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
###################################################################################
#FUNCOES JÁ FEITAS

def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,total=1):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,totalItems=total)
	return ok

def addDir(name,url,mode,iconimage,pasta = True,total=1):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta,totalItems=total)
	return ok

############################################################################################################
#                                               GET PARAMS                                                 #
############################################################################################################
              
def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1] 
	return param

params=get_params()
url=None
name=None
mode=None
iconimage=None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)

###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################

if mode==None or url==None or len(url)<1: CATEGORIES()
elif mode==1: keyboard(url)
elif mode==2: change_keyboard_windows(url)
elif mode==3: librtmp_windows()
elif mode==4: change_keyboard_android(url)
xbmcplugin.endOfDirectory(int(sys.argv[1]))