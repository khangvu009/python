# print("My name is: Minh Khang Vu")
# print("I'm 15 years old")

# firstname = "Minh Khang"
# lastname = " Vu"
# fullname = firstname + lastname
# number = 0

# print(fullname)

# def Is_prime(n):
#     if (n == 0 or n == 1):
#         return False
#     for i in range (2,int(math.sqrt(n))+1):
#         if n % i == 0:
#             return False
#     return True

# for i in range (100):
#     if Is_prime(i):
#         number += i
    
# print(number)

# num = int(input("input integer: "))
# flag = True

# while flag:
#     if Is_prime(num):
#         flag = False
#     num -= 1 
# print(num+1)

# food = input("what did you eat yesterday: ")
# print("Yesterday I ate " + food + " delicious")

# str = input("input number: ")
# number = 0
# length = len(str)

# for i in range (0,length):
#     number = number * 10 + (ord(str[i]) - ord('0'))
#     print(number)

# print(number + 5)

# mylist = []

# number_elements = int(input("ammount: "))
# for i in range (number_elements):
#     temp = input("input element:")
#     mylist.append(temp)
# newlist = []

# for i in range (0,len(mylist)):    
#     newlist.append({mylist[i]:ord(mylist[i])})
# print(newlist)

# A = []
# Is_Unique = []
# unique = []

# number_elements = int(input("ammount: "))
# for i in range (number_elements):
#     temp = int(input("input element:"))
#     A.append(temp)

# index = 0

# for i in  range (0,len(A)):
#     flag = True
#     if len(Is_Unique) == 0:
#         Is_Unique.append(A[i])
#     for j in range (0,len(Is_Unique)):
#         print(A[i])
#         if A[i] == Is_Unique[j]:
#             flag = False
#             break
#     if flag == False:
#         Is_Unique.append(A[i])
# for item in A:
#     flag = True
#     for j in range (0,len(Is_Unique)):
#         if (item == Is_Unique[j]):
#             flag = False
#     if flag == True:
#         unique.append(item)
# print(unique)

# def Is_Curzon(n):
#     if (2**n+1) % (2*n+1) == 0:
#         return True
#     return False

# n = int(input("input number: "))

# result = Is_Curzon(n)

# if result == True:
#     print(True)
# else :
#     print (False)
# A = []

# def Find_Max(index, number):
#     if index == len(A):
#         return number
#     number = max(number, A[index])
#     return Find_Max(index + 1, number)

# number_elements = int(input("Amount: "))
# for i in range(number_elements):
#     temp = int(input("Input element: "))
#     A.append(temp)
# result = Find_Max(0, A[0])
# print("The maximum number is:", result)

# def Caesar_Cypher_convert (str,n):
#     result = ""
#     for i in range (len(str)):
#         result += chr(ord(str[i])+n)    
#     return result

# str = input("input string: ")
# Nshift = int(input("input amount of letter to shift: "))
# result = Caesar_Cypher_convert(str,Nshift)

# print(result)

# password = "Admin123"
# code = input("Enter the password: ")

# run = True

# while run:
#     code = input("Enter the password: ")
#     if code == password: run = False
# print("correct")

# def plus(a, b):
#     c = []
#     temp = 0
    
#     # Ensure a is the larger list
#     if len(a) < len(b):
#         a, b = b, a
    
#     # Pad the shorter list with zeros at the beginning
#     b = [0] * (len(a) - len(b)) + b
    
#     # Perform addition from the end to the beginning
#     for i in range(len(a) - 1, -1, -1):
#         number = a[i] + b[i] + temp
#         temp = number // 10
#         c.append(number % 10)
    
#     # If there's a remaining carry, add it to the result
#     if temp > 0:
#         c.append(temp)
    
#     # The result is currently reversed, so reverse it back
#     c.reverse()
#     return c

# def multiply(a, b):
#     result = [0] * (len(a) + len(b))
    
#     for i in range(len(a) - 1, -1, -1):
#         carry = 0
#         for j in range(len(b) - 1, -1, -1):
#             temp = a[i] * b[j] + result[i + j + 1] + carry
#             carry = temp // 10
#             result[i + j + 1] = temp % 10
        
#         result[i + j] += carry
    
#     # Remove leading zeros
#     while len(result) > 1 and result[0] == 0:
#         result.pop(0)
    
#     return result

# # Convert an integer to a list of its digits
# def int_to_list(n):
#     return [int(x) for x in str(n)]

# # Main code to calculate factorial
# n = int(input("Enter the factorial you want: "))

# a = [1]

# for i in range(2, n + 1):
#     a = multiply(a, int_to_list(i))

# # Print the result as a number
# print("Factorial:", ''.join(map(str, a)))

for i in range (10,0,-1):
    print(i)