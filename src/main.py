from vex import *
# C:\Users\ehapo\AppData\Roaming\Code\User\globalStorage\vexrobotics.vexcode\sdk\python

# Brain should be defined by default
brain = Brain()

# define controller (you're welcome ik lol)
controller = Controller()

# define motors
front_left_motor = Motor(Ports.PORT2, GearSetting.RATIO_6_1, False)
back_left_motor = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)

front_right_motor = Motor(Ports.PORT4, GearSetting.RATIO_6_1, True)
back_right_motor = Motor(Ports.PORT3, GearSetting.RATIO_6_1, True)

conveyer_motor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)

flywheel_motor = Motor(Ports.PORT17, GearSetting.RATIO_6_1, False)
flywheel_motor_2 = Motor(Ports.PORT15, GearSetting.RATIO_6_1, True)

pusher_motor = Motor(Ports.PORT16, GearSetting.RATIO_18_1, False)

inertial_sensor = Inertial(Ports.PORT2)
roller_sensor = Optical(Ports.PORT3)

# flywheel_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

# define motor groups

class omnidrive:
    def __init__(self, frontleft_motor, backleft_motor, frontright_motor, backright_motor, conveyer_motor, flywheel_motors, velocity_percent = 100, flywheel_speed = 40) -> None:
        self.front_left_motor = frontleft_motor
        self.back_left_motor = backleft_motor
        self.front_right_motor = frontright_motor
        self.back_right_motor = backright_motor
        self.conveyer_motor = conveyer_motor
        self.flywheel_motors = flywheel_motors

        self.intake_running = False
        self.flywheel_running = False

        self.pusher_moving_right = False
        self.pusher_moving_left = False

        self.is_pushing = False
        self.is_unwinding = False

        self.is_rotating_roller = False

        self.flywheel_motor_speed = flywheel_speed # percent

        self.is_auto = False
    
    def tick(self):
        # do omni movement based on current controller positions
        if not self.is_auto:
            self.move(controller)

        # handle if the intake is running or if the roller is running
        if self.intake_running or self.is_rotating_roller:
            self.conveyer_motor.spin(FORWARD, 200, PERCENT)
        elif self.is_unwinding:
            self.conveyer_motor.spin(REVERSE, 200, PERCENT)
        else:
            self.conveyer_motor.stop()

        if self.pusher_moving_right:
            pusher_motor.spin(FORWARD, 100, PERCENT)

            # print('[RIGHT] Pusher power usage =')
            # print(pusher_motor.power())

        if self.pusher_moving_left:
            pusher_motor.spin(REVERSE, 100, PERCENT)
        
        if controller.buttonR2.pressing():
            self.fire_disk()

        if not self.pusher_moving_right and not self.pusher_moving_left:
            pusher_motor.stop()


        if self.flywheel_running:
            for motor in self.flywheel_motors:
                motor.spin(FORWARD, self.flywheel_motor_speed, PERCENT)
                motor.spin(FORWARD, self.flywheel_motor_speed, PERCENT)
        else:
            for motor in self.flywheel_motors:
                motor.stop()


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

    def stop_pusher(self):
        # so I can handle wattage stuff :D

        self.pusher_moving_left = False
        self.pusher_moving_right = False


    def fire_disk_thread(self):
        self.is_pushing = True
        # the actual code for firing a disk
        self.toggle_pusher_right()
        sleep(360)
        self.toggle_pusher_left()
        sleep(380)
        self.stop_pusher()
        self.is_pushing = False

    def fire_disk(self):
        if not self.is_pushing:
            fire_disk_thread = Thread(self.fire_disk_thread)

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

    def manual_move(self, direction: DirectionType.DirectionType, motor_power: int):
        self.front_left_motor.spin(direction, motor_power, PERCENT)
        self.back_left_motor.spin(direction, motor_power, PERCENT )
        self.front_right_motor.spin(direction, motor_power, PERCENT )
        self.back_right_motor.spin(direction, motor_power, PERCENT)

    def strafe(self, direction: str, motor_power: int):
        self.front_left_motor.spin(FORWARD, motor_power, PERCENT)
        self.back_left_motor.spin(REVERSE, motor_power, PERCENT )
        self.front_right_motor.spin(REVERSE, motor_power, PERCENT )
        self.back_right_motor.spin(FORWARD, motor_power, PERCENT)

    def stop_drivetrain(self):
        self.back_left_motor.stop()
        self.back_right_motor.stop()
        self.front_right_motor.stop()
        self.front_left_motor.stop()

    def rotate(self, deg, speed=100):

        self.front_left_motor.spin(FORWARD, speed, PERCENT)
        self.back_left_motor.spin(FORWARD, speed, PERCENT )
        self.front_right_motor.spin(FORWARD, speed * -1, PERCENT )
        self.back_right_motor.spin(FORWARD, speed * -1, PERCENT)

        sleep( int( (deg*5.2)/(speed/100) ) )

        self.back_left_motor.stop()
        self.back_right_motor.stop()
        self.front_right_motor.stop()
        self.front_left_motor.stop()

    def toggle_unwind_string(self):
        self.intake_running = False
        self.is_unwinding = not self.is_unwinding

    def get_roller_color(self):
        current_color = None
        hue = int( roller_sensor.hue() )
        print(hue)
        if (hue > 10) and (hue < 50):
            current_color = "blue" 
        elif (hue > 60):
            current_color = "red"
        else:
            print("invalid hue")
            current_color = 0

        return current_color

    def score_roller(self, team_color):
        """
        Spins the roller to either "red" or "blue".
        If you are on team blue, you want to pass "blue"
        """
        if not ((team_color == "red") or (team_color == "blue")):
            NameError( "Team color \"" + str(team_color) + " does not exist! (use \"red\" or \"blue\")" )

        # so we can record the state and resume it once we have finished rolling
        # might be a bad idea though, it could keep moving even once stopped if the intake is toggled on
        # intake_state = self.intake_running

        # more promising approach
        self.intake_running = False

        current_color = None
        print("switching")
        while not (current_color == team_color):
            self.conveyer_motor.spin(FORWARD, 200, PERCENT)
            self.manual_move(REVERSE, 25)
            current_color = self.get_roller_color()
            self.is_rotating_roller = True
            print(current_color)
            
            sleep(10)

        self.is_rotating_roller = False
        self.stop_drivetrain()
        self.conveyer_motor.stop()

        print("should be switched")


