import time
import curses
import asyncio
import random

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

async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for iteration in range(3):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for iteration in range(2):
            await asyncio.sleep(0)


        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for iteration in range(6):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border('|', '|')
    curses.curs_set(False)
    #paint_star(canvas)
    max_y, max_x = canvas.getmaxyx()
    coroutines = []
    symbols_for_star = ['+', '*', '.', ':']
    for star_count in range(1, 500):
        column = random.randint(1, max_x-5)
        row = random.randint(1, max_y-5)
        symbol = random.choice(symbols_for_star)
        coroutines.append(blink(canvas,row, column, symbol))

    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
                time.sleep(0.1)
            except StopIteration:
                coroutines.remove(coroutine)
        if len(coroutines)== 0:
            break



if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)