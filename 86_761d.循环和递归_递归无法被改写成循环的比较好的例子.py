# !/usr/bin/python
# coding: utf-8

# http://www.qlcoder.com/task/761d
# 循环和递归在编程中经常会用到。
# 有人认为:"所有递归都可以改写成循环,并且循环的效率会大于递归"。 可以参考知乎的某个帖子:所有递归都可以改写成循环吗？。
# 奥利奥却不这么认为，奥利奥认为递归的表达能力要比循环高很多呢。
# 下面有一个伪代码写的递归函数。奥利奥认为它很难被改写成循环。这是一个递归无法被改写成循环的比较好的例子。
#
# function f(m,n)
# {
#     if(m==0)return n+1;
#     if(n==0)return f(m-1,1);
#     return f(m-1,f(m,n-1));
# }
# 这题的答案是f(7,7)的16进制表达的最后8位。(答案是一个长度为8的16进制数,请用大写)

# 阿克曼函数
# 果然是脑筋急转弯，看了N久公式，然后想了一下位运算，轻松手动得到答案

cache = {}

# f会导致栈溢出。
def f(m,n):
	key = '{}_{}'.format(m, n)
	print(key)
	if key in cache:
		return cache[key]

	answer = 0
	if m == 0:
		answer = n+1
	elif n == 0:
		answer = f(m-1,1)
	else:
		answer = f(m-1,f(m,n-1))

	cache[key] = answer
	return answer

# f2使用数组代替调用栈。
# 内部计算要不返回一个数字，要不返回一个向量。
# 要不返回一个方法对象。计算该方法对象有可能返回值或者新的方法对象。
# 将所有的方法推入数组。
# 当一个方法对象返回数字时，其父方法对象即可被计算。
def f_arr(m, n):
	def calc(m, n):
		key = '{}_{}'.format(m, n)
		if key in cache:
			print('find {} = {}'.format(key, cache[key]))
			return cache[key]

		if m == 0:
			cache[key] = (n + 1) % (16**8)
			print('calc {} = {}'.format(key, cache[key]))
			return cache[key]

		if n == 0:
			newm = m - 1
			newn = 1
			newkey = '{}_{}'.format(newm, newn)
			if newkey in cache:
				print('calc {} = {} = {}'.format(key, newkey, cache[newkey]))
				cache[key] = cache[newkey]
				return cache[newkey]
			else:
				print('calc {} need1 {}'.format(key, newkey))
				return (newm, newn)


		newm = m
		newn = n - 1
		newkey = '{}_{}'.format(newm, newn)
		if newkey not in cache:
			print('calc {} need2 {}'.format(key, newkey))
			return (newm, newn)
		else:
			newm = m - 1
			newn = cache[newkey]
			newkey = '{}_{}'.format(newm, newn)
			if newkey in cache:
				print('calc {} = {} = {}'.format(key, newkey, cache[newkey]))
				cache[key] = cache[newkey]
				return cache[newkey]
			else:
				print('calc {} need3 {}'.format(key, newkey))
				return (newm, newn)


	arr = [(m, n)]

	while(len(arr)):
		temp = arr[-1]
		result = calc(temp[0], temp[1])
		if isinstance(result, int):
			arr.pop()
		else:
			arr.append(result)

	return result


'''
  f(1, n)
= f(0, f(1, n - 1))
= f(1, n - 1) + 1
又 f(1, 0) = 2
所以 f(1, n) = n + 2

  f(2, n)
= f(1, f(2, n - 1))
= f(2, n - 1) + 2
又 f(2, 0) = 3
所以 f(2, n) = 2*n + 3

  f(3, n)
= f(2, f(3, n - 1))
= f(3, n - 1) * 2 + 3
又 f(3, 0) = 5。

分析可知，f(7, 7)的结果一定在f(3, n)的结果集中，并且n是一个很大的数字。
需求的结果保留16**8的尾数。
特别的，当n >= 29时，这个尾数均为FFFFFFFD(即16**8 - 3)。所以FFFFFFFD即为所求。
'''

dic = {}
a = 5
i = 0
n = 16 ** 8
print(n)
while a not in dic:
	if i % (1024 * 1024) == 0:
		print('calc {} M'.format(i / 1024 / 1024))

	dic[a] = i
	a = (a * 2 + 3) % n
	i += 1

print('find! f(3, {}) = f(3, {}) = {}'.format(i, dic[a], a))
