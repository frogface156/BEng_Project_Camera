import csv

def log_motor_ticks(log_file_path, time_at_reading, motor_ticks):
	with open(log_file_path, 'a') as log_file:
		writer = csv.writer(log_file)
		writer.writerow(['M', time_at_reading, motor_ticks[0], motor_ticks[1]])

def log_imu(log_file_path, time_at_reading, lin_acc, heading):
	with open(log_file_path, 'a') as log_file:
		writer = csv.writer(log_file)
		writer.writerow(['I', time_at_reading, lin_acc[0], lin_acc[1], lin_acc[2], heading])

def log_camera_coords(log_file_path, time_at_reading, x, y):
	with open(log_file_path, 'a') as log_file:
		writer = csv.writer(log_file)
		writer.writerow(['C', time_at_reading, x, y])