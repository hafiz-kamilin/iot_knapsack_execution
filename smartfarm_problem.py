#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[Smart Tomato Farm Problem]

    Tomato farm is divided into 10 areas which have it own exclusive sprinkler (1 area 1 sprinkler). We
    assume the sprinkler can freely adjust the irrigation area based on the sprinkler head. now
    the problem is the water tank can only support 40 L/min of total irrigation output (in 
    other words we can't execute the all sprinklers at the same time), and there is 
    a list of sprinklers to be choosen from. How to simplify this problems?

    #####################
    # 0 # 1 # 2 # 3 # 4 #
    #####################   Area partition
    # 5 # 6 # 7 # 8 # 9 #
    #####################

    To solve this problem, we will imagine our sprinkler execution sequence as a knapsack problem.

        1. Imagine sprinkler output specification and (output specification)/cost as item weight
           and value.
        2. Imagine supported water tank output as knapsack weight limit.
        3. Based on the knapsack weight limit, find the item(s) that need to be included and
           minus selected items with the number of area partition. This will be our first
           round of executions.
        4. Repeat step 3 for the second, third and so on for the execution round until the
           number of area partition is 0.

    From the hard coded sprinklers selection, we will get;

        ROUND 1: [('sprinkler_01', 10, 5), ('sprinkler_02', 10, 5), ('sprinkler_07', 9, 2), ('sprinkler_16', 10, 5)]
        ROUND 2: [('sprinkler_05', 13, 4), ('sprinkler_11', 13, 3), ('sprinkler_19', 13, 6)]
        ROUND 3: [('sprinkler_03', 20, 6), ('sprinkler_20', 18, 3)]
        ROUND 4: [('sprinkler_15', 15, 3)]

    which mean, this program choose the best value versus specification we can get and at the same time
    it arrange the sprinklers order of execution to abide the water tank output specification.

"""
# cache to memoize (memoization) the result 
cache = {}

# function to calculate the total value for the listed devices
def total_value(listed_devices, system_cap):

    # return the total value for the listed devices
    return  sum([x[2] for x in listed_devices]) if sum([x[1] for x in listed_devices]) < system_cap else 0

# function to perform the recursive dynamic programming algorithm to get the result
def solve_knapsack(listed_devices, system_cap):

    # if there is no more listed devices
    if not listed_devices:
        
        # return empty tuple
        return ()

    # if the listed devices and system cap are not in cache
    if (listed_devices, system_cap) not in cache:

        # load the first item into head
        head = listed_devices[0]
        # load the rest of listed devices into tail
        tail = listed_devices[1:]
        # TODO: supplementary study https://www.youtube.com/watch?v=xOlhR_2QCXY
        include = (head,) + solve_knapsack(tail, system_cap - head[1])
        dont_include = solve_knapsack(tail, system_cap)
        # if the total value and weight for the head is bigger than total value and weight for the tail 
        if total_value(include, system_cap) > total_value(dont_include, system_cap):

            # the answer is head
            answer = include

        else:

            # the answer is tail
            answer = dont_include
        
        # load the answer into the cache
        cache[(listed_devices, system_cap)] = answer
    
    # return the cache
    return cache[(listed_devices, system_cap)]

# function to sequence the choosen devices based on the system cap
def sequencing_order(listed_devices, required_devices, system_cap):

    # initialize counter
    counter = 0
    # initialize output
    output = []

    # as long there is remaining devices
    while (required_devices != 0):

        print ("\nKnapsack solution %s\n" %(counter + 1))
        # compute the result
        result = list(solve_knapsack(listed_devices, system_cap))
        # show the list of device that need to be carried
        print ("Selected device:")

        # for every devices listed in the result
        for x in result:

            # as long there is remaining required devices
            if (required_devices != 0):

                # decrease by 1
                required_devices -= 1
                # show only the item name
                print (" → " + x[0])

            else:

                # remove the excess element
                result.remove(x)

        # save the result into the output
        output.insert(counter, result)
        # compute the total value
        print ("Value:", total_value(output[counter], system_cap))
        # compute the total output
        print ("Output:", sum([x[1] for x in output[counter]]))
        # convert the tuple into a list
        listed_devices = list(listed_devices)

        # for every actuator listed in the output
        for x in output[counter]:

            # remove it from the listed devices
            listed_devices.remove(x)

        # convert the list back into a tuple
        listed_devices = tuple(listed_devices)
        # increase the counter
        counter += 1

    # return the output
    return output

# initiator
if __name__ == '__main__':

    # actuator limit
    watertank_output = 40
    # number of farm partition
    farm_partition = 10
    # list of actuators (name, specification, specification/cost)
    actuators = (
                ("sprinkler_01", 10, 5), ("sprinkler_02", 10, 5),
                ("sprinkler_03", 20, 6), ("sprinkler_04", 15, 1),
                ("sprinkler_05", 13, 4), ("sprinkler_06", 14, 3),
                ("sprinkler_07",  9, 2), ("sprinkler_08", 20, 5),
                ("sprinkler_09", 23, 3), ("sprinkler_10", 25, 5),
                ("sprinkler_11", 13, 3), ("sprinkler_12", 16, 2),
                ("sprinkler_13", 10, 1), ("sprinkler_14", 30, 2),
                ("sprinkler_15", 15, 3), ("sprinkler_16", 10, 5), 
                ("sprinkler_17", 23, 5), ("sprinkler_18", 22, 4),
                ("sprinkler_19", 13, 6), ("sprinkler_20", 18, 3),
    )
    print ("\n10 actuators are choosen from list and the execution order is automated")
    print ("while adhering the 40 L/min water tank limit based on knapsack problem.")

    ##############################################################

    # initialize counter
    counter = 0
    # compute the solution
    solution = sequencing_order(actuators, farm_partition, watertank_output)
    # show the solution in aggregated way
    print ("\nAggregated actuators sequence:\n")

    # for every actuator listed in the solution
    for x in solution:

        # print it for every round
        print ("Step %i: %s" %(counter + 1, x))
        # increase the counter
        counter += 1