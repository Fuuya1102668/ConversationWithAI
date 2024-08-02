import getapi as get
import socket

import io
import simpleaudio as sa

#########
# SLAVE #
#  TCP  #
#########

master_ip = get.get_master_ip()
master_port = get.get_master_port()
slave_port = get.get_slave_port()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((master_ip, int(master_port)))

print("Conection server")

while True:
    inputs = input("  あなた  ：")
    s.sendall(inputs.encode())
    if inputs.lower() == "exit":
        break
    response = s.recv(1000000)
    print("Total : " + str(len(responde)))
    response = pickle.loads(response)
    sa.WaveObject.from_wave_file(io.BytesIO(response.content)).play()
    print(date.decode())

s.close()

