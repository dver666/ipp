from PythonMagick import *
img=Image('30x30','red')
img.write('test1.png')
data=file('test1.png','rb').read()
img=Image(Blob(data))
img.write('test2.png')
print "now you should have two png files"

#import PythonMagick as Magick
img = Magick.Image("testIn.jpg")
img.quality(100) #full compression
img.magick('PNG')
img.write("testOut.png")
