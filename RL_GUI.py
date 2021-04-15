import tkinter as tk

def get_max_reward(terminal_states):
    max_reward = float('-inf')

    for state in terminal_states:
        if state[2] > max_reward:
            max_reward = state[2]

    return max_reward


def get_max_punishment(terminal_states):
    max_punishment = float('inf')

    for state in terminal_states:
        if state[2] < max_punishment:
            max_punishment = state[2]

    return max_punishment

def is_terminal_state(terminal_states, row, col):
    terminal = False

    for state in terminal_states:
        if state[0] == row and state[1] == col:
            terminal = True

    return terminal


def draw_board(window, grid, iterations, terminal_states, boulder_states, rows, cols, maxReward, maxPunishment):
    max_reward = maxReward
    max_punishment = maxPunishment

    canvas_width = 1000  # Width of the window
    canvas_height = 600  # Length of the window
    window.geometry('%dx%d+%d+%d' % (canvas_width, canvas_height, 0, 0))
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height,
                       background='black')  # Create a black background

    edge_dist = 10  # Distance of the board to the edge of the window
    bottom_space = 100  # Distance from the bottom of the board to the bottom of the window
    small_rect_diff = 0.1 * min(canvas_width / cols, (canvas_height - bottom_space) / rows)  # For terminal states, distance from outside rectangle to inside rectangle

    for row in range(rows):  # Loop through the rows of the grid
        for col in range(cols):  # Loop through the columns of the grid
            if [row, col] not in boulder_states:  # If it's not a boulder state
                x1 = edge_dist + col * ((canvas_width - 2 * edge_dist) / cols)  # Top left x coordinate of the rectangle
                # y1 = edge_dist + row * (
                #             (canvas_height - edge_dist - bottom_space) / rows)  # Top left y coordinate of the rectangle
                y1 = edge_dist + (rows - row - 1) * ((canvas_height - edge_dist - bottom_space) / rows)
                x2 = x1 + ((canvas_width - 2 * edge_dist) / cols)  # Bottom right x coordinate of the rectangle
                # y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)  # Bottom right y coordinate of the rectangle
                y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)
                
                if is_terminal_state(terminal_states, row , col):  # If this cell is a terminal state
                    value = grid[row][col][0][0]
                    if value > 0:  # Best value is positive, so draw the rectangle in green
                        canvas.create_rectangle(x1, y1, x2, y2, outline='white',
                                                fill='#%02x%02x%02x' % (0, int(200 * min(value / max_reward, max_reward)), 0))  # Draw the rectangle of this cell
                    else:  # Best value is negative, so draw the rectangle in red
                        canvas.create_rectangle(x1, y1, x2, y2, outline='white',
                                                fill='#%02x%02x%02x' % (int(200 * min(value / max_punishment, -1 * max_punishment)), 0, 0))  # Draw the rectangle of this cell

                    x1 = x1 + small_rect_diff
                    y1 = y1 + small_rect_diff
                    x2 = x2 - small_rect_diff
                    y2 = y2 - small_rect_diff
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white')  # Draw a smaller rectangle inside
                    canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(round(grid[row][col][0][0], 2)),
                                       font=(
                                           'TkDefaultFont', int(0.25 * ((canvas_width - 2 * edge_dist) / cols))),
                                       fill='white')  # Print the best value in the middle of the cell
                else:
                    actions = grid[row][col]  # Get the value of this cell
                    #print(row, col, actions)
                    for value in actions:
                        if value[0] >= 0:  # Best value is positive, so draw the rectangle in green
                            color = (0, int(200 * min(value[0] / max_reward, max_reward)), 0)
                        else:  # Best value is negative, so draw the rectangle in red
                            color = (int(200 * min(value[0] / max_punishment, -1 * max_punishment)), 0,
                                     0)  # Draw the rectangle of this cell

                        mid_x = (x1 + x2) / 2
                        mid_y = (y1 + y2) / 2
                        # print(color, value[0], value[0] / max_punishment, -1 * max_punishment)
                        if value[1] == '↑':  # Draw an up arrow
                            triangle_points = [mid_x, mid_y, x1, y1, x2, y1]
                            canvas.create_polygon(triangle_points, outline='white', fill='#%02x%02x%02x' % color)
                            canvas.create_text((x1 + x2) / 2, y1 + (y2 - y1) / 5, text=str(round(value[0], 2)),
                                               font=(
                                               'TkDefaultFont', int(0.15 * ((canvas_width - 2 * edge_dist) / cols))),
                                               fill='white')  # Print the best value in the middle of the cell
                        elif value[1] == '↓':  # Draw a down arrow
                            triangle_points = [mid_x, mid_y, x1, y2, x2, y2]
                            canvas.create_polygon(triangle_points, outline='white', fill='#%02x%02x%02x' % color)
                            canvas.create_text((x1 + x2) / 2, y2 - (y2 - y1) / 5, text=str(round(value[0], 2)),
                                               font=(
                                                   'TkDefaultFont', int(0.15 * ((canvas_width - 2 * edge_dist) / cols))),
                                               fill='white')  # Print the best value in the middle of the cell
                        elif value[1] == '←':  # Draw a left arrow
                            triangle_points = [mid_x, mid_y, x1, y1, x1, y2]
                            canvas.create_polygon(triangle_points, outline='white', fill='#%02x%02x%02x' % color)
                            canvas.create_text(x1 + (x2 - x1) / 5, (y1 + y2) / 2, text=str(round(value[0], 2)),
                                               font=(
                                               'TkDefaultFont', int(0.15 * ((canvas_width - 2 * edge_dist) / cols))),
                                               fill='white')  # Print the best value in the middle of the cell
                        elif value[1] == '→':  # Draw a right arrow
                            triangle_points = [mid_x, mid_y, x2, y1, x2, y2]
                            canvas.create_polygon(triangle_points, outline='white', fill='#%02x%02x%02x' % color)
                            canvas.create_text(x2 - (x2 - x1) / 5, (y1 + y2) / 2, text=str(round(value[0], 2)),
                                               font=(
                                               'TkDefaultFont', int(0.15 * ((canvas_width - 2 * edge_dist) / cols))),
                                               fill='white')  # Print the best value in the middle of the cell
            else:  # This is a boulder state
                x1 = edge_dist + col * ((canvas_width - 2 * edge_dist) / cols)
                # y1 = edge_dist + row * ((canvas_height - edge_dist - bottom_space) / rows)
                y1 = edge_dist + (rows - row - 1) * ((canvas_height - edge_dist - bottom_space) / rows)
                x2 = x1 + ((canvas_width - 2 * edge_dist) / cols)
                # y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)
                y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)
                canvas.create_rectangle(x1, y1, x2, y2, fill='grey', outline='white')

    canvas.create_text(int(canvas_width / 2), canvas_height - bottom_space / 2,
                       font=('TkDefaultFont', int(bottom_space / 2)),
                       text=('VALUE AFTER ' + str(iterations) + ' EPISODES'),
                       fill='white')  # Write text at the bottom of the canvas

    canvas.pack()

