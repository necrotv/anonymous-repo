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

import urllib,urllib2,re,xbmcplugin,xbmcgui,xbmc,xbmcaddon,HTMLParser,time,os
h = HTMLParser.HTMLParser()

addon_id = 'plugin.video.freehdporn'
selfAddon = xbmcaddon.Addon(id=addon_id)
addonfolder = selfAddon.getAddonInfo('path')
artfolder = addonfolder + '/resources/img/'
versao = '1.0.1a'
base_url = 'http://www.freehdporn.ws/'
down_path = selfAddon.getSetting('download-folder')


################################################## 

#MENUS############################################

def CATEGORIES():
	addDir('Search','-',3,artfolder + 'search.png')
	addDir('Studios','-',4,artfolder + 'videos.png')
	addDir('Actresses','-',5,artfolder + 'videos.png')
	addDir('Categories','-',6,artfolder + 'videos.png')
	addLink("",'','-')
	addDir('[B][COLOR red]Open settings[/COLOR][/B]','-',8,artfolder + 'settings.png',pasta=False)
	disponivel=versao_disponivel()
	if disponivel==versao: addLink('[B][COLOR white]Last version installed (' + versao + ')[/COLOR][/B]','',artfolder + 'version.png')
	elif disponivel=='Error checking version!': addLink('[B][COLOR white]' + disponivel + '[/COLOR][/B]','',artfolder + 'version.png')
	else: addLink('[B][COLOR white]New version available... ('+ disponivel + '). Please update![/COLOR][/B]','',artfolder + 'version.png')
	
###################################################################################
#FUNCOES
def download(name,url):
	if down_path == '':
		dialog = xbmcgui.Dialog()
		dialog.ok(" Error:", "Please set your download folder!")
		selfAddon.openSettings()
		return
	
	name = re.sub('[^-a-zA-Z0-9_.()\\\/ ]+', '',name)
	name += '.mp4'
	mypath=os.path.join(down_path,name)
	if os.path.isfile(mypath) is True:
		dialog = xbmcgui.Dialog()
		dialog.ok('Error:','There is already a file with the same name!')
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
            tempo = 'Estimated time:' + ' %02d:%02d' % divmod(eta, 60) 
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
	  
def listar_estudios():
	codigo_fonte = abrir_url('http://www.freehdporn.ws')
	try: texto = re.findall('<h2>Studios</h2>(.+?)</ul>',codigo_fonte,re.DOTALL)[0]
	except: return
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url,titulo in match:
		addDir(titulo,base_url+url,1,artfolder + 'videos.png')

def listar_actrizes():
	codigo_fonte = abrir_url('http://www.freehdporn.ws')
	try: texto = re.findall('<h2>Actresses</h2>(.+?)</ul>',codigo_fonte,re.DOTALL)[0]
	except: return
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url,titulo in match:
		addDir(titulo,base_url+url,1,artfolder + 'videos.png')

def listar_categorias():
	codigo_fonte = abrir_url('http://www.freehdporn.ws')
	try: texto = re.findall('<h2>Category</h2>(.+?)</ul>',codigo_fonte,re.DOTALL)[0]
	except: return
	match = re.compile('<li><a href="(.+?)">(.+?)</a></li>').findall(texto)
	for url,titulo in match:
		addDir(titulo,base_url+url,1,artfolder + 'videos.png')	
		
def versao_disponivel():
	try:
		codigo_fonte=abrir_url('http://anonymous-repo.googlecode.com/svn/trunk/anonymous-repo-adults/plugin.video.freehdporn/addon.xml')		#ALTERAR NO FIM
		match=re.compile('<addon id="plugin.video.freehdporn" name="Free HD Porn" version="(.+?)"').findall(codigo_fonte)[0]
	except:
		match='Error checking version!'
	return match
	
