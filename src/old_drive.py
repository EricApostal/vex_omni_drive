from vex import *
# C:\Users\ehapo\AppData\Roaming\Code\User\globalStorage\vexrobotics.vexcode\sdk\python

# Brain should be defined by default
brain = Brain()

# define controller (you're welcome ik lol)
controller = Controller()

# define motors
front_left_motor = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
back_left_motor = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)

front_right_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, True)
back_right_motor = Motor(Ports.PORT12, GearSetting.RATIO_18_1, True)

# define motor groups
left_motorgroup = MotorGroup(front_left_motor, back_left_motor)
right_motorgroup = MotorGroup(front_right_motor, back_right_motor)

bot = DriveTrain(lm = left_motorgroup, rm = right_motorgroup)

# main thread
while True:
    bot.set_drive_velocity(controller.axis3.position(), units = VelocityUnits.PERCENT)
    bot.drive(FORWARD)

    bot.set_turn_velocity(controller.axis1.position(), units = VelocityUnits.PERCENT)
    bot.turn(LEFT)
    