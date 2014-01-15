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


addon_id = 'plugin.audio.rcpodcast'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = '/resources/img/'


################################################## 

#MENUS############################################

def CATEGORIES():
	#addDir('Barulho das Luzes','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=3',1,addonfolder + artfolder + '3.jpg')    #onclick="play_wma
	addDir('Barulho das Luzes - Entrevistas','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=10',1,addonfolder + artfolder + '3.jpg')
	addDir('Caderneta de Cromos','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=17',1,addonfolder + artfolder + '17.jpg')
	addDir('Grandiosa História Universal das Traquitanas','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=40',1,addonfolder + artfolder + '40.jpg')
	addDir('Homem que mordeu o Cão','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=47',1,addonfolder + artfolder + '47.jpg')
	addDir('Mixórdia de Temáticas','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=36',1,addonfolder + artfolder + '36.jpg')
	addDir('Momentos da Manhã','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=25',1,addonfolder + artfolder + '25.jpg')
	addDir('Ouvintes no ar','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=26',1,addonfolder + artfolder + '26.jpg')
	addDir('Primo','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=19',1,addonfolder + artfolder + '19.jpg')
	#addDir('TNT - Todos no top','http://www.radiocomercial.iol.pt/podcast/index.aspx?id=11',1,addonfolder + artfolder + '11.jpg')
	addLink('teste','http://www.radiocomercial.iol.pt/player/silver/?wma=/rcomercial/8484GAJZ-3F1U-4N0G-PCP8-CRQJK6AQU2W6.wma','')
	


###################################################################################
#FUNCOES

def listar_videos(url):
	codigo_fonte = abrir_url(url)
	dia = re.compile('<div class="dia">(.+?)</div>').findall(codigo_fonte)
	mes = re.compile('<div class="mes">(.+?)</div>').findall(codigo_fonte)
	ano = re.compile('<div class="ano">(.+?)</div>').findall(codigo_fonte)
	url = re.compile('<a title="Download" href="(.+?)"').findall(codigo_fonte)
	titulo = re.compile('<h2 style=".+?">(.+?)</h2>').findall(codigo_fonte)
	page = re.compile('<li class="current">.+?</li><li><a href="(.+?)"').findall(codigo_fonte)
	print titulo
	a = []
	for x in range(0, len(url)):
		temp = [titulo[x],dia[x],mes[x],ano[x],url[x]]; 
		a.append(temp);
	
	for titulo, dia, mes, ano, url in a:
		titulo = titulo.replace("\xe9","é")
		titulo = titulo.replace("\xe1","á")
		titulo = titulo.replace("\xf3","ó")
		titulo = titulo.replace("\xca","Ê")
		titulo = titulo.replace("\xe3","ã")
		titulo = titulo.replace("\xed","í")
		titulo = titulo.replace("\xea","ê")
		titulo = titulo.replace("\xe7","ç")
		titulo = titulo.replace("\xf5","õ")
		addLink(titulo + ' - ' + dia + '/' + mes + '/' + ano,url,'')
	
	for prox_pagina in page:
		addDir('Página Seguinte >>','http://www.radiocomercial.iol.pt/podcast/' + prox_pagina,1,'')
	

###################################################################################
#FUNCOES JÁ FEITAS


def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultAudio.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Audio", infoLabels={ "Title": name } )
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

elif mode==1:
	print ""
	listar_videos(url)
       
xbmcplugin.endOfDirectory(int(sys.argv[1]))
