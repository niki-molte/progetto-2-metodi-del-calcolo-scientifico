import numpy as np
from PIL import Image
from matplotlib import pyplot as plt

def make_imgs_plot(img, compressed_img, F, d):
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

def make_frequency_plot(var_img, var_block_img, index, var_img2, var_block_img2, index2, image_width, F):
    blocchi_per_riga = image_width // F

    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='3d')
    x = np.arange(F)
    y = np.arange(F)
    X, Y = np.meshgrid(x, y)
    ax.bar3d(X.flatten(), Y.flatten(), np.zeros_like(var_block_img).flatten(),
             0.8, 0.8, var_block_img.flatten(), shade=True)

    riga_blocco = index2 // blocchi_per_riga
    col_blocco = index2 % blocchi_per_riga
    y_px = riga_blocco * F
    x_px = col_blocco * F

    ax.set_title(f"DCT2 blocco max varianza {round(var_img, 2)}\ncoord x:{x_px} y:{y_px}")

    fig2 = plt.figure()
    ax = fig2.add_subplot(111, projection='3d')
    x = np.arange(F)
    y = np.arange(F)
    X, Y = np.meshgrid(x, y)
    ax.bar3d(X.flatten(), Y.flatten(), np.zeros_like(var_img2).flatten(),
             0.8, 0.8, var_block_img2.flatten(), shade=True)

    riga_blocco = index2 // blocchi_per_riga
    col_blocco = index2 % blocchi_per_riga
    y_px = riga_blocco * F
    x_px = col_blocco * F

    ax.set_title(f"DCT2 blocco max varianza {round(var_img2, 2)}\ncoord x:{x_px} y:{y_px} dopo compressione")
    plt.show(block=False)
