from ultrasonic import get_all_distance,setup_ultrasonic

from time import sleep

def main():
    setup_ultrasonic()
    while(True):
        ultraResult = get_all_distance()
        print(ultraResult)
        sleep(0.5)

if __name__ == '__main__':
    main()