#import __init__
import temp, os

print('called main')

file=os.path.split(__file__)
print(file)

parent=os.path.split(__file__)[0]
print(parent)
fpath  = os.path.join(parent,'minimums.csv')
print(fpath)

DWcsv=os.path.split('./recon/dir1/dir2/DW.csv')
print(DWcsv)

print( os.path.join ('..', 'recon', 'dir','dir','file') )
print( os.path.join ('.', 'recon', 'dir','dir','file') )

