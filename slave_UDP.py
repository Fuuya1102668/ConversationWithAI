import getapi as get
import socket

import io
import simpleaudio as sa

#########
# SLAVE #
#########

master_ip = get.get_master_ip()
master_port = get.get_master_port()
slave_port = get.slava_port()

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", slave_port))

print("Conection server")

while True:
    inputs = input("  あなた  ：")
    s.sendto(inputs.encode(), (master_ip, master_port))
    if inputs.lower() == "exit":
        break

    response, addr = s.recvfrom(65535)
    response = pickle.load(response)
    sa.WaveObject.from_wave_file(io.BytesIO(response.content)).play()
    print(date.decode())

s.close()

