

def CountFrequency(my_list):
    # Creating an empty dictionary
    freq = {}
    for item in my_list:
        if (item in freq):
            freq[item] += 1
        else:
            freq[item] = 1

    print(freq)


updated = []
with open("D:/Bytes.txt", "r") as r_file:
    CountFrequency(r_file.readlines())





