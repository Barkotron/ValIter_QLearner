import tkinter as tk


def main():

    window = tk.Tk()

    # Sample grid after 10 iterations
    grid = [[[[0.19007013163048878, '↑'], [0.06949349578957349, '↓'], [0.3042928921162562, '→'], [0.15652736072667697, '←']],
     [[0.3567050660918199, '↑'], [0.3567050660918199, '↓'], [0.5072615790177806, '→'], [0.20854082305418617, '←']],
     [[0.5516309435734041, '↑'], [0.2934347863772087, '↓'], [0.7167255573827326, '→'], [0.36177064093774475, '←']],
     [[1.0, '*']]],
    [[[0.14145528124656256, '↑'], [-0.09084170632159716, '↓'], [0.021985680919856136, '→'],
      [0.021985680919856136, '←']], [[0.0, '↑'], [0.0, '↓'], [0.0, '→'], [0.0, '←']],
     [[0.35822582699563155, '↑'], [-0.052136131323774315, '↓'], [-0.7422951677576689, '→'], [0.23550898317516328, '←']],
     [[-1.0, '*']]],
    [[[-0.005154745884862078, '↑'], [-0.11687509761210652, '↓'], [-0.08963317715708871, '→'], [-0.10480675028750272, '←']],
     [[-0.08851624797145073, '↑'], [-0.08851624797145072, '↓'], [0.005677384241543525, '→'], [-0.11497840097080475, '←']],
     [[0.14907246992522372, '↑'], [-0.0030933311979867255, '↓'], [-0.1245792731957479, '→'], [-0.05441354967950589, '←']],
     [[-0.8155464044973666, '↑'], [-0.16555599028592122, '↓'], [-0.2687607840121239, '→'], [-0.09311284841394765, '←']]]]

    terminal_states = [[0, 3, 1], [1, 3, -1]]
    boulder_states = [[1, 1]]
    num_iterations = 10

    draw_board(window, grid, [row[:-1] for row in terminal_states], boulder_states,
               max_reward(terminal_states), max_punishment(terminal_states), num_iterations)

    window.mainloop()


def max_reward(terminal_states):
    max_reward = float('-inf')

    for state in terminal_states:
        if state[2] > max_reward:
            max_reward = state[2]

    return max_reward


def max_punishment(terminal_states):
    max_punishment = float('inf')

    for state in terminal_states:
        if state[2] < max_punishment:
            max_punishment = state[2]

    return max_punishment


