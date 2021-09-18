#!/usr/bin/env python3

import math
import time

import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

do = ''
direction = ''

def deepsort_pose(msg):
    global do, direction
    x, y, size = msg.split(',')
    if size > 30:
        do = 'stop'
    elif size < 15:
        do = 'fast_forward'
    else:
        do = 'forward'
    if x > 60:
        direction = 'right'
    elif x < 40:
        direction = 'left'
    else:
        direction = 'none'
    print(do, direction)



def move_to_goal(speed, relative_angle_degree, distance):
    velocity_message = Twist()
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0
    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    angular_speed = math.radians(5)

    loop_rate = rospy.Rate(10)  # we publish the velocity at 10 Hz (10 times a second)
    cmd_vel_topic = '/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True:
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1 - t0) * 5
        loop_rate.sleep()

        if (current_angle_degree > relative_angle_degree):
            velocity_message.angular.z = 0
            break

    t0 = time.time()

    while True:
        rospy.loginfo("Turtlebot move forward")
        velocity_message.linear.x = speed
        velocity_publisher.publish(velocity_message)

        loop_rate.sleep()
        t1 = time.time()

        distance_moved = (t1 - t0) * speed

        if not (distance_moved < distance):
            rospy.loginfo("reached")
            break

    velocity_message.angular.z = 0
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


def move_to_goal(speed, relative_angle_degree, distance):
    velocity_message = Twist()
    velocity_message.linear.x = 0
    velocity_message.linear.y = 0
    velocity_message.linear.z = 0
    velocity_message.angular.x = 0
    velocity_message.angular.y = 0
    velocity_message.angular.z = 0

    angular_speed = math.radians(5)

    loop_rate = rospy.Rate(10)  # we publish the velocity at 10 Hz (10 times a second)
    cmd_vel_topic = '/cmd_vel'
    velocity_publisher = rospy.Publisher(cmd_vel_topic, Twist, queue_size=10)

    t0 = rospy.Time.now().to_sec()

    while True:
        velocity_message.angular.z = angular_speed
        velocity_publisher.publish(velocity_message)

        t1 = rospy.Time.now().to_sec()
        current_angle_degree = (t1 - t0) * 5
        loop_rate.sleep()

        if (current_angle_degree > relative_angle_degree):
            velocity_message.angular.z = 0
            break

    t0 = time.time()

    while True:
        rospy.loginfo("Turtlebot move forward")
        velocity_message.linear.x = speed
        velocity_publisher.publish(velocity_message)

        loop_rate.sleep()
        t1 = time.time()

        distance_moved = (t1 - t0) * speed

        if not (distance_moved < distance):
            rospy.loginfo("reached")
            break

    velocity_message.angular.z = 0
    velocity_message.linear.x = 0
    velocity_publisher.publish(velocity_message)


if __name__ == '__main__':
    try:
        rospy.init_node('turtlebot_move_to_goal', anonymous=True)
        listener = rospy.Subscriber('/odom', Odometry, print_pose)
        deepsort_listener = rospy.Subscriber('/deepsort_position_topic', Odometry, deepsort_pose)
        time.sleep(1.0)
        move_to_goal(0.1, 90, 2)
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
