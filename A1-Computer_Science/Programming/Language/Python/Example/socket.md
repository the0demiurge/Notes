# TCP

## Server

bind -> listen -> accept -> conn.recv -> conn.send

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(("localhost", 8080))
sock.listen(5)

conn, addr = sock.accept()
data = conn.recv(1000)
print(data.decode('utf-8'))
conn.send(b'''HTTP/2 200 OK\nContent-Type: text/plain; charset=utf-8\n\n'''+data)
conn.close()

sock.close()
```

## Client

connect -> send -> recv

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 8080))

sock.send(bytes(input(), 'utf-8'))
data = sock.recv(1000)
print(data.decode('utf-8'))

sock.close()
```

# UDP

## Server

bind -> recvfrom

```python
import socket

address = ('127.0.0.1', 31500)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(address)
data, addr = sock.recvfrom(2048)
print(data.decode('utf-8'))
sock.close()
```

## Client

sendto

```python
import socket

address = ('127.0.0.1', 31500)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(bytes(input(), 'utf-8'), address)
sock.close()
```

