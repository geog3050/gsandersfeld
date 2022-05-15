### Create a script that examines a list of numbers (for example, 2, 8, 64, 16, 32, 4) determines the second-largest number.
#
### HINT: You can use mylist.sort() function to sort the array.
#
myList = eval(input('enter a list of values for which you want to know the second largest value: '))
myList.sort() # myList is now rearranged smallest to largest
#print(myList) # for verifying that myList is now sorted smallest to largest
print(myList[-2]) # print the penultimate element in the list as that element is now the second largest