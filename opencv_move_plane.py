import cv2
import subprocess

# start the video capture.
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    # things wnat to happen in the loop. 1) get the vertex input 
    # print(frame.shape)

    # getting that image from the blender.
    # call the blender with the blend file and blend script.
    print("calling the blender")
    return_code = subprocess.run(['/home/pavithra/Pictures/software/blender-3.0.0-linux-x64/blender',
                             '--factory-startup',
                             'blend_files/plane.blend',
                             '-b',
                             '-P',
                             'move_plane_userInput.py',
                             '--',
                             '--value=[[1.0,0.0,0.0],[],[],[1.0,1.0,1.0]]'])
    # print("return code", return_code)
    # if return_code == 0: # if 0 means no errors.
        # if 0, then the image from the blender is saved in this folder ... we can overlay that image to frame.
    blender_plane_img = cv2.imread("img.jpg")
        # print(blender_plane_img.shape) --> (100,100,3)
    frame[0:100,0:100] = blender_plane_img
    cv2.imshow("Original Video", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
video_capture.release()
# Destroy all the windows
cv2.destroyAllWindows
