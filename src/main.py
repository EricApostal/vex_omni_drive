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

conveyer_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)

flywheel_motor = Motor(Ports.PORT17, GearSetting.RATIO_6_1, False)
flywheel_motor_2 = Motor(Ports.PORT15, GearSetting.RATIO_6_1, True)

pusher_motor = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)

# flywheel_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

# define motor groups

class omnidrive:
    def __init__(self, frontleft_motor, backleft_motor, frontright_motor, backright_motor, velocity_percent = 100) -> None:
        self.front_left_motor = frontleft_motor
        self.back_left_motor = backleft_motor
        self.front_right_motor = frontright_motor
        self.back_right_motor = backright_motor

        self.intake_running = False
        self.flywheel_running = False

        self.pusher_moving_right = False
        self.pusher_moving_left = False
    
    def toggle_intake(self):
        self.intake_running = not self.intake_running

    def toggle_flywheel(self):
        self.flywheel_running = not self.flywheel_running

    def toggle_pusher_left(self):

        # so we can automatically stop it from moving right
        if not self.pusher_moving_left:
            self.pusher_moving_right = False
        
        self.pusher_moving_left = not self.pusher_moving_left

    def toggle_pusher_right(self):

        # so we can automatically stop it from moving left
        if not self.pusher_moving_right:
            # we know that it will move left as this function exits
            self.pusher_moving_left = False
        
        self.pusher_moving_right = not self.pusher_moving_right

    def move(self, controllerobj):
        x = -1 * controllerobj.axis4.position()
        y = -1 * controllerobj.axis3.position()
        rx = controllerobj.axis1.position()

        multiplier = 1.5
        turn_speed_multiplier = 1.5
        # print("---")
        # print( rx**turn_speed_multiplier )
        # print("---")
        self.front_left_motor.spin(FORWARD, (y + x + (rx*turn_speed_multiplier)) * multiplier, PERCENT)
        self.back_left_motor.spin(FORWARD, (y - x + (rx*turn_speed_multiplier)) * multiplier, PERCENT )
        self.front_right_motor.spin(FORWARD, (y - x - (rx*turn_speed_multiplier)) * multiplier, PERCENT )
        self.back_right_motor.spin(FORWARD, (y + x - (rx*turn_speed_multiplier)) * multiplier, PERCENT)

bot = omnidrive(front_left_motor, back_left_motor, front_right_motor, back_right_motor)       


# main thread


controller.buttonUp.pressed(bot.toggle_intake)
controller.buttonRight.pressed(bot.toggle_flywheel)

controller.buttonL1.pressed(bot.toggle_pusher_left)
controller.buttonR1.pressed(bot.toggle_pusher_right)

# controller.buttonUp.released(lambda: toggle_intake() )

while True:
    # start omni movement
    bot.move(controller)

    # controller.buttonUp.pressed(lambda: toggle_intake() )
    
    # toggle intake
    if bot.intake_running:
        conveyer_motor.spin(FORWARD, 200, PERCENT)
    else:
        conveyer_motor.stop()

    if bot.flywheel_running:
        flywheel_motor.spin(FORWARD, 1000, PERCENT)
        flywheel_motor_2.spin(FORWARD, 1000, PERCENT)
    else:
        flywheel_motor_2.stop()
        flywheel_motor.stop()

    if bot.pusher_moving_right:
        pusher_motor.spin(FORWARD, 100, PERCENT)

    if bot.pusher_moving_left:
        pusher_motor.spin(REVERSE, 100, PERCENT)
    # pusher_motor.spin(FORWARD, 25, PERCENT)
    
    if not bot.pusher_moving_right and not bot.pusher_moving_left:
        pusher_motor.stop()

    sleep(10)