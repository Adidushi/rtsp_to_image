#!/usr/bin/env python

import sys, rospy
from bufferless_capture import VideoCapture
from cv_bridge import CvBridge
from sensor_msgs.msg import Image

def publish_image(url, divisor):
    pub = rospy.Publisher('/mtgr_camera', Image, queue_size=1)
    rospy.init_node('publish_image')
    rate = rospy.Rate(29.97/divisor)
    url += '&framerate={}'.format(divisor)
    vcap = VideoCapture(url)

    missed_before = False

    while not rospy.is_shutdown():
        ret, frame = vcap.read(1)
        if ret:
            image_message = CvBridge().cv2_to_imgmsg(frame, encoding="bgr8")
            pub.publish(image_message)
        else:
            if missed_before:
                rospy.logerr("Image not received! Restarting VideoCapture...")
                vcap = VideoCapture(url)
            missed_before = not missed_before
        rate.sleep()

if __name__ == '__main__':

    url = rospy.get_param("/rtsp_url")
    divisor = rospy.get_param("/fps_div")

    try:
        publish_image(url, divisor)
    except rospy.ROSInterruptException:
        pass
