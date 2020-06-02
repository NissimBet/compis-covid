import sys
import random

if __name__ == '__main__':
    if len(sys.argv) < 2:
        out_file = "test_input_data.txt"
    else:
        out_file = sys.argv[1]

    with open(out_file, "w+") as file:
        cols = int(random.random() * 100) + 1
        rows = int(random.random() * 100) + 1

        for j in range(0, rows):
            data = random.sample(range(cols * rows), cols)
            file.write(",".join(str(num) for num in data))
            file.write("\n")
