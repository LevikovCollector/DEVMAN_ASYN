import time
import curses
import asyncio
import random
from curses_tools import draw_frame, get_frame_size, read_controls
from itertools import cycle

def paint_star(canvas):
    row, column = (6, 20)
    symbol = '*'
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        canvas.refresh()
        time.sleep(2)
        canvas.addstr(row, column, symbol)
        canvas.refresh()
        time.sleep(0.3)
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        canvas.refresh()
        time.sleep(0.5)
        canvas.addstr(row, column, symbol)
        canvas.refresh()

async def fire(canvas, start_row, start_column, rows_speed=-0.3, columns_speed=0):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = start_row, start_column

    canvas.addstr(round(row), round(column), '*')
    await asyncio.sleep(0)

    canvas.addstr(round(row), round(column), 'O')
    await asyncio.sleep(0)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await asyncio.sleep(0)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed

async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for iteration in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for iteration in range(2):
            await asyncio.sleep(0)

        time.sleep(1)
        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for iteration in range(6):
            await asyncio.sleep(0)

async def animate_spaceship(canvas, frame_row, frame_column, frame_1, frame_2):
    draw_frame(canvas, frame_row, frame_column, frame_1)
    await asyncio.sleep(0)

    draw_frame(canvas, frame_row, frame_column, frame_1, negative=True)
    draw_frame(canvas, frame_row, frame_column, frame_2)
    await asyncio.sleep(0)

    draw_frame(canvas, frame_row, frame_column, frame_2, negative=True)
    draw_frame(canvas, frame_row, frame_column, frame_1)


def draw(canvas):
    canvas.border('|', '|')
    curses.curs_set(False)
    canvas.nodelay(True)
    max_y, max_x = canvas.getmaxyx()
    coroutines = []
    symbols_for_star = ['+', '*', '.', ':']
    start_rows = int(max_y / 2)
    start_columns =  int (max_x / 2)
    fire_coroutine = fire(canvas, start_rows,start_columns)
    with open('./frames/rocket_frame_1.txt', 'r') as frame:
        frame_1 = frame.read()
    with open('./frames/rocket_frame_2.txt', 'r') as frame:
        frame_2 = frame.read()

    spaceship = animate_spaceship(canvas, start_rows, start_columns, frame_1, frame_2)
    for star_count in range(1, 200):
        column = random.randint(1, max_x-5)
        row = random.randint(1, max_y-5)
        symbol = random.choice(symbols_for_star)
        coroutines.append(blink(canvas,row, column, symbol))

    while True:
        try:
            fire_coroutine.send(None)
            canvas.refresh()
            time.sleep(0.1)
        except StopIteration:
            break

    for coroutine in cycle(coroutines.copy()):
        try:
            spaceship.send(None)
            canvas.refresh()
        except StopIteration:
            row, column, space = read_controls(canvas)
            if row != 0 or column != 0:
                draw_frame(canvas, start_rows, start_columns, frame_1, negative=True)
            start_rows = start_rows + row
            start_columns = start_columns + column
            spaceship = animate_spaceship(canvas, start_rows, start_columns, frame_1, frame_2)
        try:
            coroutine.send(None)
            time.sleep(0.1)
        except StopIteration:
            coroutines.remove(coroutine)




if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)