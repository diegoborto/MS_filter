import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#input file
path_file = '/Users/diegobortolin/Documents/Programmazione/Python/MS spectra/'
name_file = 'Cu2O 13_05 3h 3,9 min' 
extension_file= '.csv'
folder_output = '/Filtered/'

# Load the CSV file into a DataFrame
df = pd.read_csv(path_file+name_file+extension_file, sep='\t', names=['m/z', 'abb %'])
df['m/z'] = df['m/z'].astype(int)

# Display the first few rows of the DataFrame
print(df.head(50))

# Check for missing values
missing_values = df.isnull().sum()
print("Missing values:",missing_values)

#plotting the original dataset
plt.figure()
df.plot(x='m/z',y='abb %', kind='bar')
plt.title('Original spectra '+name_file)


#filtering the background
threshold = 5.0
filtered_df = df[df['abb %'] > threshold]
print("Filtered MS spectra with threshold:", threshold)
print(filtered_df)

graph_filt_df= df.map(lambda x:x if x > threshold else 0)

#exporting the dataframe to csv
filtered_df.to_csv(path_file+folder_output+name_file+'_filtered'+str(threshold)+extension_file, sep='\t', index=False)

#plotting the filtered dataset
plt.figure()
graph_filt_df.plot(x='m/z',y='abb %', kind='bar')
plt.title('Filtered spectra '+name_file)


#input file of the background
name_file_blk = 'Blankstd 2_filtered30.0'
#name_file_blk_gph = 'Blankstd 2_filtered_graph30.0'

blk_df = pd.read_csv(path_file+name_file_blk+extension_file, sep='\t')
print('Background values:')
print(blk_df)
filtered_df = pd.read_csv(path_file+folder_output+name_file+'_filtered'+str(threshold)+extension_file, sep='\t')

print("Filtered MS spectra imported:", threshold)
print(filtered_df)
df_withoutblk = filtered_df

for i in range(len(filtered_df)):
    # Get corresponding rows from df1 and df2
    row_filtered_df = filtered_df.loc[i,'m/z']
    for j in range(len(blk_df)):
        row_blk_df = blk_df.loc[j,'m/z']
        #print(row_filtered_df)
        # Compare rows
        if row_filtered_df == row_blk_df:
            df_withoutblk.loc[i,'m/z'] = filtered_df.loc[i,'m/z']  
            df_withoutblk.loc[i,'abb %'] = filtered_df.loc[i,'abb %'] - blk_df.loc[j,'abb %']
 
#filtering the background
threshold = 5.0
filtered_df_withoutblk = df_withoutblk[df_withoutblk['abb %'] > threshold]
print("Filtered MS spectra with threshold:", threshold)
print(filtered_df)            

print('Result:')
print(filtered_df_withoutblk.head(20))

#exporting the dataframe to csv
filtered_df_withoutblk.to_csv(path_file+folder_output+name_file+'_filtered'+str(threshold)+'_withoutblank'+extension_file, sep='\t', index=False)

#graph of the filtred data and without background
filtered_df_withoutblk = pd.read_csv(path_file+folder_output+name_file+'_filtered'+str(threshold)+'_withoutblank'+extension_file, sep='\t') 
graph_filtered_df_withoutblk= df

print('Uploaded:')
print(filtered_df_withoutblk)
print(graph_filtered_df_withoutblk)
for i in range(len(df)):
    row_graph_filtered_df_withoutblk = graph_filtered_df_withoutblk[i,'m/z']    
    for j in range(len(filtered_df_withoutblk)):
        row_filtered_df_withoutblk = filtered_df_withoutblk[j,'m/z']
        
        # Compare rows
        if row_graph_filtered_df_withoutblk  == row_filtered_df_withoutblk:
            graph_filtered_df_withoutblk.loc[i,'abb %'] = filtered_df_withoutblk[j,'abb %']
        else:
            graph_filtered_df_withoutblk.loc[i,'abb %'] = 0.0

plt.figure()
graph_filtered_df_withoutblk.plot(x='m/z',y='abb %', kind='bar')
plt.title('Original spectra, filtered and without blank '+name_file)
plt.show()

