########Phosphenogram#########
# To document percieved phosphenes
# configurable drawing window with monitor parameters
# you can inspect and plot data after they are saved 
# Area or perimeter in pixel, mm or visual angle
# Remy Cohan; Github.CohanR.io
# July 05, 2022
##############################

import matplotlib
matplotlib.use('TkAgg')

import pygame
import pygame.gfxdraw
import sys
import os
import csv
import math
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label, Frame, Toplevel, Entry, Button, StringVar, filedialog, simpledialog
from tkinter import ttk
import ast

# fx to calculate visual angle area
def calculate_visual_angle_area(area_mm2, viewing_distance_mm):
    """Calculate the visual angle area in square degrees."""
    if area_mm2 <= 0:
        return 0
    S = math.sqrt(area_mm2)  # S is the linear dimension in mm
    theta_rad = 2 * math.atan((S / 2) / viewing_distance_mm)
    theta_deg = math.degrees(theta_rad)
    return theta_deg ** 2

# fx to calculate visual angle perimeter
def calculate_visual_angle_perimeter(perimeter_mm, viewing_distance_mm):
    """Calculate the visual angle perimeter in degrees."""
    if perimeter_mm <= 0:
        return 0
    # For small angles, the arc length in radians is perimeter_mm / viewing_distance_mm
    # Convert to degrees
    perimeter_deg = (perimeter_mm / viewing_distance_mm) * (180 / math.pi)
    return perimeter_deg

