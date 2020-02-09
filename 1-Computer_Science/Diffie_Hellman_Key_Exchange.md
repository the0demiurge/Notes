```python
mod = 53  # large prime number
base = 5  # usually 2 to 5
index_a = 30  # large number
index_b = 25  # large number


class Diffie_Hellman_Key_Exchanger(object):
    def __init__(self, base=None, mod=None, _private_index=None, external_message=None):
        self.base = base
        self.mod = mod
        self._private_index = _private_index
        self.external_message = None
        self.public_message = None
        self._key = None

    def get_public_message(self):
        self.public_message = self.base ** self._private_index % self.mod
        return self.public_message

    def get_key(self):
        self._key = self.external_message ** self._private_index % self.mod
        return self._key


Alice = Diffie_Hellman_Key_Exchanger(base, mod, index_a)
Bob = Diffie_Hellman_Key_Exchanger(None, None, index_b)

# Alice compute public message
Alice.get_public_message()

# Alice send base, mod, public message -> Bob
Bob.base, Bob.mod, Bob.external_message = Alice.base, Alice.mod, Alice.public_message

# Bob receive base, mod to compute public message, send to Alice
Bob.get_public_message()
Alice.external_message = Bob.public_message

# compute key from external public message with private index and mod
print(Alice.get_key(), Bob.get_key())
```
