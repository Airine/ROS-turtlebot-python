#!/usr/bin/env python

'''
Copyright (c) 2019, Aaron Tian
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from math import radians

mms = None

# curr_cmd_idx = 0 # Current command index
moving = False
move_state = 0 # 0: stand, 1: go_circle, 2: cxk, 3: tri, 4:rotate
moves = []
times = []
# 0: stand, 1: go_circle, 2: cxk_left, 3: cxk_right, 3: tri_move, 4: tri_turn, 5: rotate
        # for i in range(times(0)):
            # while rospy.is_shutdown():
            #     mms.cmd_vel.publish(moves[0])
            #     mms.r.sleep()

class Movements():
    
    def __init__(self):
        rospy.init_node('Movements', anonymous=False)
        rospy.Subscriber('chatter', String, self.callback)
        # rospy.loginfo("To stop TurtleBot CTRL + C")
        rospy.on_shutdown(self.shutdown)
        self.cmd_vel = rospy.Publisher('cmd_vel_mux/input/navi', Twist, queue_size=10)
        self.r = rospy.Rate(10) # 10Hz = 0.1s
        rospy.spin()
        rospy.loginfo("Start Running")
        while not rospy.is_shutdown():
            if not moving:
                self.cmd_vel.publish(moves[move_state])
                r. sleep()
            else:
                if move_state == 1:
                    for i in range(0, times[1]):
                        self.cmd_vel.publish(moves[1])
                        r.sleep()
                elif move_state == 2:
                    for i in range(0, 30):
                        for j in range(0, times[2]):
                            self.cmd_vel.publish(moves[2])
                            r.sleep()
                        for k in range(0, times[3]):
                            self.cmd_vel.publish(moves[3])
                            r.sleep()
                # if move_state == 3:
                moving = False
        # rospy.spin()

    def init_cmds():
        stand_cmd = Twist()
        stand_cmd.linear.x = 0
        stand_cmd.angular.z = 0
        moves.append(circle_cmd)
        times.append(0)

        circle_cmd = Twist()
        circle_cmd.linear.x = 0.2
        circle_cmd.angular.z = 0.5
        moves.append(circle_cmd)
        times.append(30)

        cxk_left = Twist()
        cxk_left.linear.x = 0
        cxk_left.angular.z = 1
        moves.append(cxk_left)
        times.append(2)

        cxk_right = Twist()
        cxk_right.linear.x = 0
        cxk_right.angular.z = -1
        moves.append(cxk_right)
        times.append(2)
        
        tri_move = Twist()
        tri_move.linear.x = 0.2
        moves.append(tri_move)
        times.append(10)

        tri_turn = Twist()
        tri_turn.linear.x = 0
        tri_turn.angular.z = radians(60)
        moves.append(tri_turn)
        times.append(20)

        rotate_cmd = Twist()
        rotate_cmd.linear.x = 0
        rotate_cmd.angular.z = 0.5 # radians/s
        moves.append(rotate_cmd)
        times.append(20)

    def shutdown(self):
        rospy.loginfo("Stop TurtleBot")
        self.cmd_vel.publish(Twist())
        rospy.sleep(1)

    def callback(self, data):
        rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
        if data.data == 'test':
            moving = True
            move_state = 1

if __name__ == "__main__":
    try:
        mms = Movements()
    except:
        rospy.loginfo("Movements node terminated.")