bot = omnidrive(front_left_motor, back_left_motor, front_right_motor, back_right_motor, conveyer_motor, [flywheel_motor, flywheel_motor_2], flywheel_speed=55)       

# controller function bindings
controller.buttonUp.pressed(bot.toggle_intake)
controller.buttonRight.pressed(bot.toggle_flywheel)
controller.buttonX.pressed(bot.toggle_unwind_string)
# controller.buttonL1.pressed(bot.toggle_pusher_left)
# controller.buttonR1.pressed(bot.toggle_pusher_right)

# controller.buttonR2.pressing()
# main thread
print("starting drive thread!")

def init_inertial():
    print("starting inertial calibration")
    inertial_sensor.calibrate()
    print("calibrated")
    # inertial_sensor.set_heading(90)

init_inertial()


def manual():
    bot.is_auto = False
    bot.flywheel_motor_speed = 40
    while True:
        bot.tick()
        sleep(10)

def tick_thread():
    while True:
        bot.tick()
        sleep(10)

def auto():
    bot.is_auto = True
    bot.flywheel_motor_speed = 25
    
    # bot.score_roller("red")
    # flywheel_thread = Thread(bot.auto_flywheel_thread) 
    perisistant_ticks = Thread(tick_thread)

    # bot.manual_move(REVERSE, 25)
    # sleep(500)
    # bot.intake_running = True
    # sleep(3000)
    # bot.intake_running = False

    # sleep(250)

    bot.strafe('right', 25)
    bot.flywheel_running = True
    sleep(2000)
    bot.stop_drivetrain()
    print("drivetrain stopped")
    bot.rotate(100, speed=25)
    bot.manual_move(FORWARD, 100)
    sleep(400)
    bot.stop_drivetrain()
    
    for i in range(4):
        bot.fire_disk()
        sleep(1000)

    bot.is_auto = False
    bot.flywheel_running = False



# manual()
# debug()
# bot.score_roller("red")
# USE THIS IN PROD!
Competition(manual, auto)
# auto()