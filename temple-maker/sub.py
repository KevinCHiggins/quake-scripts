import super

class Sub(super.Super):
	def __init__(self, word):
		self.test.append(word)
jim = Sub("Bog")
jim.dor()
hay = Sub("Min")
hay.dor()


print(jim.test)
print(str(jim.dor))