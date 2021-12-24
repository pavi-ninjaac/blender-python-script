import cv2
import socket 

from hand_detector import hand_detector

# define the blender server host and port
host = ""  # The server's hostname or IP address
port = 49411 

# start the video capture.
video_capture = cv2.VideoCapture(0)
hand_detector_obj = hand_detector(max_hands=1)

def get_vertext_value(vertext_value_list):
    """
    Convert the actual (x,y) value to 500,500 tracking area (x,y) values.( convert the pixcel image value to blender point value)
    """


while True:
    ret, frame = video_capture.read()
    # print(frame.shape)

    # change the frame size.
    frame = cv2.resize(frame, (1280,720), interpolation = cv2.INTER_AREA)
    # print(frame.shape)

    img, is_hand_detected = hand_detector_obj.detect_hand(frame,draw_points=False)
    if is_hand_detected:
        points_array = hand_detector_obj.get_landmark_array(img, draw_tip = False)
        # do tracking when the index finger is up. ( Index finger id in mediapipe is 8)
        if points_array[8][2] < points_array[6][2]:
            # Draw the index finger tip for tracking.
            print("Tracking.....")
            cv2.circle(img, (points_array[8][1], points_array[8][2]), 10, (255,0,0), cv2.FILLED)

            # call the blender with the blend file and blend script.
            print("calling the blender")
            vertex_value = get_vertext_value([[],[float(points_array[8][1]), float(points_array[8][2]), 0.0],[],[]]) # should be like [[x,y,z],[],[],[]]
            
            print(vertex_value, "vertex point got")
            # define a client to communicate with blender server.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                s.sendall(str(vertex_value).encode())
                data = s.recv(1024)

            blender_plane_img = cv2.imread("img.jpg")
            frame[0:500,0:500] = blender_plane_img

        else:
            print("do nothing")

    

    cv2.imshow("resized window", img)

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
