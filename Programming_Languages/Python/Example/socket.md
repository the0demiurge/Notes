# Server

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", 8080))

try:
    sock.listen(5)
    while True:
        conn, addr = sock.accept()
        data = conn.recv(1000)
        print(data.decode('ascii'))
        conn.send(b'''HTTP/2 200 OK\nContent-Type: text/plain; charset=utf-8\n\n'''+data)
        conn.close()
except (KeyboardInterrupt):
    print('bye')
finally:
    sock.close()
```

# Client

```python
import socket

sock = socket.socket()
sock.connect(('localhost', 8080))

sock.send(bytes(input(), 'utf-8'))
data = sock.recv(1000)
print(data.decode('utf-8'))

sock.close()
```

