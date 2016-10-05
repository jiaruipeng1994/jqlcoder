#!/usr/bin/python
# coding: utf-8
# http://www.qlcoder.com/task/7656


vardic = {}
typedic = {}
#class mytype():
#	def __init__(self, name):
#		self.name = name
#		self.vars = []
#
#	def addvar(self, var):
#		self.vars.append(var)
#
#	def merge(self, mytype2):
#		self.vars.extend(mytype2.vars)
#		for var in mytype2.vars:
#			vardic[var] = self


f = open('7656.txt')
for line in f.readlines():
	if 0 == line.find('type'):
		typename = line[5:]
		typedic[typename] = True
	else:
		temp = line.split(' ')
		varname = temp[0]
		if varname in typedic:
			#定义一个和类型重名的变量continue
		if
		if varname in vardic:
			# 忽略
			continue

		if 'new' == temp[2]:
			# a := new b
			typename = temp[3]
			if typename not in typedic:
				continue
			vardic[varname] = typename
			print('{}-{}'.format(varname, typename))
		else:
			# a = b
			var2name = temp[2]
			if var2name not in vardic:
				continue
			vardic[varname] = vardic[var2name]
			print('{}-{}'.format(varname, vardic[var2name]))
