import sys
sys.path.append("/raspberrypi/rpi-rgb-led-matrix/bindings/python/samples")
from raspberrypi\rpi-rgb-led-matrix\bindings\python\samples\samplebase import SampleBase
from rgbmatrix import graphics
import time
import random


class SnakeGame(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SnakeGame, self).__init__(*args, **kwargs)

    def run(self):
        while true:
            canvas = self.matrix
            font = graphics.Font()
            font.LoadFont("../../../fonts/7x13.bdf")

            red = graphics.Color(255, 0, 0)
            graphics.DrawLine(canvas, 5, 5, 22, 13, red)

            green = graphics.Color(0, 255, 0)
            graphics.DrawCircle(canvas, 15, 15, 10, green)

            blue = graphics.Color(0, 0, 255)
            graphics.DrawText(canvas, font, 2, 10, blue, "snake")

            time.sleep(0.1)  


# Main function
if __name__ == "__main__":
    snake_game = SnakeGame()
    if (not snake_game.process()):
        snake_game.print_help()
