import json
import urllib.request
import urllib.error

payload = {"name":"Camilo","email":"camilo@example.com","password":"password123","is_active":True}
data = json.dumps(payload).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8000/users/', data=data, headers={'Content-Type':'application/json'})
try:
    resp = urllib.request.urlopen(req)
    print(resp.status)
    print(resp.read().decode())
except urllib.error.HTTPError as e:
    print('HTTP', e.code)
    try:
        print(e.read().decode())
    except Exception:
        pass
except Exception as e:
    import traceback
    traceback.print_exc()
