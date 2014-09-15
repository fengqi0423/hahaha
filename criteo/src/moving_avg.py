import sys

if __name__ == "__main__":
	"""
	python moving_avg.py {file_name} {window_size}
	"""
	f = open(sys.argv[1])
	o = open(sys.argv[1]+"_moving_avg", 'w')
	w = int(sys.argv[2])

	line = f.readline()
	window = []
	sm = 0.0
	count = 0
	while line:
		count += 1
		x = float(line.strip('\n'))
		sm += x
		window.append(x)

		if count > w:
			sm -= window[0]
			window.pop(0)

		o.write("%d\t%f\n" % (count, sm/w))

		line = f.readline()

	f.close()
	o.close()