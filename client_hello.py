import socket
import time

host = ""  # The server's hostname or IP address
port = 49411   # The port used by the server

for i in range(5):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall("[[],[],[0.0,1.0,0.0,0.0],[]]".encode())
        data = s.recv(1024)

    print("data Recived -- >",data.decode(), " int he loop number ",i)
    time.sleep(i + 3)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall("end".encode())
        data = s.recv(1024)
print("data Recived",data.decode())



# run the server using the below command
"""
/home/pavithra/Pictures/software/blender-3.0.0-linux-x64/blender --factory-startup blend_files/plane.blend -P blender_move_plane_socket.py


"""