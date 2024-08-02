import getapi as get
import socket
import pickle

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

print("Connected to server")

try:
    while True:
        inputs = input("  あなた  ：")
        s.sendall(inputs.encode())
        if inputs.lower() == "exit":
            break
        
        response = b''
        while True:
            part = s.recv(4096)
            if not part:
                break
            response += part
        
        print("Data received")
        print("Total : " + str(len(response)))
        
        response_content = pickle.loads(response)
        sa.WaveObject.from_wave_file(io.BytesIO(response_content)).play()
        print("Response played")

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    s.close()
    print("Connection closed")

