import os
import csv


'''
if os.path.isfile('./Attendance.csv') == 0:
    with open('Attendance.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Time"])
'''


with open('innovators.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["SN", "Name", "Contribution"])


