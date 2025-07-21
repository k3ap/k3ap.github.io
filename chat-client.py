import socket
import threading
import random


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def string_to_numbers(msg, bitwidth):
    # To funkcijo lahko spreminjaš, ampak ni potrebno
    if isinstance(msg, str):
        msg = msg.encode()

    if len(msg) % bitwidth != 0:
        msg = b"\0" * (bitwidth - len(msg) % bitwidth) + msg

    nums = []
    for i in range(0, len(msg), bitwidth):
        num = int.from_bytes(msg[i:i+bitwidth], "big")
        nums.append(num)

    return nums


def numbers_to_string(nums, bitwidth):
    # To funkcijo lahko spreminjaš, ampak ni potrebno
    msg = b""
    for num in nums:
        msg += num.to_bytes(bitwidth, "big")

    for i in range(len(msg)):
        if msg[i] != b'\n':
            msg = msg[i:]
            break

    return msg


def najdi_prastevilo(spodnja_meja, zgornja_meja):
    # Te funkcije ne spreminjaj!

    def check_composite(n, a, d, s):
        x = pow(a, d, n)
        if x == 1 or x == n-1: return False
        for r in range(s):
            x = x * x % n
            if x == n-1:
                return False
        return True

    def miller_rabin(n, iters=5):
        if n < 4: return n == 2 or n == 3
        if n % 2 == 0 or n % 3 == 0 or n % 5 == 0: return False

        s = 0
        d = n-1
        while (d & 1) == 0:
            d >>= 1
            s += 1

        for i in range(iters):
            a = 2 + random.randint(0, n-3)
            if check_composite(n, a, d, s):
                return False

        return True

    while not miller_rabin(num := random.randint(spodnja_meja, zgornja_meja)):
        pass

    return num


def inverz(x, n):
    # Te funkcije ne spreminjaj!
    def eea(a, b):
        x = 1
        y = 0
        x1 = 0
        y1 = 1
        a1 = a
        b1 = b
        while b1 > 0:
            q = a1 // b1
            x, x1 = x1, x - q * x1
            y, y1 = y1, y - q * y1
            a1, b1 = b1, a1 - q * b1
        return a1, x, y

    d, a, b = eea(x, n)
    if d != 1:
        raise Exception("gcd(x, n) != 1, cannot invert")
    return a

def send_introduction(name):
    # Te funkcije ne spreminjaj!
    sock.sendall(name)


def encode_message(msg):
    # To funkcijo lahko spremeniš.
    if isinstance(msg, str):
        msg = msg.encode()
    return msg


def send_message(msg):
    # Te funkcije ne spreminjaj!
    msg = encode_message(msg)
    length = len(msg).to_bytes(4, "big")
    sock.sendall(length + msg)


def decode_message(msg):
    # To funkcijo lahko spremeniš.
    return msg.decode()


def receive_message():
    # Te funnkcije ne spreminjaj!
    sender = sock.recv(32).decode()
    length = int.from_bytes(sock.recv(4), "big")
    msg = sock.recv(length)
    if msg:
        try:
            print("\r"+sender, "::", decode_message(msg))
        except:
            print(f"\rReceived non-decryptable message from '{sender}'")
        finally:
            print("> ", end="", flush=True)


def receive_messages():
    # Te funkcije ne spreminjaj!
    while True:
        receive_message()


if __name__ == "__main__":
    host = input("IP? ").strip()
    port = int(input("Port? ").strip())
    name = input("Name? ").strip().encode()
    name = bytes(32 - len(name)) + name

    sock.connect((host, port))
    send_introduction(name)

    threading.Thread(target=receive_messages, daemon=True).start()

    try:
        while True:
            msg = input("> ")
            if not msg:
                break
            send_message(msg)

    finally:
        sock.close()
        print("Disconnected.")
