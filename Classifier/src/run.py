from sklearn.externals import joblib
import socket
from time import sleep

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
print("connection acepted")

# load the model from disk
trained_model = open("trained_model.sav", 'r')
loaded_model = joblib.load(trained_model)

try:
    while(True):
        result = loaded_model.predict(new_value)
        conn.send((result + "\n").encode())
        print(result)
        sleep(1)
except(KeyboardInterrupt, socket.error) as e:
    conn.close()
    s.close()