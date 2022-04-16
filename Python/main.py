# MCCCCXXXVIIII
# MCDXXXIX

# MCDXXXVXIV

from enum import Enum


legend = {
	"I": 1,
	"V": 5,
	"X": 10,
	"L": 50,
	"C": 100,
	"D": 500,
	"M": 1000
}


class RomanNumeralNotation(Enum):
	Standard = 0
	Additive = 1
	IrregularSubtractive = 2



def dec2rom(number: int, notation: RomanNumeralNotation):
	sorted_legend = sorted(legend.items(), key=lambda x: x[1])
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
			if notation == RomanNumeralNotation.Additive:
				continue

			# If able to subtract reduced numeral
			# Ex. If not X but IX works (9)
			reducer = (v * 0.1) if (str(v)[0] == "1") else (v * 0.2)
			subk, subv = next(
				filter(lambda x: x[1] == int(reducer), legend.items()), 
				(None, None)
			)
			if subk is None and subv is None:
				continue

			if (v - subv) <= number:
				number -= (v - subv)
				out += subk + k
				break

	return out


def rom2dec(numerals: str):
	total = 0
	prev_dval = -1 # Start below minimum number
	for digit in numerals[::-1]:
		dval = legend.get(digit)
		if prev_dval <= dval:
			total += dval
		else:
			total -= dval
		prev_dval = dval
	return total

def main():
	print(f"{dec2rom(3999)=}")


if __name__ == "__main__":
	main()
