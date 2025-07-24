from vex import *
from math import atan2, degrees


def izvedi_pot(drivetrain, pot):
    prev = pot[0]
    angle = 0
    for pt in pot[1:]:
        new_angle = atan2(pt.y - prev.y, pt.x - prev.x)
        if new_angle > angle:
            drivetrain.turn_for(LEFT, degrees(new_angle - angle), DEGREES)
        else:
            drivetrain.turn_for(RIGHT, degrees(angle - new_angle), DEGREES)
        angle = new_angle
        drivetrain.drive_for(FORWARD, abs(pt-prev), MM)
        prev = pt
