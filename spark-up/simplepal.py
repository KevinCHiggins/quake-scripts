import math
pal = []
found = {}

class PaletteFactory:
	_palette_data = []


	# JASC's palette format, used by Paint Shop Pro - conveniently text-based
	def loadJascPal(self, file):
		pal_file = open(file, 'r')
		pal_str = pal_file.readlines()
		pal_str = pal_str[3:] 
		for el in pal_str:
			pal.append(tuple(map(int, el.split())))
		pal_file.close()

		return pal
	def __init__(self, file):
		self._palette_data = self.loadJascPal(file)
		
		
	def create(self, *, r = None, t_mapping = None):
		if r == None and t_mapping == None:
			return self.FullPalette(tuple(self._palette_data))
		elif t_mapping == None and r != None: # redundant clause for clarity
			return self.RestrictedPalette(tuple(self._palette_data), r)
		elif t_mapping != None and r== None:
			print("TransparencyPalette")
			return self.TransparencyPalette(tuple(self._palette_data), t_mapping) 	# Note that even without a restriction, a transparency palette shouldn't assign
														# the transparent indexed colour as it would be unintended transparancy!
		else:
			return self.FullPalette(tuple(self._palette_data)) # TODO THIS IS JUST A STAND-IN! WRONG PALETTE TYPE FOR TRANSPARENT RESTRICTED
		#else:											
		#	return self.TransparencyPaletteRestrictedPalette(r, t_mapping)

	class Palette:
		def __init__(self, palette_data):
			self._convertor = None
			self._searcher = None
			self.found = {}
			self._palette_data = palette_data
		def redmean_variance(self, c1, c2): # No square root as Wikipedia suggests it's unnecessary when finding least distances, hence "variance"
			r_bar = (c1[0] + c2[0]) / 2.0 # These formulae are from Wikipedia's Colour Difference article
			return ((2 + (r_bar / 256.0)) * (c1[0] - c2[0])**2)		+ (4.0 * (c1[1] - c2[1])**2)	+ ((2 + ((255 - r_bar) / 256)) * (c1[2] - c2[2])**2)

		def index_to_least_variant(self, rgb_col, r): 
			least = 584971 # higher than of redmean_variance((0,0,0),(255,255,255)), so works as a max
			index_to_col_with_least = 0
			# brute force through whole palette
			for i in range(r[0], r[1]):
				dist = self.redmean_variance(rgb_col, self._palette_data[i])
				if dist < least:
					least = dist
					index_to_col_with_least = i
			return index_to_col_with_least

		# abstract method?
		def paletted(self, pixel_data):
			return self._convertor(pixel_data)

	class FullPalette(Palette):
		def standard_convertor(self, pixel_data):
			paletted_l = []
			for rgb_col in pixel_data:
				
				# save results of brute force search in a dictionary in case the same rgb colour reappears
				if rgb_col not in self.found:
					self.found[rgb_col] = self.index_to_least_variant(rgb_col, (0, 256))
				paletted_l.append(self.found[rgb_col])
			return paletted_l
		def __init__(self, palette_data):
			super().__init__(palette_data)
			self._convertor = self.standard_convertor
			self._searcher = self.index_to_least_variant
	class RestrictedPalette(Palette):
		def ranged_convertor(self, pixel_data):
			paletted_l = []
			for rgb_col in pixel_data:
				
				# save results of brute force search in a dictionary in case the same rgb colour reappears
				if rgb_col not in self.found:
					self.found[rgb_col] = self.index_to_least_variant(rgb_col, (self._start_range, self._end_range))
				paletted_l.append(self.found[rgb_col])
			return paletted_l
		def __init__(self, palette_data, r): # I'll see about making defaults for the range later
			super().__init__(palette_data)
			self._convertor = self.ranged_convertor	
			# TODO value error handling
			self._start_range = r[0]
			self._end_range = r[1]
			self._searcher = self.index_to_least_variant
	class TransparencyPalette(Palette):
		def transparency_handling_convertor(self, pixel_data):
			paletted_l = []
			
			for rgb_col in pixel_data:
				# catch transparent colour in source image (an rgb colour specified by t_mapping)
				
				if rgb_col[0] == self._transparent_rgb[0] and rgb_col[1] == self._transparent_rgb[1] and rgb_col[2] == self._transparent_rgb[2]:

					paletted_l.append(self._transparent_index) # convert it to the indexed transparent colour specified by t_mapping
				else:
					# save results of brute force search in a dictionary in case the same rgb colour reappears
					if rgb_col not in self.found:
						self.found[rgb_col] = self.index_to_least_variant(rgb_col, (0, 256))
					paletted_l.append(self.found[rgb_col])
			return paletted_l
		def index_to_least_variant_avoid_transparent_index(self, rgb_col, r): 
			least = 584971 # higher than of redmean_variance((0,0,0),(255,255,255)), so works as a max
			index_to_col_with_least = 0
			# brute force through whole palette
			for i in range(r[0], r[1]):
				if i != self._transparent_index: # don't assign transparent index
					dist = self.redmean_variance(rgb_col, self._palette_data[i])
					if dist < least:
						least = dist
						index_to_col_with_least = i
			return index_to_col_with_least
		def __init__(self, palette_data, t_mapping): 
			super().__init__(palette_data)
			self._convertor = self.transparency_handling_convertor	
			# TODO value error handling
			self._transparent_rgb = t_mapping[0]
			self._transparent_index = t_mapping[1]
			print("Transparent rgb " + str(self._transparent_rgb) +", transparent index " + str(self._transparent_index))
			self._searcher = self.index_to_least_variant_avoid_transparent_index