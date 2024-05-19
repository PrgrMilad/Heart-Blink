from machine import Pin
import time

# Define constants
ANIMDELAY = 100
INTENSITYMIN = 0  # Minimum brightness (0-15)
INTENSITYMAX = 8  # Maximum brightness (0-15)

# Define pin connections
DIN_PIN = 15
CS_PIN = 5
CLK_PIN = 0

# MAX7219 registers
MAXREG_DECODEMODE = 0x09
MAXREG_INTENSITY = 0x0a
MAXREG_SCANLIMIT = 0x0b
MAXREG_SHUTDOWN = 0x0c
MAXREG_DISPTEST = 0x0f

# Heart pattern as a bytearray
heart = bytearray([
    0b00110011,
    0b11111111,
    0b11111111,
    0b11111111,
    0b00111111,
    0b00011110,
    0b00001100,
    0b00000000
])


def setup():
    global din, cs, clk  # Declare pins as global

    # Initialize pins as output
    din = Pin(DIN_PIN, Pin.OUT)
    clk = Pin(CLK_PIN, Pin.OUT)
    cs = Pin(CS_PIN, Pin.OUT)

    # Initialize MAX7219
    set_registry(MAXREG_SCANLIMIT, 0x07)
    set_registry(MAXREG_DECODEMODE, 0x00)  # Using LED matrix
    set_registry(MAXREG_SHUTDOWN, 0x01)  # Not in shutdown mode
    set_registry(MAXREG_DISPTEST, 0x00)  # No display test
    set_registry(MAXREG_INTENSITY, INTENSITYMIN)  # Initial intensity

    # Draw heart
    for i in range(1, 9):
        set_registry(i, heart[i - 1])


def loop():
    global INTENSITYMAX, INTENSITYMIN  # Declare variables as global

    # Second beat - high intensity
    set_registry(MAXREG_INTENSITY, INTENSITYMAX)
    time.sleep_ms(ANIMDELAY)

    # Switch off
    set_registry(MAXREG_INTENSITY, INTENSITYMIN)
    time.sleep_ms(ANIMDELAY)

    # Second beat - high intensity
    set_registry(MAXREG_INTENSITY, INTENSITYMAX)
    time.sleep_ms(ANIMDELAY)

    # Switch off
    set_registry(MAXREG_INTENSITY, INTENSITYMIN)
    time.sleep_ms(ANIMDELAY * 6)


def set_registry(reg, value):
    global cs  # Declare CS pin as global

    cs.value(0)

    # Send register and data using bytearray for efficiency
    data = bytearray([reg, value])
    for byte in data:
        send_byte(byte)

    cs.value(1)


def send_byte(data):
    for i in range(7, -1, -1):
        mask = 1 << i
        clk.value(0)
        if data & mask:
            din.value(1)
        else:
            din.value(0)
        clk.value(1)


setup()
while True:
    loop()
