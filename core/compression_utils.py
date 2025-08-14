import numpy as np
from core.my_dct2_and_idct2 import Calcolous

def make_blocks(pixel_matrix, F):

    # creo le sottomatrici di dimensione F
    # e nel caso scarto l'eccesso. In blocks
    # ci sono i blocchi FxF e in remainder
    # gli avanzi
    blocks, remainder_blocks = [], []
    h, w = pixel_matrix.shape


    for i in range(0, h, F):
        for j in range(0, w, F):

            # prendo la riga che va da i a i + F, se
            # l'immagine non è divisibile con il blocco
            # allora scarto. Questo è possibile grazie
            # alla funzione min.
            block = pixel_matrix[i:min(i + F, h), j:min(j + F, w)]
            if block.shape == (F, F):
                blocks.append(block)
            else:
                remainder_blocks.append(block)

    return blocks, remainder_blocks

def make_transform(idct2_block, F):
    # corregge i range e i valori
    # nell'intervallo corretto
    for i in range(F):
        for j in range(F):
            if idct2_block[i, j] < 0:
                idct2_block[i, j] = 0
            elif idct2_block[i, j] > 255:
                idct2_block[i, j] = 255
    return idct2_block

def compress(blocks, F, d):

    # applico la DCT2 ai singoli blocchi
    # dell'immagine e successivamente idct2
    dct2_blocks = []
    max_var = 0.0
    max_var_block = None
    ret_index = 0
    idct2_blocks = []
    frequency_cut_block = []
    index = 0

    for block in blocks:
        dct2_block = Calcolous.dct2(block)
        index += 1
        var = np.var(block)
        if var >= max_var:
            max_var = var
            max_var_block = block
            ret_index = index

        dct2_blocks.append(dct2_block)

        # taglio le frequenze con
        # k + l maggiore di d
        cut_block = dct2_block
        for k in range(F):
            for l in range(F):
                if k + l >= d:
                    cut_block[k, l] = 0.0

        frequency_cut_block.append(cut_block)

        # calcolo la idct2
        idct2_block = Calcolous.idct2(cut_block)

        # eseguo le trasformazioni di intervallo
        idct2_transformed_block = make_transform(idct2_block, F)
        idct2_blocks.append(idct2_transformed_block)

    return idct2_blocks, max_var, max_var_block, ret_index

def make_compressed_img(idct2_blocks, F, image_width, image_height):

    # blocchi non tagliati vengono
    # salvati come intero
    num_blocchi_righe = image_height // F
    num_blocchi_col = image_width // F
    compressed_img = np.zeros((num_blocchi_righe * F, num_blocchi_col * F), dtype=float)

    index = 0
    for i in range(num_blocchi_righe):
        for j in range(num_blocchi_col):
            compressed_img[i * F:(i + 1) * F, j * F:(j + 1) * F] = idct2_blocks[index]
            index += 1

    return compressed_img
