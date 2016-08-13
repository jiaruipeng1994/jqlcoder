# http://www.qlcoder.com/task/7617

from PIL import Image
import urllib.request
import io
url = 'http://121.201.63.168/uploads/145303100168558.png'
file = urllib.request.urlopen(url)
tmpIm = io.BytesIO(file.read())
im = Image.open(tmpIm)
r, g, b = im.split()
out = r.point(lambda i: (i % 2 == 0) * 200)
out.show()
