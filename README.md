## Secure Socket Programming System for Communication and Video Streaming

Welcome to the Secure Socket Programming System repository. This system enables secure communication and video streaming among clients through a central server. Developed in Python, it utilizes RSA encryption for secure messaging and OpenCV for video streaming.

### Server

The server component, `server.py`, orchestrates client connections, maintains a registry of clients with their public keys, and facilitates secure communication and video streaming.

#### Features:

- **Client Management**: Prompt clients for their name and public key upon connection. Maintain a dictionary of clients and broadcast updates to all connected clients.
- **Secure Communication**: Encrypt messages using RSA encryption before broadcasting. Only the intended recipient can decrypt the message using their private key.
- **Video Streaming**: Stream video files in multiple resolutions upon client request. Distribute frames sequentially from each resolution for balanced viewing experience.

#### Dependencies:
- Python 3
- OpenCV (`cv2`)

### Client

The client component, `client.py`, establishes connections with the server, sends encrypted messages, requests video playback, and displays received messages and video frames.

#### Features:

- **Connection Establishment**: Connect to the server and provide name and public key for identification and secure communication.
- **Message Encryption**: Encrypt messages using recipient's public key before transmission for confidentiality.
- **Video Playback**: Request video streaming from the server and display frames in real-time for an immersive viewing experience.

#### Dependencies:
- Python 3
- OpenCV (`cv2`)
- pycryptodome (`Crypto`)

### Instructions for Running:

1. Ensure Python 3 is installed on your system.
2. Run the server script using `python server.py`.
3. Run the client script using `python client.py`.
4. Follow the prompts to establish connections, send messages, request video playback, and quit.

### Demo Video

For a visual demonstration of the system's capabilities, please refer to the demo video available at [[here](https://www.youtube.com/watch?v=UsuVoRccBw4&t=521s)].

### Conclusion

The Secure Socket Programming System provides a robust platform for secure communication and seamless video streaming, enhancing collaborative experiences while ensuring data privacy and integrity.