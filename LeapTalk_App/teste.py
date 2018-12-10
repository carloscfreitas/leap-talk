import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = ''
port = 3000

try:
    variavel = (host,port)
    s.bind(variavel)
except socket.error as e:
    print(e)
    exit(0)

s.listen(1)

conn, addr = s.accept()
print("acepted")

while True:
    try:
        i = 0
        userinput = input()
        conn.send((userinput + "\n").encode())
    except(KeyboardInterrupt, socket.error) as e:
        conn.close()
        s.close()