def listar_videos(url):
	codigo_fonte = abrir_url(url)
	match = re.compile('<iframe class="modal_video" src="(.+?)"').findall(codigo_fonte)
	match2 = re.compile('data-description="(.+?)"').findall(codigo_fonte)
	print match2
	
	a = []
	for x in range(0, len(match)):
		temp = [match[x],match2[x]]; 
		a.append(temp);
	total = len(a)
	i=1
	for url,titulo in a:
		if titulo == '" class=':
			titulo = 'Video ' + str(i)
			i += 1
		codigo_fonte2 = abrir_url(url)
		try: img = re.compile('<img id="player_thumb" src="(.+?)"/></div>').findall(codigo_fonte2)[0]
		except: continue
		titulo = titulo.replace("&#8211;","-")
		titulo = titulo.replace("&#8217;","'")
		addDir(titulo,url,2,img,total)
	
	page = re.compile("class='active'>.+?</a><a href='(.+?)'>.+?<").findall(codigo_fonte)
	try: url_base = re.compile('<link rel="canonical" href="(.+?)"').findall(codigo_fonte)[0]
	except: return
	for url_prox_pagina in page:
		print url_prox_pagina
		addDir('Next page >>',url_base + str(url_prox_pagina),1,artfolder + 'next.png')
		break
	xbmc.executebuiltin("Container.SetViewMode(500)")
	
def encontrar_fontes(url):
	codigo_fonte = abrir_url(url)
		
	match = re.compile('cache720=(.+?)&amp').findall(codigo_fonte)
	img = re.compile('<img id="player_thumb" src="(.+?)"/></div>').findall(codigo_fonte)
	url = re.compile("var video_host = '(.+?)'").findall(codigo_fonte)
	id1 = re.compile("var video_uid = '(.+?)'").findall(codigo_fonte)
	id2 = re.compile("var video_vtag = '(.+?)'").findall(codigo_fonte)
	res = re.compile("var video_max_hd = '(.+?)'").findall(codigo_fonte)

	if res[0] == '3': addLink('720',url[0] + 'u' + id1[0] + '/videos/' + id2[0] + '.' + '720' + '.mp4',img[0],True)
	addLink('480',url[0] + 'u' + id1[0] + '/videos/' + id2[0] + '.' + '480' + '.mp4',img[0],True)
	
def pesquisa():
	keyb = xbmc.Keyboard('', 'Search') #Chama o keyboard do XBMC com a frase indicada
	keyb.doModal() #Espera ate que seja confirmada uma determinada string
	if (keyb.isConfirmed()): #Se a entrada estiver confirmada (isto e, se carregar no OK)
		search = keyb.getText() #Variavel search fica definida com o conteudo do formulario
		parametro_pesquisa=urllib.quote(search) #parametro_pesquisa faz o quote da expressao search, isto é, escapa os parametros necessarios para ser incorporado num endereço url
		url = 'http://freehdporn.ws/hd_porn.php?s=' + str(parametro_pesquisa) #nova definicao de url. str força o parametro de pesquisa a ser uma string
		listar_videos(url) #chama a função listar_videos com o url definido em cima
	
###################################################################################


def abrir_url(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

def addLink(name,url,iconimage,video=False):
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	liz.setInfo( type="Video", infoLabels={ "Title": name } )
	cm =[]
	if video: cm.append(('Download', 'XBMC.RunPlugin(%s?mode=7&url=%s&name=%s)' % (sys.argv[0], urllib.quote_plus(url),name)))
	liz.addContextMenuItems(cm, replaceItems=True) 	
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
	return ok

def addDir(name,url,mode,iconimage,total=1,pasta = True):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setProperty('fanart_image', addonfolder + '/fanart.jpg')
	cm =[]
	liz.addContextMenuItems(cm, replaceItems=True)
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
		
elif mode==1: listar_videos(url)
elif mode==2: encontrar_fontes(url)
elif mode==3: pesquisa()
elif mode==4: listar_estudios()
elif mode==5: listar_actrizes()
elif mode==6: listar_categorias()
elif mode==7: download(name,url)
elif mode==8: selfAddon.openSettings()
xbmcplugin.endOfDirectory(int(sys.argv[1]))
