import socket

master_ip = "202.13.169.179"
master_port = 12345

slave_port = 12346

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", slave_port))

print("Conection")

while True:
    inputs = input("  あなた  ：")
    if inputs.lower() == "exit":
        break
    s.sendto(inputs.encode(), (master_ip, port))

    data, addr = s.recvfrom(1024)
    print(date.decode())

s.close()

