# BidulaxStudio Links
A python FastAPI to make short links !

## Usage
```python
import requests

res = requests.put('http://localhost:8000/add', params={'token': 'a_wonderful_token', 'link': 'https://example.com/'})
print(res.json()) # {'code': 'ABC123', 'link': 'https://google.com/'}

res = requests.post('http://localhost:8000/edit', params={'token': 'a_wonderful_token', 'code': 'ABC123', 'new_link': 'https://anotherexample.com/'})
print(res.json()) # {'code': 'ABC123', 'old_link': 'https://example.com/', 'new_link': 'https://anotherexample.com/'}

res = requests.delete('http://localhost:8000/delete', params={'token': 'a_wonderful_token', 'code': 'ABC123'})
print(res.json()) # {'code': 'ABC123', 'link': 'https://anotherexample.com/'}

res = requests.get('http://localhost:8000/links', params={'token': 'a_wonderful_token'})
print(res.json()) # [{'code': DEF456, 'link': 'https://anexample.com/'}, {'code': GHI789, 'link': 'https://asecondexample.com/'}]

# You can open your browser and type 'http://localhost:8000/go/ABC123' and you'll be redirected to the link !
```

## Warning
Be careful if you use this code ! For the moment I didn't consider it necessary to make a real token management... Anyone can use a wrong token and add, edit or delete links !

## Credits
- Made by Bidulman
- With Python
- And FastAPI
