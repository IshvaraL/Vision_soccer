import socket
import pickle

HOST = "127.0.0.1"
PORT = 5005

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((HOST, PORT))

while True:
    s.listen()
    conn, addr = s.accept()

    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            else:
                message = pickle.loads(data)
                print(message)
                print("\n\n")
                header = message.pop(0)

                '''
                Display teams
                '''
                print("Raw:", header[0])
                print("Teams:", len(header[0][1:]))
                print("Consists of:", header[0][1:])


                print("Team size:", header[1])
                print("Data:", header[2])
                print("")

                for d in range(0, header[2][1]):
                    player_data = message[d]
                    print("Team id:", player_data[0])
                    print("Coords", player_data[1])
                    print("", player_data[2])
                    print("")

