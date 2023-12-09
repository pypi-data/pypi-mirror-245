# pygifdec

a python wrapper for https://github.com/lecram/gifdec

## Usage
```
import pygifdec

gif = pygifdec.open("cube.gif")

shape = (gif.width, gif.height)
print(shape)
pring(gif.size)

frame = bytearray(gif.size)
gif.render_frame(frame)
gif.get_frame()


from PIL import Image

for i in range(10):
    ret = gif.get_frame()
    if ret < 0:
        break
    gif.render_frame(frame)
    img = Image.frombuffer("RGB", shape, bytes(frame))
    img.show()
```