def draw_board(window, grid, terminal, boulders, max_reward, max_punishment, iterations):

    canvas_width = 1000  # Width of the window
    canvas_height = 600  # Length of the window

    edge_dist = 10  # Distance of the board to the edge of the window
    bottom_space = 100  # Distance from the bottom of the board to the bottom of the window
    small_rect_diff = 10  # For terminal states, distance from outside rectangle to inside rectangle

    rows = len(grid)  # Number of rows in the grid
    cols = len(grid[0])  # Number of columns in the grid

    edge_dist_triangle = 5  # Distance from tip of the triangle to the edge of the rectangle
    triangle_height = int(0.1 * min(((canvas_width - 2 * edge_dist) / cols), ((canvas_height - edge_dist - bottom_space) / rows)))  # Height of the triangles
    triangle_width = 2 * triangle_height  # Width of the triangles

    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height, background='black')  # Create a black background

    for row in range(rows):  # Loop through the rows of the grid
        for col in range(cols):  # Loop through the columns of the grid
            if [row, col] not in boulders:  # If it's not a boulder state
                x1 = edge_dist + col * ((canvas_width - 2 * edge_dist) / cols)  # Top left x coordinate of the rectangle
                y1 = edge_dist + row * ((canvas_height - edge_dist - bottom_space) / rows)  # Top left y coordinate of the rectangle
                x2 = x1 + ((canvas_width - 2 * edge_dist) / cols)  # Bottom right x coordinate of the rectangle
                y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)  # Bottom right y coordinate of the rectangle

                best_move = get_best_move(grid[row][col])  # Get the index of the maximum q-value for this cell
                best_value = grid[row][col][best_move][0]  # Get the best q-value for this cell
                best_direction = grid[row][col][best_move][1]  # Get the best direction out of this cell

                if best_value >= 0:  # Best value is positive, so draw the rectangle in green
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white',
                                            fill='#%02x%02x%02x' % (0, int(200 * min(best_value / max_reward, max_reward)), 0))  # Draw the rectangle of this cell
                else:  # Best value is negative, so draw the rectangle in red
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white',
                                            fill='#%02x%02x%02x' % (int(200 * min(best_value / max_punishment, -1 * max_punishment)), 0, 0))  # Draw the rectangle of this cell

                canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(round(best_value, 2)),
                                   font=('TkDefaultFont', int(0.25 * ((canvas_width - 2 * edge_dist) / cols))), fill='white')  # Print the best value in the middle of the cell

                if [row, col] in terminal:  # If this cell is a terminal state
                    x1 = x1 + small_rect_diff
                    y1 = y1 + small_rect_diff
                    x2 = x2 - small_rect_diff
                    y2 = y2 - small_rect_diff
                    canvas.create_rectangle(x1, y1, x2, y2, outline='white')  # Draw a smaller rectangle inside
                else:  # Not a terminal state, so draw an arrow in the direction of the highest q-value
                    if best_direction == '↑':  # Draw an up arrow
                        mid = (x1 + x2) / 2
                        top = y1 + edge_dist_triangle
                        triange_points = [mid, top, mid - triangle_width / 2, top + triangle_height, mid + triangle_width / 2, top + triangle_height]
                        canvas.create_polygon(triange_points, fill='white')
                    elif best_direction == '↓':  # Draw a down arrow
                        mid = (x1 + x2) / 2
                        top = y2 - edge_dist_triangle
                        triange_points = [mid, top, mid - triangle_width / 2, top - triangle_height,
                                          mid + triangle_width / 2, top - triangle_height]
                        canvas.create_polygon(triange_points, fill='white')
                    elif best_direction == '←':  # Draw a left arrow
                        mid = (y1 + y2) / 2
                        top = x1 + edge_dist_triangle
                        triange_points = [top, mid, top + triangle_height, mid - triangle_width / 2,
                                          top + triangle_height, mid + triangle_width / 2]
                        canvas.create_polygon(triange_points, fill='white')
                    elif best_direction == '→':  # Draw a right arrow
                        mid = (y1 + y2) / 2
                        top = x2 - edge_dist_triangle
                        triange_points = [top, mid, top - triangle_height, mid - triangle_width / 2,
                                          top - triangle_height, mid + triangle_width / 2]
                        canvas.create_polygon(triange_points, fill='white')

            else:  # This is a boulder state
                x1 = edge_dist + col * ((canvas_width - 2 * edge_dist) / cols)
                y1 = edge_dist + row * ((canvas_height - edge_dist - bottom_space) / rows)
                x2 = x1 + ((canvas_width - 2 * edge_dist) / cols)
                y2 = y1 + ((canvas_height - edge_dist - bottom_space) / rows)
                canvas.create_rectangle(x1, y1, x2, y2, fill='grey', outline='white')

    canvas.create_text(int(canvas_width / 2), canvas_height - bottom_space / 2, font=('TkDefaultFont', int(bottom_space / 2)),
                       text=('VALUE AFTER ' + str(iterations) + ' ITERATIONS'), fill='white')  # Write text at the bottom of the canvas

    canvas.pack()


def get_best_move(state):
    max_value = float('-inf')
    max_index = -1

    for move in range(len(state)):
        if state[move][0] > max_value:
            max_index = move
            max_value = state[move][0]
    return max_index


main()