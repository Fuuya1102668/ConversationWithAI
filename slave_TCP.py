import getapi as get
import socket

import io
import simpleaudio as sa

#########
# SLAVE #
#  TCP  #
#########

master_ip = get.get_master_ip()
master_port = int(get.get_master_port())
slave_port = int(get.get_slave_port())

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, master_port))

print("Conection server")

while True:
    inputs = input("  あなた  ：")
    s.sendall(inputs.encode())
    if inputs.lower() == "exit":
        break
    while True:
        response = s.recv(4096)
        if not chunk:
            break
        response += chunk
    print("Total : " + str(len(response)))
    response = pickle.loads(response)
    sa.WaveObject.from_wave_file(io.BytesIO(response.content)).play()
    print(date.decode())

s.close()

