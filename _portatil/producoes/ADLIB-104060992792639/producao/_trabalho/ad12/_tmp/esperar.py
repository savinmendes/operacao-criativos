import os, time, sys
d, n = sys.argv[1], int(sys.argv[2])
for _ in range(110):
    if len(os.listdir(d)) >= n: print("pronto"); break
    time.sleep(5)
print(len(os.listdir(d)))
