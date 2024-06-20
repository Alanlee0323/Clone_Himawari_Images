import numpy as np
import os 
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER
import re

def plot_map_with_data(data_file_path, extent, locked_longitude, locked_latitude, figsize=(10, 8)):
    # 讀取數據
    data = np.loadtxt(data_file_path)
    print(data.shape)

    # 提取時間資訊
    filename = os.path.basename(data_file_path)
    pattern = re.compile(r'tbblittle-endian-(\d{12})\.ext\.01\.fld_output\.txt')
    match = pattern.match(filename)
    if match:
        time_info = match.group(1)
    else:
        time_info = "Unknown"

    # 創建圖像
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # 設置地圖範圍
    ax.set_extent(extent)

    # 添加地理特徵
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.LAKES, alpha=0.5)
    ax.add_feature(cfeature.RIVERS)

    # 繪製數據
    img = ax.imshow(data, extent=extent, transform=ccrs.PlateCarree(), cmap='gray', vmin=0, vmax=128, origin='upper')

    # 添加色條
    cbar = plt.colorbar(img, ax=ax, orientation='vertical', pad=0.02, aspect=50)
    cbar.set_label('Value')

    # 添加網格和經緯度標記
    gl = ax.gridlines(draw_labels=True, linewidth=1, color='gray', alpha=0.5, linestyle='--')
    gl.top_labels = False
    gl.right_labels = False
    gl.xformatter = LONGITUDE_FORMATTER
    gl.yformatter = LATITUDE_FORMATTER

    # 畫出鎖定經緯度的紅線
    ax.plot([locked_longitude, locked_longitude], [extent[2], extent[3]], color='red', linestyle='-', linewidth=2, transform=ccrs.PlateCarree())
    ax.plot([extent[0], extent[1]], [locked_latitude, locked_latitude], color='red', linestyle='-', linewidth=2, transform=ccrs.PlateCarree())

    # 在右上角添加時間資訊
    plt.text(0.95, 0.95, time_info, horizontalalignment='right', verticalalignment='top', transform=ax.transAxes, fontsize=12, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none'))

    # 顯示圖像
    plt.savefig(data_file_path.replace('.txt', '.png'))


def main():
    # 假設經緯度範圍
    extent = [119, 120, 20, 21]
    # 鎖定的經緯度
    locked_longitude = 119
    locked_latitude = 20

    # 呼叫函數來繪製地圖
    for files in os.listdir(r'C:\Users\alana\Dropbox\實驗室\Github\Research\code\201810260850_201810280900'):
        if files.endswith('.txt'):
            full_path = os.path.join(r'C:\Users\alana\Dropbox\實驗室\Github\Research\code\201810260850_201810280900', files)
            plot_map_with_data(full_path, extent, locked_longitude, locked_latitude)

# 確認這個檔案被執行，而不是被引入
if __name__ == "__main__":
    main()
