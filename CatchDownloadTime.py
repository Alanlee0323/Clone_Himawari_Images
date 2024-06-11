import pandas as pd

def catch_time(csv_file_path, time_column_name, new_csv_file_path):
    """
    這個函數用於從 csv 文件中擷取時間並將其轉換為整數格式。
    :param csv_file_path: csv 文件的路徑
    :param time_column_name: 包含時間的列名
    :param new_csv_file_path: 新的 csv 文件的路徑
    :return: 無返回值
    """
    # 讀取 csv 文件
    dataframe = pd.read_csv(csv_file_path)
    
    # 過濾 Elevation > 0.01 的行
    dataframe_filter = dataframe[dataframe['Elevation'] > 0.01]
    
    # 將時間列轉換為日期時間格式
    dataframe_filter[time_column_name] = pd.to_datetime(dataframe_filter[time_column_name])
    
    # 提取日期部分並格式化為整數格式
    dataframe_filter['Time_int'] = dataframe_filter[time_column_name].dt.strftime('%Y%m%d').astype(int)
    
    # 根據時間列進行排序
    dataframe_filter.sort_values(by=time_column_name, inplace=True)

    # 去除 Time_int 列中的重複值
    dataframe_filter = dataframe_filter.drop_duplicates(subset=['Time_int'])
    
    # 將結果寫入新的 csv 文件
    dataframe_filter.to_csv(new_csv_file_path, index=False)

# 定義文件路徑
csv_file_path = r'C:\Users\alana\Dropbox\實驗室\Github\Research\Data\Output2.csv'
new_csv_file_path = r'C:\Users\alana\Dropbox\實驗室\Github\Research\Data\Output3.csv'

# 調用函數
catch_time(csv_file_path, 'Time', new_csv_file_path)
