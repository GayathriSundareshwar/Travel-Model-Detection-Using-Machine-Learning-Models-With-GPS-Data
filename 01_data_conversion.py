import os
import pandas as pd
import csv
from os import listdir
import time

import os
# traverse whole directory
Data_files = []
for root, dirs, files in os.walk(r'Data'):
    # select file name
    for file in files:
        # check the extension of files
        if file.endswith('.txt'):
            # print whole path of files
            root = root.split("/")[1]
            Data_files.append(os.path.join(root))

f = open('data.csv', 'w', encoding='utf-8', newline="")
headers = ['People_Num', 'Time', 'Travel Start Time',
           'Travel End Time', 'Lat', 'Lon', 'Alt', 'Transportation Mode']
csv_writer = csv.writer(f)
csv_writer.writerow(headers)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

start_time = time.time()

for m in range(len(Data_files)):
    #print(Data_files[m])
    if(Data_files[m] not in [".DS_Store",".ipynb_checkpoints"]):       
        trajectory_path = r"Data/"+Data_files[m]+"/Trajectory"
        Trajectory_files = listdir(trajectory_path)
        #print(Trajectory_files)
        for n in range(len(Trajectory_files)): 
            path_traj = r"Data/"+Data_files[m]+"/Trajectory/"+Trajectory_files[n]
            path_label = r"Data/"+Data_files[m]+"/labels.txt"
            labels = pd.read_table(path_label, sep='\t')
            trajectory = pd.read_table(path_traj, header=None, sep=',', skiprows=6)
            size_labels = len(labels)
            size_trajectory = len(trajectory)

            labels['Start Time'] = pd.to_datetime(labels['Start Time'])
            labels['End Time'] = pd.to_datetime(labels['End Time'])

            count = 0
            i = 0
            while i < size_labels - 1:
                if (labels['Start Time'][i + 1] - labels['End Time'][i]).seconds == 1 \
                    and labels['Transportation Mode'][i] == labels['Transportation Mode'][i + 1]:
                    labels['End Time'].at[i] = labels['End Time'].at[i + 1]
                    labels = labels.drop(labels.index[i + 1]).reset_index(drop=True)
                    count = count + 1
                    i = i - 1
                i = i + 1
                if i == size_labels - count - 1:
                    break

            size_labels = len(labels)

            trajectory['Time'] = trajectory[5] + ' ' + trajectory[6]
            trajectory = trajectory.drop(columns=[2, 4, 5, 6], axis=1)
            trajectory.columns = ['Lat', 'Lon', 'Alt', 'Time']
            trajectory['Time'] = pd.to_datetime(trajectory['Time'])
            origin_j = 0
            origin_i = 0

            for i in range(origin_i, size_labels):
                for j in range(origin_j, size_trajectory):
                    if labels['Start Time'][i] <= trajectory['Time'][j] <= labels['End Time'][i]:
                        csv_writer.writerow([Data_files[m], trajectory['Time'][j], labels['Start Time'][i],
                                         labels['End Time'][i], trajectory['Lat'][j], trajectory['Lon'][j],
                                         trajectory['Alt'][j], labels['Transportation Mode'][i]])
                        origin_j = j
                        origin_i = i
f.close()

end_time = time.time()
time_taken = end_time - start_time
print(end='\n')
print(f'Total time taken: {time_taken}')
            