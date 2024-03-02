from flask import Flask, render_template, redirect, url_for
import socket
import pickle
import cv2
import os

class OperatorSocket:
    BUFF_SIZE = 65536
    HEADERSIZE = 10
    HOST = '127.0.0.1'  # the IP address of the model server
    PORT = 4001  # the port number used by the model server
    fps, st, frames_to_count, cnt = (0, 0, 20, 0)
    frames = []

    # def __init__(self):

    def set_dir_path(self):
        # Get the full path of the current file
        self.file_path = os.path.abspath(__file__)

        # Get the directory name of the current file
        self.dir_name = os.path.dirname(self.file_path)
        # path_out = f'{dir_name}/operator-server-frames/'
        self.path_out = f'{self.dir_name}/static/operator-server-frames'

        # return path_out

    def create_socket_and_bind_it_to_model(self):
        # (self.HOST, self.PORT) - the values that used by the model server.
        self.socket_address = (self.HOST, self.PORT)
        # print(f"(self.HOST, self.PORT) = {(self.HOST, self.PORT)}")


        # Create a socket object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.BUFF_SIZE)

        # establishes the connection with the model server
        # connect() - The socket connects to the specified socket_address
        self.sock.connect(self.socket_address)
        # Bind the socket to a specific address and port
        # sock.bind(socket_address)

        # Send data to the model server
        data = b'Hello from operator server'
        print(f":: data = {data}")
        self.sock.sendto(data, self.socket_address)


        print("::: FINISH create_socket_and_bind_it_to_model()")


# frames = get_frames_from_model_server(sock)
    def get_frames_from_model_server(self):
        self.frames = []


        while True:
            # Receive response from the model server
            packet, _ = self.sock.recvfrom(self.BUFF_SIZE)
            frame_id, encoded_frame = pickle.loads(packet[self.HEADERSIZE:])

            print(f"frame_id ={frame_id}")

            if 'FINISH' in frame_id:
                print("Close the socket connection")
                # self.sock.close()
                print(f"len(frames = {len(self.frames)})")
                return

            decoded_frame = cv2.imdecode(encoded_frame, cv2.IMREAD_COLOR)
            frame = cv2.putText(decoded_frame, ":".join(frame_id.split("-")[3:]),
                                (10, 40),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                (0, 0, 255),
                                2)
            self.set_dir_path() # self.path_out
            # self.full_path = os.path.join(self.path_out, frame_id)
            full_frame_location = f'{self.path_out}/{frame_id}.jpg'
            cv2.imwrite(full_frame_location, frame)

            print(f"full_frame_location = {full_frame_location}")
            self.frames.append(frame)
            print("::: finish get_frames_from_model_server()")

        