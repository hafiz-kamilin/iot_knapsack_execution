#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
[Smart Tomato Farm Problem]

    Tomato farm is divided into 10 areas which have it own exclusive sprinkler (1 area 1 sprinkler). We
    assume the sprinkler can freely adjust the irrigation area based on the sprinkler head. now
    the problem is the water tank can only support 40 L/min of total irrigation output.
    In other words we can't execute the all sprinklers at the same time...

    #####################
    # 0 # 1 # 2 # 3 # 4 #
    #####################   Area partition
    # 5 # 6 # 7 # 8 # 9 #
    #####################

    To solve this problem, we will imagine our sprinkler execution sequence as a knapsack problem.
    1. Imagine sprinkler output specification and (output specification)/cost as item weight and value
    2. Imagine supported water tank output as knapsack weight limit
    3. Based on the knapsack weight limit, find the item(s) to be included. Minus selected items with 
       the number of area partition. This will be our first round of executions.
    4. Repeat step 3 for the second, third and so on for the execution round until the number of area
       partition is 0.

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

# function to calculate the total value for the carried actuators
def total_value(actuators, specification_limit):

    # return the total value for the carried actuators
    return  sum([x[2] for x in actuators]) if sum([x[1] for x in actuators]) < specification_limit else 0

# function to perform the recursive dynamic programming algorithm to get the result
def solve(actuators, specification_limit):

    # if there is no more actuators
    if not actuators:
        
        # return empty tuple
        return ()

    # if the actuators and max weight are not in cache
    if (actuators, specification_limit) not in cache:

        # load the first item into head
        head = actuators[0]
        # load the rest of actuators into tail
        tail = actuators[1:]
        # TODO: supplementary study https://www.youtube.com/watch?v=xOlhR_2QCXY
        include = (head,) + solve(tail, specification_limit - head[1])
        dont_include = solve(tail, specification_limit)
        # if the total value and weight for the head is bigger than total value and weight for the tail 
        if total_value(include, specification_limit) > total_value(dont_include, specification_limit):

            # the answer is head
            answer = include

        else:

            # the answer is tail
            answer = dont_include
        
        # load the answer into the cache
        cache[(actuators, specification_limit)] = answer
    
    # return the cache
    return cache[(actuators, specification_limit)]

# initiator
if __name__ == '__main__':

    # actuator limit
    specification_limit = 40
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

    ##############################################################

    # initialize counter
    counter = 0
    # initialize solution
    solution = []

    # as long there is remaining partition
    while (farm_partition != 0):

        print ("\nROUND %s\n" %(counter + 1))
        # compute the result
        result = list(solve(actuators, specification_limit))
        # show the list of actuators that need to be carried
        print ("Selected actuators:")

        # for every actuator listed in the result
        for x in result:

            # as long there is remaining partition
            if (farm_partition != 0):

                # decrease by 1
                farm_partition -= 1
                # show only the item name
                print ("→ " + x[0])

            else:

                # remove the excess element
                result.remove(x)

        # save the result into a solution
        solution.insert(counter, result)
        # compute the total value
        print ("value:", total_value(solution[counter], specification_limit))
        # compute the total output
        print ("output:", sum([x[1] for x in solution[counter]]))
        # convert the tuple into a list
        actuators = list(actuators)

        # for every actuator listed in the solution
        for x in solution[counter]:

            # remove it from the listed actuators
            actuators.remove(x)

        # convert the list back into a tuple
        actuators = tuple(actuators)
        # increase the counter
        counter += 1

    print ("\nAggregated solution:\n")

    # for every actuator listed in the solution
    for x in solution:

        # remove it from the listed actuators
        print (x)