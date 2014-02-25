def obtem_url_google(url):
	""" Encontra streams para docs.google.com """
	html = abrir_url(url)
	FLASHVARS_START = 'flashVars":{'
	start = html.find(FLASHVARS_START) + len(FLASHVARS_START)
	end = html.find('}', start)

	flashvars = html[start:end]

	d = flashvars.decode('unicode-escape')
	decoded = urllib2.unquote(urllib2.unquote(d))

	urls = [l for l in decoded.split('url=') if 'mp4' in l and l.startswith('https')]
	qualidade = []
	url_video = []
	for u in urls:
		q = 'quality='
		quality = u[u.find(q) + len(q): u.find(',', u.find(q))]
		qualidade.append(quality)
		url_video.append(u[:-1])
	print qualidade
	print url_video
	index = xbmcgui.Dialog().select('Qualidade do vídeo:', qualidade)
	if index == -1: return
	return [url_video[index],'-']