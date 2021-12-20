import bpy
import socket

def print_hello():
    print("hello  hi :)")
    
host = ""
port = 49411

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    
    while True:
        print("The server listernig on all host and port",port)
        s.listen()
        conn, add = s.accept()
        with conn:
            print("connected by", add)
            data_from_client = conn.recv(1024).decode() # recieved data also byte --> so meed decoding here
            if data_from_client == 'do_process': 
                print_hello()
                conn.send("success".encode()) # sending value should be byte--> so needed to be encoded
            elif data_from_client == 'end':
                print("Ending the blender server connection")
                conn.send("Connection Ended".encode())
                break
            
        