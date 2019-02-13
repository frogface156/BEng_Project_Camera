from imutils.video import VideoStream
import numpy as np
import cv2
import imutils
import time


orange_lower = (29, 86, 6) # change values to see orange
orange_upper = (64, 255, 255)

vs = VideoStream(usePiCamera=True).start()
print("Warming camera up...")
time.sleep(2.0) # let's camera warm up...

while True:

	frame = vs.read() # get current frame
	frame = frame[1] # '1' is the actual frame, '0' is whether a frame was received

	frame = imutils.resize(frame, width=600) # resizes image - allows faster processing - will use this with KF for even faster, targeted computer vision
	blurred = cv2.GaussianBlur(frame, (11, 11), 0) # reduces noise and allows focus on the ball

	hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) # turns image into hsv colour space

	mask = cv2.inRange(hsv, orange_lower, orange_upper) # mask for orange colour - returns black and white image of the orange regions
	mask = cv2.erode(mask, None, iterations=2) # remove noise and blobs
	mask = cv2.dilate(mask, None, iterations=2) # remove noise and blobs

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # find contours from the mask
	cnts = imutils.grab_contours(cnts)
	center = None

	# only proceed if at least one contour was found
	if len(cnts) > 0:
		c = max(cnts, key=cv2.contourArea) # find largest contour and use it to form the circle
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size - so it doesn't detect circles that aren't actually the ball
		if radius > 10:
			# draw the circle and centroid on the frame,
			# then update the list of tracked points
			cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
			cv2.circle(frame, center, 5, (0, 0, 255), -1)

	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

vs.release()
cv2.destroyAllWindows()
