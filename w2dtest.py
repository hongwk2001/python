
arr=[['a','b'],['c','d'] ]
rows, cols=2,2
narr= list(list())
print(narr)

for i in range(rows):
    col=[]
    for j in range(cols):
        col.append(arr[i][j])
    narr.append(col)
print(narr)

for i in range(rows):
    for j in range(cols):
        narr[j][i] = arr[i][j]
print(narr)

for i in range(rows):
    for j in range(cols):
        arr[i][j] = narr[i][j]
print(arr)
