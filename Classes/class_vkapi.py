import urllib.request  # импортируем модуль
import json
"""https://vk.com/id1?w=wall1_2442097"""
req = urllib.request.Request('https://api.vk.com/method/wall.getComments?owner_id=1&post_id=2442097&v=5.92&access_token=8423c2448423c2448423c244d08441f2a1884238423c244dee1644d9e90529494134bf8') 
response = urllib.request.urlopen(req) # да, так тоже можно, не обязательно делать это с with, как в примере выше
result = response.read().decode('utf-8')
data = json.loads(result)
print(data)
#print(data['response']['items'][1]['text'])
#print(data['response']['items'][0]['text'])
#data['response']['items'][18]['copy_history'][0]['text']
