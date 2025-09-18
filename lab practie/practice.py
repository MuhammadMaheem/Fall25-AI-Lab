# string1 = "Kuch,Bhi:Kuch?Bhi!"

# not_allowed = set("~`!@#$%^&*()_+-={}[]|\:;'\"<>?/,.")


# for i in string1:
#     if i in not_allowed:
#         string1 = string1.replace(i , " ")
#     print(string1)

















# # sort teh string


# string1 = "I am Rasikh"
# x = []
# x = [ord(ch) for ch in string1 ]
# print(x)
# for i in range(len(x)):
#     secd = x[i]  
#     for j in range(i+1, len(x)):   
#         if x[j] < secd:
#             print(x[j], "<", secd)





string1 = "I am Rasikh"
x = [ord(ch) for ch in string1]

sorted_list = []
for val in x:  
    count = 0
    while count < len(sorted_list) and sorted_list[count] <val:
        count +=1
        print(count)

    sorted_list.insert(count,val)
    print(sorted_list)


assi_code = [chr(ch) for (ch) in sorted_list]
print(assi_code)








# card_num = input("Enter your card number: ")
# sum1 = 0
# for i in range(len(card_num)-1, -1, -1):
#     print(i)
#     digit = int(card_num[i])
#     print(digit)
#     if (len(card_num) - i) % 2 == 0:
#         digit *= 2
#         if digit > 9:
#             digit -= 9
#     sum1 += digit
# if sum1 % 10 == 0:
#     print("Valid card number")
# else:
#     print("Invalid card number")





card_num = list(input("Enter your card number: "))
sum1 = 0
last_digit = card_num.pop()
print(last_digit)
print(card_num)
reversed_num = card_num[::-1]
print(reversed_num)
new_list = []
for i in range(len(reversed_num)):
    if i % 2 == 0:
        new_list.append(int(reversed_num[i]) * 2)
    else:
        new_list.append(int(reversed_num[i]))
print(new_list)
for i in new_list:
    if i > 9:
        i -= 9
    sum1 += i
print(sum1)
sum1 += int(last_digit)
if sum1 % 10 == 0:
    print("Valid card number")
else:
    print("Invalid card number")

