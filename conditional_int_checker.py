Number_to_check = int(input("Please give a number to check: "))
if Number_to_check % 2 == 1 or Number_to_check < 0: #Check for Odd number and Negative number
    print("Weird!\n")
elif Number_to_check % 2 == 0 and 2 <= Number_to_check <= 5: #Check for Even number and 2<=number<=5
    print("Not weird!\n")
elif Number_to_check % 2 == 0 and 6 <= Number_to_check <= 20: #Check for Even number and 6<=number<=20
    print("Weird!\n")
elif Number_to_check % 2 == 0 and 20 < Number_to_check: #Check for Even number and 20<=number
    print("Not weird!\n")