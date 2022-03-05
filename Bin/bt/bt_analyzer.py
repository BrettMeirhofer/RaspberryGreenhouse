import time

freq = {}
with open("BT2.txt") as read_file:
    with open("Output.txt", "w") as write_file:
        for index, line in enumerate(read_file.readlines()):
            if line != "\n":
                length = len(line)
                end = ""
                if index % 3 == 1:
                    print(index)
                    end = "\n"
                line = line[6:length-20] + end
                line = line.replace(" ", "")
                write_file.write(line)



with open("Output.txt", "r") as write_file:
    for line in write_file.readlines():
        if line in freq:
            freq[line] += 1
        else:
            freq[line] = 1


print(freq)