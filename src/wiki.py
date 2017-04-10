import urllib, json, re
query = 'water'
query= query.replace(' ', '+')
url = "https://en.wikipedia.org/w/api.php?action=query&origin=*&prop=extracts&converttitles=zh&format=json&exintro=&titles=" + query.title()
response = urllib.urlopen(url)
data = json.loads(response.read())
data = data['query']['pages']
page = data.keys()[0]
if page != '-1':
	print re.sub('<[^<]+?>', '', data[page]['extract'].split('\n')[0])
