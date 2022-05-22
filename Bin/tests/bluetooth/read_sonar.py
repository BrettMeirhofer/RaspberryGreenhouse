import time
from Bin.helper import esp

if __name__ == "__main__":
    for x in range(5):
        start = time.time()
        print(esp.get_sonar("34:94:54:25:E3:12"))
        end = time.time()
        print(str(end - start) + "s")
        time.sleep(1)
