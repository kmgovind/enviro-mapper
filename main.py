from WallTracker import WallTracker
from drivetrain import drive_forward,turn_to
from ultrasonic import get_all_distance, setup_ultrasonic
from compass import return_heading
from constants import *
from random import randrange

def main():
    setup_ultrasonic()
    wall_tracker = WallTracker()

    while True:
        ultrasonic_result = get_all_distance()
        center_distance = ultrasonic_result['center']
        if center_distance > COLLISION_THRESHOLD:
            turn_deg = randrange(LOWER_TURN_LIMIT,HIGHER_TURN_LIMIT+1)
            turn_to(turn_deg)
            wall_tracker.take_reading_turn(turn_deg)
        else:
            drive_forward(FORWARD_STEP_CM)
            wall_tracker.take_reading_move_forward(FORWARD_STEP_CM)
        
        wall_tracker.export_results('results.json')



if __name__ == '__main__':
    main()