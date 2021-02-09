# import thread
import threading
import random
import time

def randoms(threadName, quantity, delay=0):
    randoms = []
    count = 0
    while count < quantity:
        time.sleep(delay)
        count += 1
        randoms.append(random.randint(1, 10))
    return randoms

exitFlag = 0

class myThread(threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name

    def run(self):
        # print("Starting ", self.name)
        numbers = randoms(self.name, random.randint(1, 10))

        for n in numbers:
            moves.append(n)
        # print("N", numbers)
        # print("Exiting ", self.name)

threads = []
moves = []
# Create new threads
for i in range(10):
    threads.append(myThread(i, "Thread-{i}".format(i=i)))

# Start new Threads
for t in threads:
    t.start()

print("Exiting Main Thread")
print(moves)
