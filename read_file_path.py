import os, sys

def main ( path ):
    for i in os.walk(path) :
        print(i[0])

if __name__ == "__main__":
   # for test
   #path = r'C:\Users\hongw\OneDrive\for_install'
    main(sys.argv[1])
