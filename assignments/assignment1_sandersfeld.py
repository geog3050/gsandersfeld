######################################################################
# Edit the following function definition, replacing the words
# 'name' with your name and 'hawkid' with your hawkid.
#
# Note: Your hawkid is the login name you use to access ICON, and NOT
# your firstname-lastname@uiowa.edu email address.
#
# def hawkid():
#     return(["Caglar Koylu", "ckoylu"])
######################################################################
def hawkid():
    return(["Graham Sandersfeld", "gsandersfeld"])

######################################################################
# DON'T MAKE ANY CHANGES HERE.
if (not hawkid()[0] or not hawkid()[1]) or (hawkid()[1] == "hawkid"):
    print('### Error: YOU MUST provide your hawkid in the hawkid() function.')
    print('### Otherwise, the Autograder will assign 0 points.')
    exit(-1)
else:
    info = hawkid()
    print(info[0])
    print(info[1])
######################################################################

######################################################################
# Problem 1 - Getting Input - (8 Points)
#
# Specification: You are expected to ask for three main inputs:
#     1. mode: This input will be a string given by the user to determine
#              the calculation method. Valid inputs are 'min', 'max', 'avg'.
#     2. count: This input will be an integer given by the user to indicate
#               how many more inputs/values are expected to be given. These
#               new values will be added to a list to be used later in the
#               calculations.
#     3. values: These inputs will be floats. You are expected to read user
#                input 'count' times to get all the values. All of the values
#                should be stored in a list to be used later.
#
# What is expected?
#     After you get all the inputs from the user, print the following information
#     in order:
#           - Print 'mode' variable value (1 Point)
#           - Print 'count' variable value (1 Point)
#           - Print length of the list you have just created (1 Point)
#           - Print the list you have just created (5 Points)
#     All of the prints should be in separate print statements. Please, don't
#     forget that the order is very important.
#
# Note: Don't forget that input() function returns a string, not a number
#       even though you give a number as an input. Therefore, be careful
#       about data type conversions.
#
# Example Input/Output:
#     Assume that you are given the following inputs:
#       avg
#       4
#       123
#       14234
#       25435
#       14
#
#     Your solution for Problem 1 should print the following:
#       Caglar Koylu (Your name will be here)
#       ckoylu (Your hawkid will be here)
#       avg
#       4
#       4
#       [123.0, 14234.0, 25435.0, 14.0]
######################################################################


# WRITE YOUR SOLUTION FOR PROBLEM 1 HERE.

# ask for input mode 
myMode = str(input('Which statistic would you like to find? (min, max, or avg): '))
#if (not(myMode == 'min' or myMode == 'max' or myMode == 'avg')):
#    myMode = input('Cannot find that statistic. Choose min, max, or avg: ')

# ask for input count
myCount = int(input('Enter the number of observations or values in your dataset: '))
#if isinstance(myCount, int) == 'False': 
#    myCount = (input('Number of observations must be an integer: '))
#print(type(myCount))

# ask for input list of values 
myList = [] # [] make a list called myList
#remainingObs = myCount
print('Enter the values with a return after each value: ')
for i in range(0,myCount):
    entryInput = float(input())
    myList = myList + [entryInput,] # append the list myList

# recall list methods and mutability

print(hawkid()[0]) #
print(hawkid()[1]) # print elements of hawkid
print(myMode) # print the desired statistic
print(myCount) # print the no. of obs. 
print(len(myList)) # print the length of the list
print(myList) # print the list of obs.

######################################################################
# Problem 2 - Find the Minimum/Maximum/Average - (12 Points)
#
# Specification: In this part of the homework, you are expected to compute
# a value for the given 'mode'. Therefore, your code has to have three main
# code blocks:
#     1. Finding Minimum: If the value of 'mode' is 'min', find the minimum
#                         element in the list. Then, print its value.
#     2. Finding Maximum: If the value of 'mode' is 'max', find the maximum
#                         element in the list. Then, print its value.
#     3. Finding Average: If the value of 'mode' is 'avg', compute the average
#                         of all elements in the list. Computation is basically:
#                               (Sum of all elements)/(Number of elements)
#
# Note: BE CAREFUL. YOU CANNOT USE ANY LIBRARIES OR PYTHON'S BUILT-IN
#       min, max, sum operations. You are expected to implement these operations
#       by your own. Such an use of those functions are not allowed and may cause
#       you loose points.
#
# Hint: These three code blocks depend on the value of 'mode'. Therefore,
#       using a conditional branches may help you to perform different
#       operations in different code blocks. Also, in order to traverse
#       over each element in the list one by one iteration concepts can
#       be very helpful.
#
# Example Input/Output:
#     Assume that you are given the following inputs:
#       avg
#       4
#       123
#       14234
#       25435
#       14
#
#     Your solution for Problem 1 & 2 should print the following:
#       Caglar Koylu (Your name will be here)
#       ckoylu (Your hawkid will be here)
#       avg
#       4
#       4
#       [123.0, 14234.0, 25435.0, 14.0]
#       9951.5
######################################################################


# WRITE YOUR SOLUTION FOR PROBLEM 2 HERE.

# avg
if myMode == 'avg':
    myTotal = 0
    for x in range(0,myCount): # iterate through list and sum
        myTotal += myList[x]
    myAvg = myTotal / myCount
    print(myAvg)

# min
if myMode == 'min':
    initialMin = myList[0]
    for y in range(0, myCount):
        if myList[y] < initialMin:
            initialMin = myList[y]
    myMin = initialMin
    print(myMin)

#def isLessThan(obs1, obs2):
#    if obs1 <= obs2:
#if myMode == 'min':

# max
if myMode == 'max':
    initialMax = myList[0]
    for z in range(0, myCount):
        if myList[z] > initialMax:
            initialMax = myList[z]
    myMax = initialMax
    print(myMax)

######################################################################