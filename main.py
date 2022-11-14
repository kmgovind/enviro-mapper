from random import randrange

from compass import return_heading
from constants import *
from drivetrain import *
from ultrasonic import get_all_distance, setup_ultrasonic
from WallTracker import WallTracker


def main():
    setup_ultrasonic()
    setup_dt()
    wall_tracker = WallTracker()

    while True:
        ultrasonic_result = get_all_distance()
        center_distance = ultrasonic_result['center']
        if center_distance < COLLISION_THRESHOLD:
            turn_deg = randrange(LOWER_TURN_LIMIT, HIGHER_TURN_LIMIT+1)
            turn_to(turn_deg)
            wall_tracker.take_reading_turn(turn_deg)
        else:
            drive_forward(FORWARD_STEP_CM)
            wall_tracker.take_reading_move_forward(FORWARD_STEP_CM)

        wall_tracker.export_results('results.json')

    close_pins()


if __name__ == '__main__':
    main()
