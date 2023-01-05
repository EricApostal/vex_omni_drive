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

conveyer_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)

# define motor groups

class omnidrive:
    def __init__(self, frontleft_motor, backleft_motor, frontright_motor, backright_motor, velocity_percent = 100) -> None:
        self.front_left_motor = frontleft_motor
        self.back_left_motor = backleft_motor
        self.front_right_motor = frontright_motor
        self.back_right_motor = backright_motor
    
    def move(self, controllerobj):
        x = -1 * controllerobj.axis4.position()
        y = -1 * controllerobj.axis3.position()
        rx = controllerobj.axis1.position()

        multiplier = 1.5

        self.front_left_motor.spin(FORWARD, (y + x + (rx*2)) * multiplier, PERCENT)
        self.back_left_motor.spin(FORWARD, (y - x + (rx*2)) * multiplier, PERCENT )
        self.front_right_motor.spin(FORWARD, (y - x - (rx*2)) * multiplier, PERCENT )
        self.back_right_motor.spin(FORWARD, (y + x - (rx*2)) * multiplier, PERCENT)

        

bot = omnidrive(front_left_motor, back_left_motor, front_right_motor, back_right_motor)        

# main thread
while True:
    bot.move(controller)
    conveyer_motor.spin(FORWARD, 200, PERCENT)
    sleep(10)
