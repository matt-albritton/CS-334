#!/usr/bin/env python
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions

import time
import random


class SnakeGame(SampleBase):
    def __init__(self, *args, **kwargs):
        super(SnakeGame, self).__init__(*args, **kwargs)
        options = RGBMatrixOptions()
        options.rows = 64
        options.cols = 64
        matrix = RGBMatrix(options = options)

    def run(self):
        while True:
            canvas = self.matrix
            font = graphics.Font()
            font.LoadFont("../raspberrypi/rpi-rgb-led-matrix/fonts/7x13.bdf")

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