# fx for drawing phosphenes
def draw_phosphenes(WIDTH, HEIGHT, physical_width_mm, physical_height_mm, BRUSH_SIZE, SAVE_DIR, calculate_pixel_area, calculate_physical_area, VIEWING_DISTANCE_MM):
    BACKGROUND_COLOR = (34, 34, 34)
    DRAW_COLOR = (50, 50, 50)
    DIVISION_COLOR = (0, 0, 0)

    # Pixels per millimeter (for converting areas)
    ppmm_x = WIDTH / physical_width_mm
    ppmm_y = HEIGHT / physical_height_mm

    # make sure the save directory exists
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    # initialise pygame and set up the display
    pygame.init()
    display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

    class Stroke:
        """Class to represent a single continuous stroke made by the user."""
        def __init__(self, start_pos):
            self.points = [start_pos]
            self.area_px2 = 0  # Cache the area in pixels
            self.area_mm2 = 0  # Cache the area in millimeters
            self.area_deg2 = 0  # Cache the area in square degrees
            self.perimeter_px = 0  # Cache the perimeter in pixels
            self.perimeter_mm = 0  # Cache the perimeter in millimeters
            self.perimeter_deg = 0  # Cache the perimeter in degrees

        def add_point(self, point):
            self.points.append(point)

        def draw(self, surface, color, brush_size):
            if len(self.points) > 1:
                pygame.draw.lines(surface, color, False, self.points, brush_size)

        def calculate_area(self):
            """Calculates the area of the stroke in square pixels, square millimeters, and square degrees using the shoelace formula."""
            if len(self.points) < 3:
                return 0, 0, 0  # not enough points to form an area

            area_pixels = 0
            n = len(self.points)
            for i in range(n):
                x1, y1 = self.points[i]
                x2, y2 = self.points[(i + 1) % n]
                area_pixels += (x1 * y2 - x2 * y1)

            area_pixels = abs(area_pixels) / 2

            if calculate_pixel_area:
                self.area_px2 = area_pixels
            if calculate_physical_area:
                self.area_mm2 = area_pixels / (ppmm_x * ppmm_y)
                self.area_deg2 = calculate_visual_angle_area(self.area_mm2, VIEWING_DISTANCE_MM)

            return self.area_px2, self.area_mm2, self.area_deg2

        def calculate_perimeter(self):
            """Calculates the perimeter of the stroke in pixels, millimeters, and degrees."""
            perimeter_pixels = 0
            n = len(self.points)
            for i in range(n - 1):
                x1, y1 = self.points[i]
                x2, y2 = self.points[i + 1]
                distance = math.hypot(x2 - x1, y2 - y1)
                perimeter_pixels += distance
            # close the shape by adding the distance from the last point to the first
            x1, y1 = self.points[-1]
            x2, y2 = self.points[0]
            perimeter_pixels += math.hypot(x2 - x1, y2 - y1)
            # convert to millimeters
            perimeter_mm = perimeter_pixels / ((ppmm_x + ppmm_y) / 2)
            # calculate perimeter in visual degrees
            perimeter_deg = calculate_visual_angle_perimeter(perimeter_mm, VIEWING_DISTANCE_MM)

            self.perimeter_px = perimeter_pixels
            self.perimeter_mm = perimeter_mm
            self.perimeter_deg = perimeter_deg

            return self.perimeter_px, self.perimeter_mm, self.perimeter_deg

    def draw_division_lines():
        """Draws division lines on the display to separate quadrants."""
        pygame.draw.line(display, DIVISION_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 2)
        pygame.draw.line(display, DIVISION_COLOR, (0, HEIGHT // 2), (WIDTH, HEIGHT // 2), 2)

    def save_drawing_and_strokes(strokes, timestamp):
        """Saves the current drawing to an image file and stroke data to a CSV file."""
        pygame.image.save(display, os.path.join(SAVE_DIR, f"drawing_{timestamp}.png"))
        with open(os.path.join(SAVE_DIR, f"strokes_{timestamp}.csv"), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["points", "start_x", "start_y", "end_x", "end_y", "min_x", "min_y", "max_x", "max_y", "width", "height", "area_px2", "area_mm2", "area_deg2", "perimeter_px", "perimeter_mm", "perimeter_deg"])
            for stroke in strokes:
                min_x = min(point[0] for point in stroke.points)
                max_x = max(point[0] for point in stroke.points)
                min_y = min(point[1] for point in stroke.points)
                max_y = max(point[1] for point in stroke.points)
                width = max_x - min_x
                height = max_y - min_y
                area_px2, area_mm2, area_deg2 = stroke.calculate_area()
                perimeter_px, perimeter_mm, perimeter_deg = stroke.calculate_perimeter()
                writer.writerow([stroke.points, stroke.points[0][0], stroke.points[0][1], stroke.points[-1][0], stroke.points[-1][1], min_x, min_y, max_x, max_y, width, height, area_px2, area_mm2, area_deg2, perimeter_px, perimeter_mm, perimeter_deg])

    strokes = []
    drawing = False
    running = True  #iInitialise the running flag

    while running:  #uUse the running flag to control the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # set running to False to exit the loop
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
                drawing = True
                strokes.append(Stroke(event.pos))
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                drawing = False
            elif event.type == pygame.MOUSEMOTION and drawing:
                strokes[-1].add_point(event.pos)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:  # save drawing and strokes
                    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                    save_drawing_and_strokes(strokes, timestamp)
                    strokes.clear()  # clear the list of strokes after saving
                elif event.key == pygame.K_c:  # clear the drawing
                    display.fill(BACKGROUND_COLOR)
                    draw_division_lines()
                    strokes.clear()  # clear the list of strokes after clearing the screen
                elif event.key == pygame.K_ESCAPE:  # Exit the drawing mode
                    running = False  #set running to False to exit the loop

        display.fill(BACKGROUND_COLOR)
        draw_division_lines()
        for stroke in strokes:
            stroke.draw(display, DRAW_COLOR, BRUSH_SIZE)

        pygame.display.flip()

    pygame.quit()  # Close the pygame window after exiting the loop

# fx to plot phosphenes
def plot_phosphenes(file_path, plot_mode):
    data = pd.read_csv(file_path)

    # initialise the plot
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, 800)  # width of the drawing area
    ax.set_ylim(0, 600)  # height of the drawing area
    ax.set_aspect('equal')
    ax.set_facecolor((34/255, 34/255, 34/255))  # set background color to match GUI
    ax.invert_yaxis()  # matching pygame's coordinate system

    # fx to plot each stroke based on its actual points
    def plot_stroke(points, ax, value, unit):
        # plot the actual polygon using the points
        polygon = plt.Polygon(points, closed=True, fill=None, edgecolor='r', linewidth=2)
        ax.add_patch(polygon)
        # label the value inside the polygon
        centroid_x = sum([p[0] for p in points]) / len(points)
        centroid_y = sum([p[1] for p in points]) / len(points)
        ax.text(centroid_x, centroid_y, f"{value:.2f} {unit}", color='yellow', fontsize=10, ha='center')

    # iterate over the data and plot each shape
    for i, row in data.iterrows():
        points = ast.literal_eval(row['points'])
        if plot_mode == 'pixel':
            plot_stroke(points, ax, row['area_px2'], 'px²')
        elif plot_mode == 'physical':
            plot_stroke(points, ax, row['area_mm2'], 'mm²')
        elif plot_mode == 'visual_angle':
            plot_stroke(points, ax, row['area_deg2'], 'deg²')
        elif plot_mode == 'peri_px':
            plot_stroke(points, ax, row['perimeter_px'], 'px')
        elif plot_mode == 'peri_mm':
            plot_stroke(points, ax, row['perimeter_mm'], 'mm')
        elif plot_mode == 'peri_deg':
            plot_stroke(points, ax, row['perimeter_deg'], 'deg')

    # draw division lines
    ax.axvline(400, color=(0, 0, 0), linewidth=2)  # vertical center line
    ax.axhline(300, color=(0, 0, 0), linewidth=2)  # horizontal center line

    plt.title(f"Reconstructed from the Saved CSV File (Plot Mode: {plot_mode.replace('_', ' ').capitalize()})")
    plt.show()

# main phosphenogram app
def open_draw_window():
    def start_drawing():
        width = int(width_var.get())
        height = int(height_var.get())
        physical_width_mm = int(physical_width_var.get())
        physical_height_mm = int(physical_height_var.get())
        brush_size = int(brush_size_var.get())
        save_dir = save_dir_var.get()
        calculate_pixel_area = pixel_area_var.get() == 'True'
        calculate_physical_area = physical_area_var.get() == 'True'
        viewing_distance_cm = int(viewing_distance_var.get())

        draw_phosphenes(width, height, physical_width_mm, physical_height_mm, brush_size, save_dir, calculate_pixel_area, calculate_physical_area, viewing_distance_cm * 10)

        draw_window.destroy()

    draw_window = Toplevel(root)
    draw_window.title("Drawing Window Parameters")
    
    width_var = StringVar(value="800")
    height_var = StringVar(value="600")
    physical_width_var = StringVar(value="530")
    physical_height_var = StringVar(value="400")
    brush_size_var = StringVar(value="3")
    save_dir_var = StringVar(value=os.path.join(os.path.expanduser("~"), "drawn_PTs"))
    pixel_area_var = StringVar(value="True")
    physical_area_var = StringVar(value="True")
    viewing_distance_var = StringVar(value="57")  # default to 57 cm

    Label(draw_window, text="Width:").grid(row=0, column=0)
    Entry(draw_window, textvariable=width_var).grid(row=0, column=1)

    Label(draw_window, text="Height:").grid(row=1, column=0)
    Entry(draw_window, textvariable=height_var).grid(row=1, column=1)

    Label(draw_window, text="Physical Width (mm):").grid(row=2, column=0)
    Entry(draw_window, textvariable=physical_width_var).grid(row=2, column=1)

    Label(draw_window, text="Physical Height (mm):").grid(row=3, column=0)
    Entry(draw_window, textvariable=physical_height_var).grid(row=3, column=1)

    Label(draw_window, text="Brush Size:").grid(row=4, column=0)
    Entry(draw_window, textvariable=brush_size_var).grid(row=4, column=1)

    Label(draw_window, text="Save Directory:").grid(row=5, column=0)
    Entry(draw_window, textvariable=save_dir_var).grid(row=5, column=1)

    Label(draw_window, text="Calculate Pixel Area:").grid(row=6, column=0)
    ttk.Combobox(draw_window, textvariable=pixel_area_var, values=["True", "False"]).grid(row=6, column=1)

    Label(draw_window, text="Calculate Physical Area:").grid(row=7, column=0)
    ttk.Combobox(draw_window, textvariable=physical_area_var, values=["True", "False"]).grid(row=7, column=1)

    Label(draw_window, text="Viewing Distance (cm):").grid(row=8, column=0)
    Entry(draw_window, textvariable=viewing_distance_var).grid(row=8, column=1)

    Button(draw_window, text="Start Drawing", command=start_drawing).grid(row=9, columnspan=2)

def run_plot():
    plot_mode = simpledialog.askstring("Plot Mode", "Enter plot mode:\n'pixel' for area in px²,\n'physical' for area in mm²,\n'visual_angle' for area in deg²,\n'peri_px' for perimeter in px,\n'peri_mm' for perimeter in mm,\n'peri_deg' for perimeter in deg")
    
    valid_plot_modes = ['pixel', 'physical', 'visual_angle', 'peri_px', 'peri_mm', 'peri_deg']

    if not plot_mode or plot_mode not in valid_plot_modes:
        print("Invalid plot mode. Please choose from the available options.")
        return

    file_path = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
    
    if file_path:
        plot_phosphenes(file_path, plot_mode)

    # ensure the main window is visible again
    root.deiconify()

def main():
    global root
    root = Tk()
    root.title("Phosphenogram")
    root.geometry("450x350")
    root.configure(bg="#f0f0f0")

    button_frame = Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=20)

    btn_draw = ttk.Button(button_frame, text="Draw Phosphenes", command=open_draw_window, width=25)
    btn_draw.pack(pady=10)

    btn_plot = ttk.Button(button_frame, text="Plot Phosphenes", command=run_plot, width=25)
    btn_plot.pack(pady=10)

    developer_info = Label(root, text="Designed & Developed by Remy Cohan (CohanR.GitHub.io)\n"
                                      "Perceptual Neuroscience Laboratory\n"
                                      "Centre for Integrative and Applied Neuroscience\n"
                                      "Centre for Vision Research\n"
                                      "York University, Toronto, Canada, July 2022",
                                      font=("Helvetica", 9), fg="#555555", bg="#f0f0f0")
    developer_info.pack(side="bottom", pady=10)

    root.protocol("WM_DELETE_WINDOW", root.quit)  # ensure proper termination

    root.mainloop()

if __name__ == "__main__":
    print("Starting Phosphenogram application...")
    main()
    print("Phosphenogram application closed.")
