from tkinter import *
from PIL import Image, ImageTk, ImageGrab
import math
import os

print("Please specify amount of tiles:")
xTiles = int(input("x: "))
yTiles = int(input("y: "))
scale = int(input("scale: "))

xMinTiles = 4
yMinTiles = 8
minScale = 64

root = Tk()

no_gc = {'images': [[0 for x in range(yTiles)] for y in range(xTiles)] }
image = None
image_list = {}
image_index = []
lines = []
offset = 0

for im in os.listdir("images/"):
	image_list[im] = ImageTk.PhotoImage(Image.open("images/{}".format(im)).resize((minScale, minScale), Image.NEAREST))
	image_index.append(im)

maxOffset = max(math.ceil(len(image_index)/xMinTiles) - yMinTiles, 0)
print(maxOffset)

def _lclick(event):
	global image
	if image == None:
		return
	x, y = event.x, event.y
	xTile, yTile = math.floor(x/scale), math.floor(y/scale)
	canvas.delete(no_gc['images'][xTile][yTile])
	show_image([xTile,yTile])

def _rclick(event):
	x, y = event.x, event.y
	xTile, yTile = math.floor(x/scale), math.floor(y/scale)
	canvas.delete(no_gc['images'][xTile][yTile])
	no_gc['images'][xTile][yTile] = None

def _select(event):
	global image
	x, y = event.x, event.y
	xTile, yTile = math.floor(x/minScale), math.floor(y/minScale)
	image = image_index[yTile*xMinTiles + xTile]

def _save(event):
	print('saving')
	x=root.winfo_rootx()+canvas.winfo_x()
	y=root.winfo_rooty()+canvas.winfo_y()
	x1=x+canvas.winfo_width()
	y1=y+canvas.winfo_height()
	ImageGrab.grab().crop((x,y,x1,y1)).save("fph.png")

def _scroll(event):
	global offset
	if event.delta > 0:
		#scroll up
		offset = max(0, offset-1)
	else:
		#scroll down
		offset = min(maxOffset, offset+1)
	print("offset: {}".format(offset))
	draw_prev()

canvas = Canvas(root, width=xTiles*scale, height=yTiles*scale)
canvas.configure(background='white')
canvas.bind("<Button-1>", _lclick) #left click
canvas.bind("<Button-3>", _rclick) #right click
canvas.bind("<Button-2>", _save)   #middle click
canvas.pack()

select_menu = Canvas(Toplevel(), width=xMinTiles*minScale, height=yMinTiles*minScale)
select_menu.configure(background='white')
select_menu.bind("<Button-1>", _select)
select_menu.bind("<MouseWheel>", _scroll)
select_menu.pack()

def draw_prev():
	global offset
	select_menu.delete('all')
	draw_lines_prev()
	for i in range(offset * xMinTiles, min(len(image_list) - offset * xMinTiles, xMinTiles*(offset + yMinTiles))):
		x, y = (i-offset * xMinTiles)%xMinTiles, int((i-offset * xMinTiles)/xMinTiles)
		img = image_list[image_index[i]]
		select_menu.create_image((x*minScale + int(minScale/2),y*minScale + int(minScale/2)), image=img)

def show_image(tileLoc):
	global image
	if image == None:
		return
	img = Image.open("images/{}".format(image))
	img = img.resize((scale, scale), Image.NEAREST)
	img = ImageTk.PhotoImage(img)
	no_gc['images'][tileLoc[0]][tileLoc[1]] = img
	canvas.create_image((tileLoc[0]*scale + int(scale/2),tileLoc[1]*scale + int(scale/2)), image=img)

def draw_lines():
	for x in range(1, xTiles):
		lines.append(canvas.create_line(x*scale, 0, x*scale, yTiles*scale, fill='#cccccc'))
	for y in range(1, yTiles):
		lines.append(canvas.create_line(0, y*scale, xTiles*scale, y*scale, fill='#cccccc'))

def draw_lines_prev():
	for x in range(1, xMinTiles):
		lines.append(select_menu.create_line(x*minScale, 0, x*minScale, yMinTiles*minScale, fill='#cccccc'))
	for y in range(1, yMinTiles):
		lines.append(select_menu.create_line(0, y*minScale, xMinTiles*minScale, y*minScale, fill='#cccccc'))

draw_lines()
draw_lines_prev()
draw_prev()

root.mainloop()
