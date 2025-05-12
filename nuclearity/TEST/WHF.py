def function1():
    print("THIS FUNCTION WORKS, DUDE")

element = {
    "type": "button",
    "name": "Test Button",
    "rect": [100, 100, 50, 50],
    "color": [1, 0, 0],
    "hover_color": [0, 1, 0],
    "action": function1
}

element["action"]()