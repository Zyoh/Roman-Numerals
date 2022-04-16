from enum import Enum


class RomanNumerals:
	legend = {
		"I": 1,
		"V": 5,
		"X": 10,
		"L": 50,
		"C": 100,
		"D": 500,
		"M": 1000
	}

	class Notation(Enum):
		Standard = 0
		Additive = 1
		IrregularSubtractive = 2

	@classmethod
	def dec2rom(cls, number: int, /, notation: Notation = Notation.Standard) -> str:
		sorted_legend = sorted(cls.legend.items(), key=lambda x: x[1])
		# These values can be used to subtract
		# Ex. The I in IV; the X in XM
		sorted_legend_subs = []
		for i in sorted_legend:
			if str(i[1])[0] == 1:
				sorted_legend_subs.append(i)
		
		out = ""

		while number > 0:
			# Descending order, prioritise higher values
			for k, v in sorted_legend[::-1]:
				# If able to subtract
				if v <= number:
					number -= v
					out += k
					break

				# No subtractive numerals in Additive mode
				if notation == cls.Notation.Additive:
					continue

				# If able to subtract reduced numeral
				# Ex. If not X but IX works (9)
				reducer = (v) if (str(v)[0] == "1") else (v * 2) # Normalise to upper 10^n
				delta_value = None
				delta_numeral = None
				while reducer >= 1:
					reducer *= 0.1

					# Find key and value for subtractive numeral
					subk, subv = next(
						filter(lambda x: x[1] == int(reducer), cls.legend.items()), 
						(None, None)
					)
					if subk is None and subv is None:
						break
					
					if (v - subv) <= number:
						delta_value = (v - subv)
						delta_numeral = subk + k

					if notation != cls.Notation.IrregularSubtractive:
						break
				
				if delta_numeral is not None and delta_value is not None:
					number -= delta_value
					out += delta_numeral
					break

		return out

	@classmethod
	def rom2dec(cls, numerals: str) -> int:
		total = 0
		prev_dval = -1 # Start below minimum number
		for digit in numerals[::-1]:
			dval = cls.legend.get(digit)
			if prev_dval <= dval:
				total += dval
			else:
				total -= dval
			prev_dval = dval
		return total


def test():
	assert RomanNumerals.dec2rom(3999, notation=RomanNumerals.Notation.Standard) == "MMMCMXCIX"
	assert RomanNumerals.dec2rom(3999, notation=RomanNumerals.Notation.Additive) == "MMMDCCCCLXXXXVIIII"
	assert RomanNumerals.dec2rom(3999, notation=RomanNumerals.Notation.IrregularSubtractive) == "MMMIM"

	assert RomanNumerals.rom2dec("MMMCMXCIX") == 3999
	assert RomanNumerals.rom2dec("MMMDCCCCLXXXXVIIII") == 3999
	assert RomanNumerals.rom2dec("MMMIM") == 3999


def main():
	for r in [49, 99, 490, 495, 499, 990, 995, 999]:
		for n in RomanNumerals.Notation:
			print(f"{r:<4} | {n:<29} -> {RomanNumerals.dec2rom(r, notation=n)}")
		print("---")


if __name__ == "__main__":
	main()
	test()
