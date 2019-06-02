#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
import sys
import select
import termios
import tty

commands = {
    'q': 'str',
    'w': 'str',
    't': 'test'
}


def getKey():
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    key = sys.stdin.read(1)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key

def shutdown():
    rospy.loginfo("Stop Talker")
    rospy.sleep(1)


if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)
    pub = rospy.Publisher('chatter', String, queue_size=1)
    rospy.init_node('talker', anonymous=True)
    rospy.on_shutdown(shutdown)
    rate = rospy.Rate(10) # 10hz
    
    while not rospy.is_shutdown():
        key = getKey()
        if key in commands.keys():
            cmd = commands[key]
        else:
            cmd = 'nothing'
        print(cmd)
        pub.publish(cmd)
        rate.sleep()
