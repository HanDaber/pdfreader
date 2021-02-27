import sys

def main(*args):
    print("Query for Jobs")
    print(" ".join(args))
    return "ok"

if __name__ == '__main__':
    main(sys.argv)