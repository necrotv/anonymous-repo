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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,os,sys,time,subprocess
h = HTMLParser.HTMLParser()

versao = '1.0.1'
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
		if os.uname()[4] == 'armv6l': 
			#RASPBERRY
			if re.search(os.uname()[1],"openelec",re.IGNORECASE):
				mensagem_os("Openelec")
			else:
				mensagem_os("de Raspberry")
				addDir("Teclado","linux",1,artfolder + "keyboard.png")
		elif os.uname()[4] == 'armv7l': erro_os()
		else: 
			#LINUX
			mensagem_os("Linux")
			addDir("Teclado","linux",1,artfolder + "keyboard.png")
			addDir("Actualizar librtmp","-",7,artfolder + "dll.png",False)
			
	elif xbmc.getCondVisibility('system.platform.Android'): 
	#ANDROID
		mensagem_os("Android")
		addDir("Teclado","android",1,artfolder + "keyboard.png")
		addDir("Actualizar librtmp [COLOR blue](XBMC Gotham 13)[/COLOR]","-",5,artfolder + "dll.png",False)
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
	dialog.ok("Atenção!", "Estas modificações apenas funcionam no tema confluence (original).","[COLOR red]Não instale estas modificações na versão Helix (14) do XBMC! - Danifica o programa[/COLOR]")
	if url == "windows":
		addDir("QWERTY","qwerty",2,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde",2,artfolder + "keyboard.png",False)
	elif url == "android":
		addDir("QWERTY","qwerty",4,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde",4,artfolder + "keyboard.png",False)
	elif url == "linux":
		addDir("QWERTY","qwerty",6,artfolder + "keyboard.png",False)
		addDir("ABCDE","abcde",6,artfolder + "keyboard.png",False)
		
#########################################	LINUX

def librtmp_linux():
	ret = dialog.select('Qual é a sua versão do Linux?', ['x86', 'x64'])
	if ret == 0: url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x86&ATV1/librtmp.so.0"
	elif ret == 1: url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Linux/x64/librtmp.so.0"
	else: return

	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('XBMC Tools', 'A procurar ficheiro.','Por favor aguarde...')
	mensagemprogresso.update(50)
	file_path = find_abs_path("librtmp.so.0")

	if (os.path.exists(file_path) and "librtmp.so.0" in file_path) is False:
		mensagemprogresso.close()
		dialog.ok("Erro:", "Impossível aceder à pasta do teclado!")
		return

	librtmp_path = file_path.replace("librtmp.so.0","")
	my_tmp = os.path.join(addonfolder,"resources","temp","librtmp.so.0")
	mensagemprogresso.update(100)
	mensagemprogresso.close()

	password = dialog.input("Introduza a palavra pass (sudo):",type = xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
	if verifica_pass(password) is False: 
		dialog.ok("Erro:", "Password incorrecta!")
		return

	if download(my_tmp,url_download):
		p = subprocess.Popen("sudo -S rm " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		p = subprocess.Popen("sudo -S cp " + my_tmp + " " + librtmp_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		remove_ficheiro(my_tmp)
		dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
	else: dialog.ok("Erro:", "Operação abortada.")
    

def verifica_pass(password):
	p = subprocess.Popen("sudo -S su ", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
	(output, err) = p.communicate(password+"\n") 
	rc = p.returncode
	if rc == 0: return True
	return False

def change_keyboard_linux(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('XBMC Tools', 'A procurar ficheiro.','Por favor aguarde...')
	mensagemprogresso.update(50)
	file_path = find_abs_path("skin.confluence/720p/DialogKeyboard.xml")
	
	if (os.path.exists(file_path) and "skin.confluence/720p/DialogKeyboard.xml" in file_path) is False:
		mensagemprogresso.close()
		dialog.ok("Erro:", "Impossível aceder à pasta do teclado!")
		return
	
	keyboard_path = file_path.replace("DialogKeyboard.xml","")
	my_tmp = os.path.join(addonfolder,"resources","temp","DialogKeyboard.xml")
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	password = dialog.input("Introduza a palavra pass (sudo):",type = xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
	if verifica_pass(password) is False: 
		dialog.ok("Erro:", "Password incorrecta!")
		return
	
	if url == "qwerty": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
	elif url == "abcde": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
	
	if download(my_tmp,url_download):
		p = subprocess.Popen("sudo -S rm " + file_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		p = subprocess.Popen("sudo -S cp " + my_tmp + " " + keyboard_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
		p.communicate(password+"\n") 
		remove_ficheiro(my_tmp)
		dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
	else: dialog.ok("Erro:", "Operação abortada.")

def find_abs_path(str_path):
	p = subprocess.Popen('find / | grep ' + str_path, stdout=subprocess.PIPE,stderr=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	p_status = p.wait()
	return output.replace("\n","").replace(" ","")

#########################################	ANDROID
	
def checksu():
    os.system("su -c ''")
	
def librtmp_android():
	dialog = xbmcgui.Dialog()
	if not dialog.yesno("Aviso!", "Este procedimento apenas funciona em dispositivos com acesso root.","Continuar?"): return

	checksu()
	
	my_librtmp = os.path.join(addonfolder,"resources","temp","librtmp.so")
	librtmp_path = os.path.join(android_xbmc_path(), "lib")
	if os.path.exists(os.path.join(librtmp_path, "librtmp.so")) is False:
		dialog.ok("Erro:", "Impossível aceder à pasta do librtmp!")
		return
		
	if download(my_librtmp,"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Android/librtmp.so"):
		os.system("su -c 'rm "+os.path.join(librtmp_path, "librtmp.so")+"'")
		os.system("su -c 'cp -f "+my_librtmp+" "+librtmp_path+"/'")
		remove_ficheiro(my_librtmp)
		dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
	else: dialog.ok("Erro:", "Operação abortada.")
	
def change_keyboard_android(url):
	xbmc_data_path = android_xbmc_path()
	
	keyboard_path = os.path.join(xbmc_data_path, "cache/apk/assets/addons/skin.confluence/720p/DialogKeyboard.xml")
	if os.path.exists(keyboard_path) is False:
		dialog.ok("Erro:", "Impossível aceder à pasta do teclado!")
		return
	
	if url == "qwerty": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
	elif url == "abcde": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
	
	if remove_ficheiro(keyboard_path):
		if download(keyboard_path,url_download):
			dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
		else: dialog.ok("Erro:", "Operação abortada.")
	
def android_xbmc_path():	#Obrigado enen92!
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
		if os.path.exists(xbmc_data_path) and uid == os.stat(xbmc_data_path).st_uid: return xbmc_data_path
	return "erro"
#########################################	WINDOWS
	
def librtmp_windows():
	librtmp_path = os.path.join(xbmc_folder, "system/players/dvdplayer/librtmp.dll")
	if os.path.exists(librtmp_path) is False:
		dialog.ok("Erro:", "Impossível aceder à pasta do librtmp!")
		return
		
	if remove_ficheiro(librtmp_path):
		if download(librtmp_path,"http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/librtmp/Windows/librtmp.dll"):
			dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
		else: dialog.ok("Erro:", "Operação abortada.")
		
def change_keyboard_windows(url):
	keyboard_path = os.path.join(xbmc_folder, "addons/skin.confluence/720p/DialogKeyboard.xml")
	if os.path.exists(keyboard_path) is False:
		dialog.ok("Erro:", "Impossível aceder à pasta do teclado!")
		return
		
	if url == "qwerty": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/qwerty/DialogKeyboard.xml"
	elif url == "abcde": url_download = "http://anonymous-repo.googlecode.com/svn/trunk/xbmc-tools/keyboard/abcd/DialogKeyboard.xml"
		
	if remove_ficheiro(keyboard_path):
		if download(keyboard_path,url_download):
			dialog.ok("Aviso:", "Concluído!","Por favor reinicie o XBMC, para que as alterações façam efeito.")
		else: dialog.ok("Erro:", "Operação abortada.")

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
	sys.exit(0)
	
def download(mypath,url):
	if os.path.isfile(mypath) is True:
		dialog = xbmcgui.Dialog()
		dialog.ok('Erro','Já existe um ficheiro com o mesmo nome')
		return False
			  
	dp = xbmcgui.DialogProgress()
	dp.create('Download')
	start_time = time.time()		# url - url do ficheiro    mypath - localizacao ex: c:\file.mp3
	try: urllib.urlretrieve(url, mypath, lambda nb, bs, fs: dialogdown(nb, bs, fs, dp, start_time))
	except:
		while os.path.exists(mypath): 
			try: os.remove(mypath); break 
			except: pass
		dp.close()
		return False
	dp.close()
	return True

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
elif mode==5: librtmp_android()
elif mode==6: change_keyboard_linux(url)
elif mode==7: librtmp_linux()
xbmcplugin.endOfDirectory(int(sys.argv[1]))