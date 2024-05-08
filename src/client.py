from socket import *
import threading
import json
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import cv2
import numpy as np

clients = {}
video_complete=True
def receive_messages(client_socket, private_key):
    global clients
    global video_complete
    while True:
        data = client_socket.recv(4096)
        if not data:
            break
        data=data.decode()     
        if data[0] == "{":
            clients=json.loads(data)
            print("Connected Clients:-")
            for client in clients:
                print(client)
        elif data[0] == "#":
            client_socket.send("#".encode())
            data = client_socket.recv(4096).decode()
            print(data)
            mv=input("Enter which video u want to watch: ")
            client_socket.send(mv.encode())
            data = client_socket.recv(4096).decode()
            print(data)
            while True:
                frame_size_data = client_socket.recv(16)
                if not frame_size_data:
                    break

                frame_size = int(frame_size_data.strip())
                if frame_size == 0:
                    break

                frame_data = b''
                while len(frame_data) < frame_size:
                    remaining_bytes = frame_size - len(frame_data)
                    frame_data += client_socket.recv(remaining_bytes)

                frame_np = np.frombuffer(frame_data, dtype=np.uint8)

                frame = cv2.imdecode(frame_np, cv2.IMREAD_COLOR)
                frame = cv2.resize(frame, (1080, 720))
                cv2.imshow('Video Stream', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            cv2.destroyAllWindows()
            video_complete=True
        else:
            client_socket.send(".".encode())
            data = client_socket.recv(4096)
            decrypted_message = decrypt_message(data, private_key)
            if decrypted_message is not None:
                print(decrypted_message)

def generate_key_pair():
    key = RSA.generate(1024)
    return key

def decrypt_message(encrypted_message, private_key):
    try:
        cipher = PKCS1_OAEP.new(private_key)
        decrypted_message = cipher.decrypt(encrypted_message)
        return decrypted_message.decode()
    except ValueError as e:
        return None

def encrypt_message(public_key_str, message, client_name):
    public_key = RSA.import_key(public_key_str)
    cipher = PKCS1_OAEP.new(public_key)
    message = client_name + ": " + message
    encrypted_message = cipher.encrypt(message.encode())
    return encrypted_message

def main():
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('localhost', 9999))

    client_name = input("Enter your name: ")
    client.send(client_name.encode())
    print("Enter your public key: ")

    key_pair = generate_key_pair()
    public_key = key_pair.publickey()
    public_key_str = public_key.export_key().decode()
    print(public_key_str)
    client.send(public_key_str.encode())
    private_key = key_pair

    receive_thread = threading.Thread(target=receive_messages, args=(client, private_key))
    receive_thread.start()

    while True:
        print("\nMenu:")
        print("1. Send Message")
        print("2. Video Playback")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Available Clients:-")
            for x in clients:
                print(x)
            recipient = input("Enter recipient's name: ")
            message = input("Enter your message: ")
            encrypted_message = encrypt_message(clients[recipient], message, client_name)
            client.send(encrypted_message)
        elif choice == "2":
            client.send("VIDEO".encode())
            global video_complete
            video_complete=False
            while True:
                if video_complete:
                    break

        elif choice == "3":
            client.send("QUIT".encode())
            break

    client.close()



if __name__ == "__main__":
    main()
