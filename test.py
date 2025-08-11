lst = [0,0,1,2,3,1,3,11,1,1,1,0,3,0,0,4]
# output - [0, 0, 0, 0, 0, 1, 2, 3, 1, 3, 11, 1, 1, 1, 3, 4]

new_lst = []
new_lst_2 = []

for i in lst:
    if i == 0:
        new_lst.append(i)
    else:
        new_lst_2.append(i)

merged_lst = new_lst + new_lst_2

print(merged_lst) 
