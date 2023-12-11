"""
RoCS Client SDK - Robot Module

The `robot` module in the RoCS (Robot Control System) Client SDK provides classes and functionality
for interacting with humanoid robots. It includes components for controlling robot movements, accessing
sensory data, and managing robot actions.

Classes:
    - Human: Class representing a humanoid robot.
    - Car: Class representing a robot with car-like functionalities.
    - Mod: Class representing the modular features of a car robot.

Enums:
    - Motor: Enum defining motor-related options.
    - ArmAction: Enum defining actions related to robot arms.
    - HandAction: Enum defining actions related to robot hands.

Usage:
    from rocs_client.robot import Human, Car, Mod, Motor, ArmAction, HandAction

    # Creating an instance of the Human class
    human_robot = Human()

    # Creating an instance of the Car class
    car_robot = Car()

    # Creating an instance of the Mod class
    modular_robot = Mod()

    # Accessing Motor enum options
    motor_option = Motor.SOME_OPTION

    # Accessing ArmAction enum options
    arm_action_option = ArmAction.SOME_ACTION

    # Accessing HandAction enum options
    hand_action_option = HandAction.SOME_ACTION
"""

from .car import Car
from .human import Human
from .robot_base import RobotBase