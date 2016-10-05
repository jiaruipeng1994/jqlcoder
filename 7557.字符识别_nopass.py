'''
使用开源库tesseract进行OCR。
原始图片的特点是：
1.都是一个英文单词
2.文字大小一致（文字高度大约15）
3.经过旋转，但还是朝上的。
原始图片经过旋转，直接OCR效果不佳，
因而先将其规范化成横向文字，再进行OCR

安装7z:
sudo apt-get install p7zip
安装 PIL:
sudo pip3 install pillow
安装tesseract（ocr库）：
sudo apt-get install tesseract-ocr
安装 pytesseract ：
sudo pip3 install pytesseract
'''

import os
dirname = 'temp_7557'
filename = dirname + '.7z'
fileurl = 'http://qlcoder.com/download/cap1.7z'
if not os.path.isdir(dirname):
    if not os.path.isfile(filename):
        print('下载数据文件……')
        import requests
        r = requests.get(fileurl)
        with open(filename, 'wb') as f:
            f.write(r.content)
    print('解压缩……')
    os.system( '7zr x {} -o{}'.format(filename, dirname))
    print('数据准备完毕。')


from PIL import Image

def xxx(image):
	'对原始图片进行旋转修正及其他增强'

	# 获取图片内容的包围盒。返回包围盒左上角和右下角的坐标
	box = image.getbbox()
	width = box[2] - box[0]
	height = box[3] - box[1]
	# print('图片包围盒{}，宽{}，高{}'.format(box, width, height))

	#获取包围盒上沿的包围，以确定旋转的方向
	region = image.crop((box[0], box[1], box[2], box[1] + 1))
	box2 = region.getbbox()
	mid = width / 2
	if box2[0] < mid and box2[2] > mid:
		# 图像是完全平直的 不需要旋转
		return image
	adjacent = max(box2[0], width - box2[2])# 邻边
	# print('邻边包围盒{}，边长{}'.format(box2, adjacent))

	# 获取包围盒左边缘的包围，确定旋转的角度
	region = image.crop((box[0], box[1], box[0] + 1, box[3]))
	box3 = region.getbbox()
	opposite = max(box3[1], height - box3[3]) # 对边
	# print('对边包围盒{}，边长{}'.format(box3, opposite))

	import math
	angle = math.atan(opposite / adjacent) / math.pi * 180

	if box2[0] > mid:
		# 图像经过逆时针旋转。需要对其进行顺时针旋转才能还原
		angle = - angle
	# print('补偿旋转角度{}'.format(int(angle)))

	# 放大
	size = image.size
	ret = image.resize((size[0] * 2,size[1] * 2),Image.ANTIALIAS )

	# 旋转
	ret = ret.rotate(angle)

	# 亮度增强，以强化被放大模糊了的边缘
	from PIL import ImageEnhance
	ret = ImageEnhance.Contrast(ret)
	ret = ret.enhance(2)

	# 切边
	ret = ret.crop(ret.getbbox())

	# box = image.getbbox()
	# width = box[2] - box[0]
	# height = box[3] - box[1]
	# print('图片包围盒{}，宽{}，高{}'.format(box, width, height))

	return ret


# image = Image.open(dirname + '/cap1/im4.png')
# ret = xxx(image)
# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
# s = pytesseract.image_to_string(ret)
# print(s, len(s))
# print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
# image.save('source.png')
# ret.save('target2.png')
root = dirname + '/cap1'
for i in os.listdir(root):
	path = os.path.join(root, i)
	image = Image.open(path)
	temp = xxx(image)
	temp.save(dirname + '/xxx/' + i)

exit()

import pytesseract

root = dirname + '/cap1'
count = 0
fail = 0
find = 0
dic = {}
for i in os.listdir(root):
	path = os.path.join(root, i)
	count += 1
	image = Image.open(path)
	temp = xxx(image)
	s = pytesseract.image_to_string(temp)
	if len(s) == 0:
		print('{} 识别失败'.format(i))
		fail += 1
	else:
		print('{} {}'.format(i, s))
		if s in dic:
			dic[s].append(i)
			print('找到重复！！！！！！！！dic[{}] = {}'.format(s, dic[s]))

			tardir = dirname + '/find/' + s
			if not os.path.isdir(tardir):
				os.makedirs(tardir)

			for j in dic[s]:
				tarfile = tardir + '/' + j
				sourcefile = os.path.join(root, j)
				if not os.path.isfile(tarfile):
					print('将文件{}复制到{}'.format(sourcefile, tarfile))
					open(tarfile, "wb+").write(open(sourcefile, "rb").read())
			find += 1
		else:
			dic[s] = [i]

print('完毕。总共处理{}个，识别失败{}个，找到重复{}个。'.format(count, fail, find))
