import glob
import pandas as pd
import os 

filenames = glob.glob('Data_Disgregada/*.csv')

try:
    os.system("mkdir Series_a_ajustar")
except:
    pass

for filename in filenames: 

    try:

        fileid = int(filename.replace('.csv', '').split('id')[1])
    
        data = pd.read_csv(filename)

        # Pongo el tiempo como el índice de los datos
        data.time = pd.to_datetime(data.time, format = "%Y-%m-%d %H:%M:%S" )
        data.set_index('time', inplace = True)

        blog = data[data.media == 'B'].resample('1H').sum()['frequency']
        media = data[data.media == 'M'].resample('1H').sum()['frequency']

        new_index = blog.index.union(media.index)

        media = media.reindex(new_index).fillna(0.00)
        blog = blog.reindex(new_index).fillna(0.00)

        all_data = pd.DataFrame(index = new_index)
        all_data['media'] = media.to_list()
        all_data['blog'] = blog.to_list()
 
        # We define a cut between 3 days before the global peak and 21 days after that
        resample_dropped = all_data[(all_data.index > (all_data.sum(axis = 1).idxmax() - pd.to_timedelta('3D'))) & (all_data.index < (all_data.sum(axis = 1).idxmax() + pd.to_timedelta('21D')))]

        # Rolling window of 24H to extract the trend
        rolling_dropped = resample_dropped.rolling('1D', center=True).mean()
    
        rolling_dropped.to_csv('Series_a_ajustar/Corte_id{}.csv'.format(fileid))

    except:
        pass
