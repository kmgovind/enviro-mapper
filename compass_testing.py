from time import sleep
from compass import return_heading

def main():
    while(True):
        print(return_heading())
        sleep(0.5)

if __name__ == '__main__':
    main()