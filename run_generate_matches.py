import os
import time

if __name__ == '__main__':
	print("starting")
	while(True):
		start_time = time.time()
		os.system("python generate_matches.py")
		elapsed_time = time.time() - start_time
		if(elapsed_time < 5):
			print("all games completed")
			break
		waittime = max(0,(140-elapsed_time))
		print("waiting: " + str(waittime))
		time.sleep(waittime)
	print("done")