import tcp_handler as tcp
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import imutils
import robot_logging as rl
import datetime

# initialize tcp connection to robot pi
'''
host = "192.168.0.40"
port = 5000
s = tcp.get_client(host, port)
'''

input("Press a key to continue: ")

# initialize camera
camera = PiCamera()
camera.hflip = True
camera.vflip = True
camera.resolution = (320, 240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=camera.resolution)

orange_lower = (5, 50, 50)
orange_upper = (15, 255, 255)
#orange_lower = (29, 86, 6)
#orange_upper = (64, 255, 255)

date = datetime.datetime.now().strftime("%H-%M-%S-%B-%d-%Y")
path = "sensor_tests/"
camera_file = "camera_coords_"
extension = ".csv"

def get_file_path(sensor_file):
	log_file_path = path + sensor_file + date + extension
	return log_file_path

# allow the camera to warm up
time.sleep(0.1)

start = time.time()
end = time.time()
dt_time = end - start

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
	image = frame.array

	blurred = cv2.GaussianBlur(image, (11, 11), 0) # blurs image, reducing noise

	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # turns image into hsv colour space

	mask = cv2.inRange(hsv, orange_lower, orange_upper) # mask for orange colour - returns black and white image
	mask = cv2.erode(mask, None, iterations=2) # remove noise and blobs
	mask = cv2.dilate(mask, None, iterations=2)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours from the mask
	cnts = imutils.grab_contours(cnts)
	center = None

	# only proceed if at least one contour is found
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea) # find largest contour and use it to form the circle
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if radius meets a minimum size - so it doesn't detect circles that aren't actually there
		if radius > 5:
			# draw circle to original image
			#tcp.send_data(s, "{}, {}".format(int(x), int(y)))
			print("X: {}\tY:{}".format(int(x), int(y)))
			dt_time = time.time() - start
			rl.log_camera_coords(get_file_path(camera_file), dt_time, int(x), int(y))
			#cv2.circle(image, (int(x), int(y)), int(radius), (0, 255, 255), 2)

	# display finalised image
	'''
	try:
		cv2.imshow("Ball Tracking", image)
		cv2.imshow("Mask", mask)
	except:
		pass
	'''
	key = cv2.waitKey(1) & 0xFF

	# clear the stream in preparation for next frame
	rawCapture.truncate(0)

	# if 'q' key is pressed, break from loop
	if key == ord("q"):
		break
