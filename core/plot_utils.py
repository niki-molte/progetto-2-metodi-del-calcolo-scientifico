import matplotlib
import numpy as np
from PIL import Image
from numpy.typing import NDArray
from matplotlib import pyplot as plt
matplotlib.use('TkAgg')
from matplotlib import cm

def make_imgs_plot(img: NDArray[float], compressed_img: NDArray[float], F: int, d: int):
    img1 = np.array(Image.fromarray(img.astype(np.uint8)))
    img2 = np.array(Image.fromarray(compressed_img.astype(np.uint8)))

    plt.figure()
    plt.imshow(img1, cmap='gray')
    plt.title("Immagine originale")
    plt.axis('off')

    plt.figure()
    plt.imshow(img2, cmap='gray')
    plt.title(f"Immagine compressa\nF: {F}, d: {d}")
    plt.axis('off')

    plt.show(block=False)


def make_pixel_plot(img_var: float, img_block: NDArray[float], compressed_var: float, compressed_block: NDArray[float], index: int, image_width: int, F: int):
    blocchi_per_riga = image_width // F
    x = np.arange(F)
    y = np.arange(F)
    X, Y = np.meshgrid(x, y)

    fig1 = plt.figure()
    ax1 = fig1.add_subplot(111, projection='3d')
    values = np.abs(img_block).flatten()
    norm = plt.Normalize(values.min(), values.max())

    # calcolo la mappa del colore con normalizzazione
    cmap = cm.get_cmap('viridis')
    colors = cmap(norm(values))

    ax1.bar3d(X.flatten(), Y.flatten(), np.zeros_like(values),
              0.8, 0.8, values, shade=True, color=colors)

    riga_blocco = index // blocchi_per_riga
    col_blocco = index % blocchi_per_riga
    y_px = riga_blocco * F
    x_px = col_blocco * F

    ax1.set_title(f"DCT2 blocco max varianza {round(img_var, 2)}\ncoord x:{x_px} y:{y_px}")
    #fig1.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax1, shrink=0.5, aspect=10)



    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111, projection='3d')
    values2 = np.abs(compressed_block).flatten()

    # calcolo la mappa del colore con normalizzazione
    norm2 = plt.Normalize(values2.min(), values2.max())
    colors2 = cmap(norm2(values2))

    ax2.bar3d(X.flatten(), Y.flatten(), np.zeros_like(values2),
              0.8, 0.8, values2, shade=True, color=colors2)

    ax2.set_title(f"DCT2 blocco max varianza {round(compressed_var, 2)}\ncoord x:{x_px} y:{y_px} dopo compressione")
    #fig2.colorbar(cm.ScalarMappable(norm=norm2, cmap=cmap), ax=ax2, shrink=0.5, aspect=10)

    plt.show(block=False)