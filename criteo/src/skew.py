USAGE = """

python skew.py {file_name} {target peak}

"""

INTRO = """

Change the skewness of a list of numbers.
Assume the numbers has a uni-modal distribution. To shift its peak to a\n
different place within its spread, each number is shifted to:

x_new = peak_new - (peak_old - x_old)/(peak_old - min)*(peak_new - min), if x_old < peak_old
x_new = (x_old - peak_old)/(max - peak_old)*(max - peak_new) + peak_new, if x_old > peak_old

"""

import sys

def bin(numbers, num_bins):
	a = min(numbers)
	b = max(numbers)
	bin_size = (b - a) / num_bins
	counts = [0] * (num_bins+1)
	for x in numbers:
		i = int((x - a) / bin_size)
		counts[i] = (counts[i] + 1)
	counts[num_bins-1] += counts[num_bins]
	counts.pop(num_bins)
	return counts, bin_size, a, b

def load(file_name):
	ret = []
	with open(file_name) as f:
		line = f.readline()
		while line:
			ret.append(float(line.strip('\n')))
			line = f.readline()
	return ret

def transform(numbers, peak_new, peak_old, a, b):
	ret = []
	for x_old in numbers:
		if x_old < peak_old:
			x_new = peak_new - (peak_old - x_old)/(peak_old - a)*(peak_new - a)
		else:
			x_new = (x_old - peak_old)/(b - peak_old)*(b - peak_new) + peak_new
		ret.append(x_new)
	return ret

def dump(file_name, numbers):
	with open(file_name, 'w') as f:
		for x in numbers:
			f.write("%f\n" % x)


if __name__ == "__main__":
	if len(sys.argv) < 3:
		print USAGE
		exit(1)

	file_name = sys.argv[1]
	peak_new = float(sys.argv[2])
	num_bins = 100
	if len(sys.argv) >=4:
		num_bins = int(sys.argv[3])

	numbers = load(file_name)
	counts, bin_size, low, high = bin(numbers, num_bins)
	print counts, bin_size, low
	m = max(counts)
	ind1 = counts.index(m)
	ind2 = ind1+1
	while ind2 < num_bins and counts[ind2] == m:
		ind2 += 1
	peak_old = (ind1+ind2-1)/2.0*bin_size + low + bin_size/2

	transformed = transform(numbers, peak_new, peak_old, low, high)
	dump("%s.skew.%f" % (file_name, peak_new), transformed)






