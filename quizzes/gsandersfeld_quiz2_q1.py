### Create a script that examines a string for the occurrence of a particular letter. If the letter occurs in the text (for example, the letter Z), the string “Yes” should be printed to the Interactive Window. If the letter does not occur in the text, the string “No” should be printed.
#
### HINT: You can use input() function to create a list:
#
### mystr = input('enter a string:')
#
myStr = input('enter a string: ')
myLetter = input('choose one letter to be searched for in the string. If contained in the string, "Yes" will print, and if not, "No": ')
#n = len(myStr)
letterFound = 0
for i in range(0, len(myStr)):
    #if myStr[i] == myLetter: # case-sensitive
    if myStr[i].upper() == myLetter or myStr[i].lower() == myLetter: # not case-sensitive
        letterFound = 'True'
if letterFound == 'True':
    print('Yes')
else:
    print('No')