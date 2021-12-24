import cv2
import mediapipe as mp
import numpy as np


class hand_detector:
    """
    This will detect 20 points of hands in the image/video stream with the help of
    mediapipe(a build-in python package for hand tracking/detecting).
    """
    def __init__(self, static_image_mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        """
        :param static_image_mode: True or false.
        :param max_hands: My number of hands for tracking.
        :param min_detection_confidence: fraction- if detction confidence go to below 50% it will detect again.
        :param min_tracking_confidence: fraction - if tracking confidence go to below 50% it will track again

        This will initialize the basic objects for tracking and drawing hand points.
        """
        self.mp_hand = mp.solutions.hands
        self.hands = self.mp_hand.Hands(static_image_mode, max_hands, min_detection_confidence, min_tracking_confidence)
        self.draw_utils = mp.solutions.drawing_utils
        
    def detect_hand(self, img, draw_points=True):
        """
        :param img: img need to be processed.
        :param draw_points: want to draw the connection lines or not.

        Find the hand landmarks and draw the hand connection lines if 'draw_points' is true.
        """
        # change the image to RBG. It can only process the RGB images, the imag from imread is BGR.
        img_rbg = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.processed_img = self.hands.process(img_rbg)
        # print(self.processed_img.multi_hand_landmarks)

        # get the landmarks.
        self.multi_hand_landmark = self.processed_img.multi_hand_landmarks
        is_hand_detected = (self.processed_img.multi_hand_landmarks != None)

        if self.multi_hand_landmark != None:
            for landmark in self.multi_hand_landmark:
                if draw_points:
                    self.draw_utils.draw_landmarks(img, landmark,
                                               self.mp_hand.HAND_CONNECTIONS)
        return (img, is_hand_detected)

    def get_landmark_array(self, img, hand_no = 0, draw_tip = True):
        """
        :param img: Image to find the hand landmarks.
        :param hand_no: Which hand to find the landmark.
        :param draw_tip: Truw if want to draw a circle in tump tip.
        :return hand_array: numpy array having the 21 point's (x,y) value.

        Get the landmark array with all 20 point's x and y pixcels
        """
        hand_array = []
        if self.multi_hand_landmark != None:
            my_hand = self.multi_hand_landmark[hand_no]
            for id, landmark in enumerate(my_hand.landmark):
                # print(id,landmark)
                h, w, c = img.shape

                # convert it to a pixcel value, because comming landmark is a fraction of image.
                pixcel_x, pixcel_y = int(landmark.x * w), int(landmark.y * h)
                hand_array.append([id, pixcel_x, pixcel_y])

            if draw_tip:
                    cv2.circle(img, (hand_array[4][1], hand_array[4][2]), 10, (255, 0, 255), cv2.FILLED)
        #print(hand_array)
        return np.array(hand_array)

    def draw_rectangle_hand(self, img, hand_points_array, draw_rectangle=True, crop_hand=True):
        """
        
        """
        # if the hand is vertical.
        # i need 4 points to crop the hand x1,x2,y1,y2. --> y2 is the point 0's y value + 5 pixcel.

        x1,x2 = np.min(hand_points_array[:,1]) - 25,np.max(hand_points_array[:,1]) + 25
        y1,y2 = np.min(hand_points_array[:,2]) - 25,np.max(hand_points_array[:,2]) + 25
        points = [(x1,y1), (x2,y2)]
        if draw_rectangle:
            cv2.rectangle(img=img, pt1=points[0], pt2=points[1], color=(255,0,0), thickness=3)
        if crop_hand:
            hand_img = img[points[0][1]:points[1][1], points[0][0]:points[1][0]]
            return hand_img
        return img






"""vedio_capture = cv2.VideoCapture(0)

hand_detector = hand_detector(max_hands=1)
while -1:
    _,img = vedio_capture.read()

    img = hand_detector.detect_hand(img,draw_points=False)
    points_array = hand_detector.get_landmark_array(img)

    cv2.imshow("image frame",img)

    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

vedio_capture.release()
cv2.destroyAllWindows()"""

# a = [[0, 65, 454], [1, 83, 396], [2, 115, 347], [3, 153, 323], [4, 179, 315], [5, 85, 299], [6, 171, 296], [7, 171, 324], [8, 150, 336], [9, 87, 328], [10, 181, 330], [11, 173, 354], [12, 149, 360], [13, 96, 363], [14, 181, 361], [15, 172, 380], [16, 148, 385], [17, 109, 403], [18, 172, 392], [19, 162, 404], [20, 142, 409]]
# hand_detector().draw_rectangle_hand(np.array(a))