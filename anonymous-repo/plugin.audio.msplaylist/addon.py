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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,socket
socket.setdefaulttimeout( 10 )  # timeout in seconds
h = HTMLParser.HTMLParser()

versao = '1.0.0'
addon_id = 'plugin.audio.msplaylist'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
playlist = addonfolder + '/resources/playlist/playlist.txt'
fanart = addonfolder + '/fanart.jpg'
download_path = selfAddon.getSetting('download-folder')

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Top 20','http://mp3skull.com/',2,artfolder + 'top.png')
	addDir('Pesquisar','-',1,artfolder + 'Search.png')
	addDir('Playlist','-',5,artfolder + 'Playlist.png')
	
	addLink('','-','-')
	addDir('[B][COLOR white]Aviso[/COLOR][/B]','-',11,artfolder + 'aviso.png',False)
	addDir('[B][COLOR blue]Definições do addon[/COLOR][/B]','-',9,artfolder + 'Settings.png',False)
	addLink('','-','-')
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','-',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','-',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','-',artfolder + 'versao.png')

###################################################################################
#FUNCOES
def listar_musicas(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<div id="topright"><a href="(.+?)" title=".+?">(.+?)</a>').findall(codigo_fonte)
	for url,titulo in match:
		titulo = titulo.replace('Mp3','')
		addDir(titulo,'http://mp3skull.com'+url,7,artfolder + 'music.png')

def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.audio.msplaylist/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.audio.msplaylist" name="Mp3 Skull Playlist" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
def pesquisa():
	keyb = xbmc.Keyboard('', 'Search') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		search = search.replace(' ','_')
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://mp3skull.com/mp3/' + str(parametro_pesquisa) + '.html' #nova definicao de url. str força o parametro de pesquisa a ser uma string
		encontrar_fontes(url) #chama a função listar_videos com o url definido em cima

def encontrar_fontes(url):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Mp3 Skull Playlist', 'A encontrar fontes','Por favor aguarde...')
	mensagemprogresso.update(50)
	codigo_fonte = abrir_url(url)
	mp3 = re.compile('<div style="float:left;"><a href="(.+?)"').findall(codigo_fonte)
	titulo = re.compile('<div style="font-size:15px;"><b>(.+?) mp3</b>').findall(codigo_fonte)
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	for x in range(0,len(mp3)):
		try:
			mp3[x] = mp3[x].replace(' ','%20')
			titulo[x] = titulo[x].replace('&','and')
			addMusica(titulo[x],mp3[x],3,'DefaultAudio.png')
		except: pass
		
def play(url):
	try: mp3file = urllib2.urlopen(url)
	except: 
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir música! ")
		return
	playlst = xbmc.PlayList(1)
	playlst.clear()
	listitem = xbmcgui.ListItem()
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'audio/mpeg')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir música! ")
		pass
		
def download(name,url):
	if download_path == '':
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", "Pasta de Download não definida!","Defina-a nas definições.")
		return
	try:
		f = urllib2.urlopen(url)
		with open(download_path + name + '.mp3', "wb") as code:
			code.write(f.read())
		dialog = xbmcgui.Dialog()
		dialog.ok(" Download:", "Download bem sucedido!")
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", "Download interrompido!")
		
def mensagemaviso():
    try:
        xbmc.executebuiltin("ActivateWindow(10147)")
        window = xbmcgui.Window(10147)
        xbmc.sleep(100)
        window.getControl(1).setLabel( "%s - %s" % ('AVISO','Mp3 Skull Playlist',))
        window.getControl(5).setText("[COLOR red][B]Termos:[/B][/COLOR]\nEste addon não aloja quaisquer conteúdos. O conteúdo apresentado é da responsabilidade dos servidores e em nada está relacionado com este addon.\n\nEste addon não é, de maneira alguma, um incentivo à pirataria.\n\n[COLOR red][B]Dicas:[/B][/COLOR]\nEvite adicionar à Playlist músicas que sejam lentas a carregar e/ou na sua reprodução, para um bom funcionamento do addon.\n\nTenha em conta que alguns servidores são mais rápidos do que outros.")
    except: pass

############################################## PLAYLIST #################################		
		
def save(name,url):
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: open(playlist, 'a').close()
	
	flag = True
	f = open(playlist,"w")
	for line in lines:
		if line == 'name="' + name + '" url="' + url + '"\n': flag = False
		f.write(line)
	if flag: f.write('name="' + name + '" url="' + url + '"\n')
	f.close()

def remove(name,url):
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: pass
	
	try: f = open(playlist,"w")
	except: return
	for line in lines:
		print line
		print str('name="' + name + '" url="' + url + '"\n')
		if line != str('name="' + name + '" url="' + url + '"\n'): f.write(line)
	f.close()
	
def le_playlist():
	lines = []
	try:
		f = open(playlist,"r")
		lines = f.readlines()
		f.close()
	except: pass
	for line in lines:
		match = re.compile('name="(.+?)" url="(.+?)"').findall(line)
		addMusicaPlaylist(match[0][0],match[0][1],'DefaultAudio.png')
	
	addLink('','-','-')
	addDir('[B][COLOR white]Apagar Playlist[/B][/COLOR]','-',10,artfolder + 'delete.png')
		
def apaga_playlist():
	dialog = xbmcgui.Dialog()
	if dialog.yesno("Aviso!", "Tem a certeza que deseja apagar a Playlist?"):
		try: 
			f = open(playlist,"w")
			f.close()
		except: return
	else: return


###################################################################################
#FUNCOES JÁ FEITAS
def addMusicaPlaylist(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	cm = []
	cm.append(('Adicionar à playlist', 'XBMC.RunPlugin(%s?mode=4&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append(('Remover da playlist', 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append(('Download', 'XBMC.RunPlugin(%s?mode=8&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	liz.setInfo( type="Audio", infoLabels={ "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz,isFolder=False)
	return ok

def addMusica(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Audio", infoLabels={ "Title": name } )
	cm = []
	cm.append(('Adicionar à playlist', 'XBMC.RunPlugin(%s?mode=4&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append(('Remover da playlist', 'XBMC.RunPlugin(%s?mode=6&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	cm.append(('Download', 'XBMC.RunPlugin(%s?mode=8&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True)
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok
	
def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,pasta = True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=pasta)
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


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

try:        
        iconimage=urllib.unquote_plus(params["iconimage"])
except:
        pass


print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)
print "Iconimage: "+str(iconimage)




###############################################################################################################
#                                                   MODOS                                                     #
###############################################################################################################


if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()

elif mode==1:
	print ""
	pesquisa()
	
elif mode==2:
	print ""
	listar_musicas(url)
	
elif mode==3:
	print ""
	play(url)
	
elif mode==4:
	print ""
	save(name,url)

elif mode==5:
	print ""
	le_playlist()
	
elif mode==6:
	print ""
	remove(name,url)
	
elif mode==7:
	print ""
	encontrar_fontes(url)

elif mode==8:
	print ""
	download(name,url)
	
elif mode==9:
	selfAddon.openSettings()

elif mode==10:
	apaga_playlist()

elif mode==11:
	mensagemaviso()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
