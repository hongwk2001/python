def crossout(table,row,col):
    for rpos in  range (len(table)):
        table[rpos] = table[rpos][:col] + table[rpos][col+1:]
    
    tbl1 = table [:row]
    tbl2 =table[row:]
    table = table [:row] + table[row:]

table = [[0.1,0.3,0.5],[0.6,0.2,0.7],[1.5,2.3,0.4]]

crossout(table,1,2)