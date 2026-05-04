import cv2
import numpy as np
from tkinter import Tk, filedialog

def freq_gaussian_low_filter(shifted_fft, radius):
    rows, cols = shifted_fft.shape
    crow, ccol = rows // 2, cols // 2
    
    # Cria grades de coordenadas unidimensionais para as linhas e colunas para representar os índices de cada pixel como frequências
    x, y = np.ogrid[:rows, :cols]
    
    # a fórmula considera a distância ao quadrado, e calcula em toda a matriz simultaneamente
    distance_sqd = (x - crow)**2 + (y - ccol)**2
    
    # Aplica a fórmula Gaussiana em toda a matriz simultaneamente
    mask = np.exp(-distance_sqd / (2 * (radius ** 2)))
    
    return shifted_fft * mask

def freq_gaussian_high_filter(shifted_fft, radius):
    rows, cols = shifted_fft.shape
    crow, ccol = rows // 2, cols // 2
    
    x, y = np.ogrid[:rows, :cols]

    distance_sqd = (x - crow)**2 + (y - ccol)**2
    
    mask = 1 - np.exp(-distance_sqd / (2 * (radius ** 2)))
    
    return shifted_fft * mask

def apply_filter_color(fft_tuple, filter, radius):
    return tuple(filter(fft_channel, radius) for fft_channel in fft_tuple)

def is_visually_gray(img):
    if len(img.shape) < 3: 
        return True
    
    b, g, r = img[:,:,0], img[:,:,1], img[:,:,2]
    if np.array_equal(b, g) and np.array_equal(g, r):
        return True
    
    return False

def load_images():
    root = Tk()
    root.withdraw()

    img_low_path = filedialog.askopenfilename(title="Selecione a imagem para baixa frequência")
    img_high_path = filedialog.askopenfilename(title="Selecione a imagem para alta frequência")

    img_low = cv2.imread(img_low_path)
    img_high = cv2.imread(img_high_path)

    if img_low is None or img_high is None:
        print("Erro ao carregar as imagens. Verifique os caminhos e tente novamente.")
        exit(1)
    
    if img_low.shape > img_high.shape:
        img_low = cv2.resize(img_low, (img_high.shape[1], img_high.shape[0]))
    elif img_high.shape > img_low.shape:
        img_high = cv2.resize(img_high, (img_low.shape[1], img_low.shape[0]))

    if is_visually_gray(img_low) or is_visually_gray(img_high):
        # converter as duas imagens para GRAY
        gray_low  = cv2.cvtColor(img_low,  cv2.COLOR_BGR2GRAY)
        gray_high = cv2.cvtColor(img_high, cv2.COLOR_BGR2GRAY)
        img_low  = cv2.cvtColor(gray_low,  cv2.COLOR_GRAY2BGR)
        img_high = cv2.cvtColor(gray_high, cv2.COLOR_GRAY2BGR)

    return img_low, img_high

def image_to_shifted_fft(image):
    # separa canais
    b, g, r = cv2.split(image)
    
    # aplica FFT em cada canal
    b_fft = np.fft.fftshift(np.fft.fft2(b))
    g_fft = np.fft.fftshift(np.fft.fft2(g))
    r_fft = np.fft.fftshift(np.fft.fft2(r))
    
    return (b_fft, g_fft, r_fft)

def shifted_fft_to_image(shifted_fft):
    b_fft, g_fft, r_fft = shifted_fft
    
    # IFFT por canal
    b = np.real(np.fft.ifft2(np.fft.ifftshift(b_fft)))
    g = np.real(np.fft.ifft2(np.fft.ifftshift(g_fft)))
    r = np.real(np.fft.ifft2(np.fft.ifftshift(r_fft)))
    
    # empilha canais
    img = cv2.merge([b, g, r])
    
    return img

if __name__ == "__main__":
    img_low, img_high = load_images()

    img_low_shifted_fft = image_to_shifted_fft(img_low)
    img_high_shifted_fft = image_to_shifted_fft(img_high)

    img_low_filtered_fft = apply_filter_color(img_low_shifted_fft, freq_gaussian_low_filter, radius=10)
    img_high_filtered_fft = apply_filter_color(img_high_shifted_fft, freq_gaussian_high_filter, radius=20)

    b_low, g_low, r_low = img_low_filtered_fft
    b_high, g_high, r_high = img_high_filtered_fft
    b = b_low + b_high
    g = g_low + g_high
    r = r_low + r_high

    hybrid_image_shifted_fft = (b, g, r)
    hybrid_image = shifted_fft_to_image(hybrid_image_shifted_fft)
    hybrid_image = np.clip(hybrid_image, 0, 255).astype(np.uint8)
    
    cv2.imshow("Imagem Hibrida", hybrid_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()