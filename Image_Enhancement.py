import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def process_image(image_path):
    # 讀取影像
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # 檢查影像是否成功讀取
    if image is None:
        raise ValueError(f"Failed to load the image at {image_path}. Please check the file path and integrity.")

    # 直方圖均衡化
    hist_eq_image = cv2.equalizeHist(image)

    # 自適應直方圖均衡化 (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    clahe_image = clahe.apply(image)

    # 拉普拉斯濾波
    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    laplacian_image = cv2.convertScaleAbs(laplacian)

    # 高斯濾波後的邊緣檢測
    blurred_image = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred_image, 50, 150)

    # 小波變換
    def wavelet_transform(image, level=1):
        import pywt
        coeffs = pywt.wavedec2(image, 'haar', level=level)
        coeffs_H = list(coeffs)
        coeffs_H[0] *= 0  # Approximation coefficients
        reconstructed_image = pywt.waverec2(coeffs_H, 'haar')
        return np.uint8(reconstructed_image)

    wavelet_image = wavelet_transform(image, level=2)

    return {
        "Original": image,
        "Histogram Equalization": hist_eq_image,
        "CLAHE": clahe_image,
        "Laplacian": laplacian_image,
        "Gaussian + Canny": edges,
        "Wavelet Transform": wavelet_image
    }

def main():
    input_folder = input("請輸入包含影像的資料夾路徑：")
    output_folder = input("請輸入儲存結果的資料夾路徑：")

    if not os.path.exists(input_folder):
        raise FileNotFoundError(f"輸入資料夾 {input_folder} 不存在。")
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            print(f"正在處理 {input_path} ...")

            try:
                processed_images = process_image(input_path)

                # 儲存每個處理過的影像
                for key, img in processed_images.items():
                    save_path = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}_{key}.png")
                    cv2.imwrite(save_path, img)

                print(f"已儲存處理過的影像到 {output_path}")

            except Exception as e:
                print(f"處理影像 {input_path} 時發生錯誤：{e}")

if __name__ == "__main__":
    main()
