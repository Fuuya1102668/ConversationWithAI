import socket

##########
# MASTER #
##########

slave_ip = "192.168.11.48"
slave_port = 12346

master_port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", master_port))

print("conectino")

while True:
    data, addr = s.recvfrom(65535)
    print(data.decode())

    a = input("入力：")
    s.sendto("gogogo".encode(), (slave_ip, slave_port))

s.close()

