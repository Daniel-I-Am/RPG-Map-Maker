from PIL import Image

file_in = input("Input file name: ")
file_out = input("Output file prefix: ")
tile_size = int(input("Tile Size: "))

img = Image.open("images/{}".format(file_in))
_w, _h = img.size
for w in range(0, _w, tile_size):
	for h in range(0, _h, tile_size):
		loc = "{}.{}".format(int(w/tile_size), int(h/tile_size))
		img.crop((w, h, w+tile_size, h+tile_size)).save("images/{}_{}.gif".format(file_out, loc))
