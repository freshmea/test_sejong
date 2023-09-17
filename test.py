import RPi.GPIO as g
import time

g.setmode(g.BCM)
g.setup(21, g.OUT)

for i in range(20):
    g.output(21, True)
    time.sleep(0.5)
    g.output(21, False)
    time.sleep(0.5)
