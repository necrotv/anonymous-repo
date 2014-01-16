#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Copyright 2013 Anonymous
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


addon_id = 'plugin.video.brazzers'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'


################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Source 1','-',0,addonfolder + artfolder + 'videos.png')
	addDir('Source 2','http://freehdporn.ws/brazzers.php',4,addonfolder + artfolder + 'videos.png')


	
###################################################################################
#FUNCOES
def fonte1():
	addDir('New Videos','http://brazzers.myporno.biz',1,addonfolder + artfolder + 'videos.png')
	addDir('Most Watched','http://brazzers.myporno.biz/?v_sortby=views&v_orderby=desc',1,addonfolder + artfolder + 'videos.png')
	addDir('Search','http://brazzers.myporno.biz',3,addonfolder + artfolder + 'search.png')
	codigo_fonte = abrir_url('http://brazzers.myporno.biz')
	match = re.compile('<li class="cat-item cat-item-.+?"><a href="(.+?)" title=".+?">(.+?)</a>').findall(codigo_fonte)
	for url, titulo in match:
		addDir(titulo,url,1,addonfolder + artfolder + 'videos.png')

def listar_videos2(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<iframe class="modal_video" src="(.+?)"').findall(codigo_fonte)
	match2 = re.compile('data-description="(.+?)"').findall(codigo_fonte)
	
	a = []
	for x in range(0, len(match)):
		temp = [match[x],match2[x]]; 
		a.append(temp);
	
	for url,titulo in a:
		codigo_fonte2 = abrir_url(url)
		img = re.compile('<img id="player_thumb" src="(.+?)"/></div>').findall(codigo_fonte2)
		#removed = re.compile('This video has been (.+?) from public access.').findall(codigo_fonte)
		#for a in removed:
			#if a == 'removed':
				#img = ''
				#continue
		titulo = titulo.replace("&#8211;","-")
		titulo = titulo.replace("&#8217;","'")
		addDir(titulo,url,2,img[0])
	
	page = re.compile("<div class='pages'><a class='active'>.+?</a><a href='(.+?)'>.+?<").findall(codigo_fonte)
	for url_prox_pagina in page:
		print url_prox_pagina
		addDir('Next page >>','http://freehdporn.ws/brazzers.php' + str(url_prox_pagina),4,addonfolder + artfolder + 'next.png')
		break
	
	
	xbmc.executebuiltin("Container.SetViewMode(500)")
	

def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('</header><iframe src="(.+?)"').findall(codigo_fonte)
	match2 = re.compile('title="Permalink to (.+?)"').findall(codigo_fonte)

	a = []
	for x in range(0, len(match)):
		temp = [match[x],match2[x]]; 
		a.append(temp);
	
	for url,titulo in a:
		codigo_fonte2 = abrir_url(url)
		img = re.compile('<img id="player_thumb" src="(.+?)"/></div>').findall(codigo_fonte2)
		#removed = re.compile('This video has been (.+?) from public access.').findall(codigo_fonte)
		#for a in removed:
			#if a == 'removed':
				#img = ''
				#continue
		titulo = titulo.replace("&#8211;","-")
		titulo = titulo.replace("&#8217;","'")
		addDir(titulo,url,2,img[0])
	
	page = re.compile("<span class='current'>.+?</span><a href='(.+?)' class='page larger'>.+?").findall(codigo_fonte)
	for url_prox_pagina in page:
		addDir('Next page >>',url_prox_pagina,1,addonfolder + artfolder + 'next.png')
		break
	
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def encontrar_fontes(url):
	codigo_fonte = abrir_url(url)
	#removed = re.compile('This video has been (.+?) from public access.').findall(codigo_fonte)
	#for a in removed:
		#if a == 'removed':
			#addLink('Removed','','')
			#return
		
	match = re.compile('cache720=(.+?)&amp').findall(codigo_fonte)
	img = re.compile('<img id="player_thumb" src="(.+?)"/></div>').findall(codigo_fonte)
	url = re.compile("var video_host = '(.+?)'").findall(codigo_fonte)
	id1 = re.compile("var video_uid = '(.+?)'").findall(codigo_fonte)
	id2 = re.compile("var video_vtag = '(.+?)'").findall(codigo_fonte)
	res = re.compile("var video_max_hd = '(.+?)'").findall(codigo_fonte)

	addLink('720',url[0] + 'u' + id1[0] + '/videos/' + id2[0] + '.' + '720' + '.mp4',img[0])
	addLink('480',url[0] + 'u' + id1[0] + '/videos/' + id2[0] + '.' + '480' + '.mp4',img[0])
	
def pesquisa():
	keyb = xbmc.Keyboard('', 'Search') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://brazzers.myporno.biz/?s=' + str(parametro_pesquisa) #nova definicao de url. str força o parametro de pesquisa a ser uma string
		listar_videos(url) #chama a função listar_videos com o url definido em cima
	#else:
		#CATEGORIES()
	
###################################################################################


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
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
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
		
elif mode==0:
		print ""
		fonte1()
		
elif mode==1:
		print ""
		listar_videos(url)

elif mode==4:
		print ""
		listar_videos2(url)
		
elif mode==2:
		print ""
		encontrar_fontes(url)
		
elif mode==3:
		print ""
		pesquisa()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
