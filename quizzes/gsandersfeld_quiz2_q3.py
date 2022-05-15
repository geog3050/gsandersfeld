### Create a script that examines a list of numbers 
### (for example, 2, 8, 64, 16, 32, 4, 16, 8) to determine whether it contains duplicates. 
### The script should print a meaningful result, such as “The list provided contains duplicate values” or 
### “The list provided does not contain duplicate values.” An optional addition is to remove the duplicates from the list.
#
### HINT: You can use list.count(value) to determine how many occurrences of a value exists in a list. 
#
myList = eval(input('enter a list of values for which you want to check for duplicates: '))
dupFlag = 'False'
for i in range(0,len(myList)):
    if myList.count(myList[i]) > 1:
        dupFlag = 'True'
    #print(myList.count(myList[i]))
if dupFlag == 'True':
    print('The list contains duplicate values.')
    myListNoDup = list(set(myList))
    print('A new version of the list without duplicates will print below:')
    print(myListNoDup)
else:
    print('The list does not contain duplicate values.')
    print(myList)