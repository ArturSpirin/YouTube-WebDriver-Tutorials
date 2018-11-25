import sys

screen = Screen(1)
draggable = sys.argv[1]
droppable = sys.argv[2]
screen.dragDrop(draggable, droppable)
