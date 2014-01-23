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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser
h = HTMLParser.HTMLParser()

versao = '1.0.0'
addon_id = 'plugin.video.tugafilmes'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
fanart = addonfolder + '/fanart.jpg'

################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Categorias','-',1,artfolder + 'categorias.png')
	addDir('Filmes 2014','http://www.tuga-filmes.com/search/label/-%20Filmes%202013',2,artfolder + 'categorias.png')
	addDir('Destaques','http://www.tuga-filmes.com/search/label/destaque',2,artfolder + 'destaques.png')
	addDir('Pesquisar','-',3,artfolder + 'pesquisar.png')
	
	addLink("",'',artfolder + '-')
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Última versão instalada (' + versao + ')[/COLOR][/B]','',artfolder + 'versao.png')
	elif disponivel=='Erro ao verificar a versão!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'versao.png')
	else: addLink('[B][COLOR white]Versão nova disponível ('+ disponivel + '). Por favor actualize![/COLOR][/B]','',artfolder + 'versao.png')


###################################################################################
#FUNCOES
def categorias():
	addDir('Acção','http://www.tuga-filmes.com/search/label/Ac%C3%A7%C3%A3o',2,artfolder + 'categorias.png')
	addDir('Comédia','http://www.tuga-filmes.com/search/label/com%C3%A9dia',2,artfolder + 'categorias.png')
	addDir('Drama','http://www.tuga-filmes.com/search/label/Drama',2,artfolder + 'categorias.png')
	addDir('Romance','http://www.tuga-filmes.com/search/label/Romance',2,artfolder + 'categorias.png')
	addDir('Guerra','http://www.tuga-filmes.com/search/label/Guerra',2,artfolder + 'categorias.png')
	addDir('Terror','http://www.tuga-filmes.com/search/label/Terror',2,artfolder + 'categorias.png')
	addDir('Ficção','http://www.tuga-filmes.com/search/label/fic%C3%A7%C3%A3o-cientifica',2,artfolder + 'categorias.png')
	addDir('Aventura','http://www.tuga-filmes.com/search/label/Aventura',2,artfolder + 'categorias.png')
	addDir('Animação','http://www.tuga-filmes.com/search/label/Anima%C3%A7%C3%A3o',2,artfolder + 'categorias.png')
	addDir('Documentário','http://www.tuga-filmes.com/search/label/Document%C3%A1rio',2,artfolder + 'categorias.png')
	
	
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo/plugin.video.tugafilmes/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.tugafilmes" name="Tuga Filmes" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Erro ao verificar a versão!'
	return match
	
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile("<a href='(.+?)' title='(.+?)'><div style='.+?'>.+?</div>.+?<div id='.+?'></div></a>").findall(codigo_fonte) 
	img = re.compile('<img alt="" border="0" src="(.+?)"').findall(codigo_fonte) #<div style="text-align: center;"><img alt="" border="0" src="(.+?)"

	a = [] # url titulo img
	for x in range(0, len(match)):
		temp = [match[x][0],match[x][1],img[x]]; 
		a.append(temp);
	
	for url2, titulo, img in a:
		titulo = titulo.replace('&#39;',"'")
		addDirPlayer(titulo,url2,4,img)
		
	page = re.compile("<a class='blog-pager-older-link' href='(.+?)'").findall(codigo_fonte)
	for prox_pagina in page:
		addDir('Página Seguinte >>',prox_pagina,2,artfolder + 'proxpagina.png')
		break
	
def obtem_url_dropvideo(url):
	codigo_fonte = abrir_url(url)
	try: url_video = re.compile('var vurl = "(.+?)";').findall(codigo_fonte)[0]
	except: url_video = '-'
	try: url_legendas =	re.compile('var vsubtitle = "(.+?)";').findall(codigo_fonte)[0]
	except: url_legendas = '-'
	return [url_video,url_legendas]
	
def obtem_url_videomega(url):
	codigo_fonte = abrir_url(url)
	code = re.compile('document.write\(unescape\("(.+?)"\)\)\;').findall(codigo_fonte)
	texto = urllib.unquote(code[0])
	try: url_video = re.compile('file: "(.+?)"').findall(texto)[0]
	except: url_video = '-'
	try: url_legendas =	re.compile('"file": "(.+?)"').findall(texto)[0]
	except: url_legendas = '-'
	return [url_video,url_legendas]

def player(name,url,iconimage):
	mensagemprogresso = xbmcgui.DialogProgress()
	mensagemprogresso.create('Tuga-Filmes', 'A resolver link','Por favor aguarde...')
	mensagemprogresso.update(33)
	
	matriz = []
	codigo_fonte = abrir_url(url)
	try: url_video = re.compile('<iframe frameborder=".+?" height=".+?" scrolling=".+?" src="(.+?)"').findall(codigo_fonte)[0]
	except: return

	mensagemprogresso.update(66)
	
	if 'videomega' in url_video: matriz = obtem_url_videomega(url_video)
	elif 'dropvideo' in url_video: matriz = obtem_url_dropvideo(url_video)
	else: matriz[0] = matriz[1] = 'url desconhecido'
	
	url = matriz[0]
	if url=='-': return
	legendas = matriz[1]
	
	mensagemprogresso.update(100)
	mensagemprogresso.close()
	
	listitem = xbmcgui.ListItem() # name, iconImage="DefaultVideo.png", thumbnailImage="DefaultVideo.png"
	listitem.setPath(url)
	listitem.setProperty('mimetype', 'video/x-msvideo')
	listitem.setProperty('IsPlayable', 'true')
	try:
		xbmcPlayer = xbmc.Player(xbmc.PLAYER_CORE_AUTO)
		xbmcPlayer.play(url)
		if legendas != '-': xbmcPlayer.setSubtitles(legendas)
	except:
		dialog = xbmcgui.Dialog()
		dialog.ok(" Erro:", " Impossível abrir vídeo! ")
		pass
	
def pesquisa():
	keyb = xbmc.Keyboard('', 'Escreva o parâmetro de pesquisa') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://www.tuga-filmes.com/search?q=' + str(parametro_pesquisa) #nova definicao de url. str força o parametro de pesquisa a ser uma string
		listar_videos(url) #chama a função listar_videos com o url definido em cima

		###################################################################################

def addDirPlayer(name,url,mode,iconimage):
	codigo_fonte = abrir_url(url)
	try: plot = re.compile('<b>SINOPSE:.+?</b><span style=".+?">(.+?)</span>').findall(codigo_fonte)[0]
	except: plot = 'Erro a obter sinopse...'
	
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	liz.setInfo( type="Video", infoLabels= { "Title": name,
											 "OriginalTitle": name,
											 "Plot": plot 
											 } )
	cm = []
	cm.append(('Sinopse', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(cm, replaceItems=True)
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

def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', fanart)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
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
	categorias()
	
elif mode==2:
	print ""
	listar_videos(url)
	
elif mode==3:
	print ""
	pesquisa()

elif mode==4:
	print ""
	player(name,url,iconimage)
	
elif mode==5:
	print ""
	listar_videos_M18(url)
	
xbmcplugin.endOfDirectory(int(sys.argv[1]))
