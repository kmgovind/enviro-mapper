from drivetrain import turn_to,setup_dt
from time import sleep

def main():
    setup_dt()
    while True:
        turn_to(90)
        sleep(1)

if __name__ == '__main__':
    main()