import cv2
import socket 

# define the blender server host and port
host = ""  # The server's hostname or IP address
port = 49411 

# start the video capture.
video_capture = cv2.VideoCapture(0)

# check the video capture is opened.
if not video_capture.isOpened():
    raise Exception("Could not open video device")
# set the video frame width adn height.
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 1280)
video_capture.set(cv2.CAP_PROP_FPS, 25)

while True:
    ret, frame = video_capture.read()
    # things wnat to happen in the loop. 1) get the vertex input 
    print(frame.shape)

    # change the frame size.
    frame = cv2.resize(frame, (1000,500), interpolation = cv2.INTER_AREA)
    print(frame.shape)

    # getting that image from the blender.
    # call the blender with the blend file and blend script.
    print("calling the blender")
    # define a client to communicate with blender server.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall("[[],[],[0.0,1.0,0.0,0.0],[]]".encode())
        data = s.recv(1024)
    # print("return code", return_code)
    # if return_code == 0: # if 0 means no errors.
        # if 0, then the image from the blender is saved in this folder ... we can overlay that image to frame.
    blender_plane_img = cv2.imread("img.jpg")
        # print(blender_plane_img.shape) --> (100,100,3)
    frame[0:500,0:500] = blender_plane_img

    cv2.namedWindow('resized window', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('resized window', 1000,500)
    cv2.imshow("resized window", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        # end the blender server.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host, port))
            s.sendall("end".encode())
            data = s.recv(1024)
        break
  
# After the loop release the cap object
video_capture.release()
# Destroy all the windows
cv2.destroyAllWindows
