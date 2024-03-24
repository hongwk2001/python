import traceback, sys

def main(*args):
    try:
        if len(args) ==1 :
            pass
        else:
            print('error')
            exit ()
    except Exception as e:
        print('exception')
        traceback.print_exc(file=sys.stdout)

main()