#!/usr/bin/env python3

import tkinter as tk
import tkinter.scrolledtext as tkscrolled
import os
from pathlib import Path
from csv import reader

# Default window dimensions
WIDTH = 1024
HEIGHT = 768

# Constants to hold data
ALL_MEALS = []
MEAL_PLAN = []
GROCERY_LIST = []
OPTIONAL_LIST = []

# Paths for file read/write
APP_DIR = Path(os.getcwd())

root = tk.Tk()

def load_meals():
    with open("mealdat.csv", "r") as read_obj:
        csv_reader = reader(read_obj)
        ALL_MEALS = list(csv_reader)
    return ALL_MEALS


def update_plan(items, MEAL_PLAN, GROCERY_LIST, ALL_MEALS, OPTIONAL_LIST):
    del MEAL_PLAN[:]
    for key, value in items:
        if value.get() > 0:
            if key not in MEAL_PLAN:
                MEAL_PLAN.append(key)
    print("\nNEW MEAL PLAN:")
    for k, each in enumerate(MEAL_PLAN):
        print("{}. {}".format(k + 1, each))
    print_groceries(MEAL_PLAN, GROCERY_LIST, ALL_MEALS, OPTIONAL_LIST)
   

def print_groceries(MEAL_PLAN, GROCERY_LIST, ALL_MEALS, OPTIONAL_LIST):
    del GROCERY_LIST[:]
    del OPTIONAL_LIST[:]
    for each in MEAL_PLAN:
        for meal in ALL_MEALS:
            if each in meal:
                new_list = meal[4].split(",")
                for item in new_list:
                    GROCERY_LIST.append(item)
                if meal[5]:
                    new_option = meal[5].split(",")
                    for option in new_option:
                        OPTIONAL_LIST.append(option)
    GROCERY_LIST.sort()
    OPTIONAL_LIST.sort()
    with open("Grocery_List.txt", "w") as f:
        f.write("GROCERIES:\n")
        for each in GROCERY_LIST:
            f.write(each)
            f.write("\n")
        f.write("\nOPTIONAL ITEMS:\n")
        for each in OPTIONAL_LIST:
            f.write(each)
            f.write("\n")
    print("\nGROCERIES:")
    for each in GROCERY_LIST:
        print(each)
    print("\nOPTIONAL ITEMS:")
    for each in OPTIONAL_LIST:
        print(each)

def select_random(items, MEAL_PLAN, GROCERY_LIST, ALL_MEALS, OPTIONAL_LIST):
    print("\nComing soon!\n")


def main_menu(ALL_MEALS, MEAL_PLAN, GROCERY_LIST, OPTIONAL_LIST):
    root.title("MealPlanner 2.0")
    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    frame = tk.Frame(root, bg="white", bd=5)
    frame.place(relx=0.5, rely=0.05, relwidth=0.9, relheight=0.9, anchor="n")

    label = tk.Label(frame, text="Mrs. Suzy's MealPlanner", font="bold")
    label.place(relx=0.40, y=5)
   
    checkbutton_list = []
    del checkbutton_list[:]
    intvar_dict = {}
    intvar_dict.clear()
    for each in ALL_MEALS:
        intvar_dict[each[0]] = tk.IntVar()
    final_y = 0
    for i, each in enumerate(ALL_MEALS):
        if i == 0:
            checkbutton_list.append(tk.Checkbutton(frame, text="{}. {} - {}".format(i + 1, each[0], each[1]), variable=intvar_dict[each[0]], onvalue=1, offvalue=0))
            checkbutton_list[i].place(x=15, y=50)
            final_y += 50
        else:
            checkbutton_list.append(tk.Checkbutton(frame, text="{}. {} - {}".format(i + 1, each[0], each[1]), variable=intvar_dict[each[0]], onvalue=1, offvalue=0))
            checkbutton_list[i].place(x=15, y=50+(20*i))
            final_y += (20*i)

    button = tk.Button(frame, text="Print grocery list", font=40, command=lambda: update_plan(intvar_dict.items(), MEAL_PLAN, GROCERY_LIST, ALL_MEALS, OPTIONAL_LIST))
    button.place(relx=0.33, y=final_y+20, height=30, relwidth=0.33)

    button = tk.Button(frame, text="Randomize selections", font=40, command=lambda: select_random(intvar_dict.items(), MEAL_PLAN, GROCERY_LIST, ALL_MEALS, OPTIONAL_LIST))
    button.place(relx=0.33, y=final_y+50, height=30, relwidth=0.33)

    button = tk.Button(frame, text="Quit", font=40, command=lambda: root.destroy())
    button.place(relx=0.33, y=final_y+80, height=30, relwidth=0.33)

    label = tk.Label(frame, text="INSTRUCTIONS:")
    label.place(x=5, y=final_y+140)

    label = tk.Label(frame, text="Select your meals and then press 'Print grocery list' or just select 'Randomize selections'.")
    label.place(x=5, y=final_y+170)

def main():
    ALL_MEALS = load_meals()
    main_menu(ALL_MEALS, MEAL_PLAN, GROCERY_LIST, OPTIONAL_LIST)

if __name__ == '__main__':
    main()
