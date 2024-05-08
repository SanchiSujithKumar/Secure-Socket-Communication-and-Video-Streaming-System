from socket import *
import threading
import json
import cv2

movies=["video_1_240p.mp4","video_1_720p.mp4","video_1_1440p.mp4"]

def handle_client(client_socket, clients, clients_socket):
    client_name = client_socket.recv(4096).decode()
    public_key = client_socket.recv(4096).decode()
    clients[client_name] = public_key
    clients_socket[client_name]=client_socket
    broadcast(clients, clients_socket)

    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        if data == b'QUIT':
            del clients[client_name]
            del clients_socket[client_name]
            client_socket.close()
            broadcast(clients, clients_socket)
            break
        elif data == b'VIDEO':
            global movies
            movie_list=""
            for mv in movies:
                movie_list+=mv + " "
            client_socket.send("#".encode())
            data = client_socket.recv(4096)
            client_socket.send(movie_list.encode())
            video_name = client_socket.recv(4096).decode()
            client_socket.send(f"Playing video {video_name}.mp4 in different resolutions".encode())
            try:
                video_files = [
                    f"../video/{video_name}_240p.mp4",
                    f"../video/{video_name}_720p.mp4",
                    f"../video/{video_name}_1440p.mp4"
                ]
                current_file_index = 0
                while current_file_index < len(video_files):
                    cap = cv2.VideoCapture(video_files[current_file_index])
                    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    start_frame = (total_frames // 3)*current_file_index
                    end_frame = (total_frames // 3) * (current_file_index+1)
                    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
                    while cap.isOpened():
                        ret, frame = cap.read()
                        if not ret:
                            break
                        current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))
                        frame_data = cv2.imencode('.jpg', frame)[1].tobytes()
                        client_socket.sendall((str(len(frame_data))).encode().ljust(16) + frame_data)
                        if  current_frame >= end_frame:
                            current_file_index += 1
                            if current_file_index == 3:
                                client_socket.sendall(b'0')
                            break
                    cap.release()
            except Exception as e:
                print(f"Error: {e}")
        else:
            broadcast_message(data, clients_socket)

def broadcast(clients, clients_socket):
    broadcast_data = json.dumps(clients)
    for client_socket in clients_socket:
        clients_socket[client_socket].send(broadcast_data.encode())

def broadcast_message(message, clients_socket):
    for client_socket in clients_socket:
        clients_socket[client_socket].send(".".encode())
        data = clients_socket[client_socket].recv(4096)
        clients_socket[client_socket].send(message)

def main():
    server = socket(AF_INET, SOCK_STREAM)
    server.bind(('localhost', 9999))
    server.listen(1)

    clients = {}
    clients_socket = {}

    print("Server started. Listening for connections...")

    while True:
        client_socket, addr = server.accept()
        print(f"Connection established from {addr}")

        client_thread = threading.Thread(target=handle_client, args=(client_socket, clients, clients_socket))
        client_thread.start()

if __name__ == "__main__":
    main()
