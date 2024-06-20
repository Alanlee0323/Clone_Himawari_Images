import os
import re
from moviepy.editor import ImageSequenceClip

# 設定圖片資料夾路徑
image_folder = input("請輸入圖片資料夾路徑: ")
output_video = 'output_video.mp4'

# 定義正則表達式來解析檔名中的時間
pattern = re.compile(r'tbblittle-endian-(\d{12})\.ext\.01\.fld_output\.png')

# 取得資料夾中所有圖片檔案
images = [img for img in os.listdir(image_folder) if pattern.match(img)]

# 按時間排序圖片檔案
images.sort(key=lambda x: pattern.search(x).group(1))

# 完整圖片路徑
image_paths = [os.path.join(image_folder, img) for img in images]

# 設定影片的幀率 (每秒顯示多少張圖片)
fps = 5  # 每張圖片表示10分鐘，因此每秒幀率為1/600

# 創建影片
clip = ImageSequenceClip(image_paths, fps=fps)

# 將影片寫入文件
clip.write_videofile(output_video, codec='libx264')
