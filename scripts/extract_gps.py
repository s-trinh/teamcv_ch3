import os
import rosbag
import cv2
import csv
from cv_bridge import CvBridge, CvBridgeError
from bisect import bisect

data_dir = "/media/jokla/Elements/udacity/challeng2/"
rosbag_file = os.path.join(data_dir, "dataset.bag")
#data_dir = "."
#rosbag_file = os.path.join(data_dir, "udacity-dataset_io_vehicle_2016-10-11-13-23-02_0.bag")

gps_angle_file = os.path.join(data_dir, "gps.csv")

gps_topic = '/vehicle/gps/fix'
topics = [gps_topic]



gps_timestamps = []
gps_latitute_values = []
gps_longitude_values = []


with rosbag.Bag(rosbag_file, "r") as bag:
    for topic, msg, t in bag.read_messages(topics=topics):
        if topic == gps_topic:
            gps_timestamps.append(msg.header.stamp.to_nsec())
            gps_latitute_values.append(msg.latitude)
            gps_longitude_values.append(msg.longitude)

# make sure timestamps are in ascending chronological order
def assert_sorted(l):
    assert all(l[i] <= l[i+1] for i in xrange(len(l)-1))

assert_sorted(gps_timestamps)


with open(gps_angle_file, "w") as angles_file:
    fieldnames = ["timestamp", "latitude","longitude"]
    writer = csv.DictWriter(angles_file, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(0,len(gps_timestamps)):
        writer.writerow({"timestamp": gps_timestamps[i],
                         "latitude": gps_latitute_values[i],
                         "longitude": gps_longitude_values[i]})
