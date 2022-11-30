#!/usr/bin/env python3

"""
This is the main entry point for the particle filter exercise node. It
subscribes to laser, map, and odometry and creates an instance of
pf.PFLocaliser() to do the localisation.
"""


import rospy
import random
from std_msgs.msg import String
import numpy as np

class OrderModelNode(object):

    def __init__(self):
        print("hellow world")
        try:
            self.orderModel(5)
        except rospy.ROSInterruptException:
            print("error rospy intrrupt exception")
            pass
    # order simulation model #TODO this is probably a different node
    # will need to listen to the frequency model and add them to a queue
    def orderModel (self, numberOfTables):
        pub = rospy.Publisher('order', String, queue_size=100)
        # defined demand phases high medium and low
        HIGH = 1 # every factor of 1
        MEDIUM = 2 # every factor of 2
        LOW = 3 # every factor of 3
        
        Q = [] #queue of orders
        
        queueAmount = numberOfTables - 1

        #TODO set timeout between tables

        while True:

            orderFrequency = random.randint(1,3)
            if orderFrequency == 1:
                orderFrequency = HIGH
            elif orderFrequency == 2:
                orderFrequency = MEDIUM
            elif orderFrequency == 3:
                orderFrequency = LOW
            
            print("switching to demand phade: ", orderFrequency)
            x = 10 # suggested number of orders for each phase
            # randomly change order frequency every x orders with noise
            numberOfOrders = np.random.normal(x, 0.5*x)

            for i in range (0, int(numberOfOrders)):
                # randomly generate order
                
                while 1:
                    print("Q : ", Q)
                    table = random.randint(1, numberOfTables)
                    if table not in Q:
                        break
                if len(Q)<queueAmount-1:
                    Q.append(table)
                    
                elif Q and len(Q) == queueAmount-1:
                    for j in range(0,queueAmount-2):
                        Q[j] = Q[j+1]
                    Q[queueAmount-2] = table
                                                    
                order = 'T' + str(table) + " "+ "D"+ str(orderFrequency)
                # publish order

                print("Order for table " + str(table) + " is " + str(order))
                data = String()
                data.data = order
                pub.publish(data)
                #distribution centered around centered around the frequency  
                rospy.sleep(np.random.normal(orderFrequency, 0.5 * orderFrequency))
                

            
        # send order message to waiter robot system

# main method
if __name__ == '__main__':
    # --- Main Program ---
    rospy.init_node('order_model_node')
    node = OrderModelNode()
    rospy.spin()
