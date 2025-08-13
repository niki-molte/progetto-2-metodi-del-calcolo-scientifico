import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt

np.set_printoptions(threshold=np.inf, linewidth=400)
import os
from core.my_dct2_and_idct2 import Calcolous


class Gui:

    def __init__(self, root):
        self.root = root
        self.root.title("Compressione Immagine")
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        # imposto il tema tkk e vado ad impostare
        # anche i font
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))

        # creo le variabili file_path, max_F, F, d e image.
        # max_F corrisponde alla massima dimensione
        # dell'immagine.
        self.file_path = None
        self.max_F = None
        self.F = None
        self.d = None
        self.image = None

        # istanzio il frame principale
        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        # aggiungo il pulsante per selezionare
        # il file, se premuto chiamo la funzione
        # apposita
        self.btn_select = ttk.Button(frame, text="Seleziona file BMP", command=self.__select_file)
        self.btn_select.grid(row=0, column=0, columnspan=2, sticky="ew", pady=10)

        # aggiungo label e textbox per il
        # parametro F
        ttk.Label(frame, text="Parametro F:").grid(row=1, column=0, sticky="w", padx=5)
        self.param1 = ttk.Entry(frame)
        self.param1.grid(row=1, column=1, sticky="ew", padx=5)

        # aggiungo label e textbox per il
        # parametro d
        ttk.Label(frame, text="Parametro d:").grid(row=2, column=0, sticky="w", padx=5)
        self.param2 = ttk.Entry(frame)
        self.param2.grid(row=2, column=1, sticky="ew", padx=5)

        # aggiungo il pulsante per avviare
        # la compressione
        self.btn_start = ttk.Button(frame, text="Avvia Compressione", command=self.__start_compression)
        self.btn_start.grid(row=3, column=0, columnspan=2, sticky="ew", pady=20)

        # aggiungo spazio alle colonne del layout
        # per centrare gli elementi.
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

    # gestisce l'apertura e la selezione del file .bmp
    # si apre il filedialog nella directory home.
    def __select_file(self):
        file_path = filedialog.askopenfilename(
            initialdir=os.path.expanduser("~"),
            filetypes=[("Bitmap Files", "*.bmp")],
            title="Seleziona un file BMP"
        )

        # se file path non è una stringa non vuota
        # ed è un file
        if file_path and os.path.isfile(file_path):
            self.file_path = file_path
            try:

                # apre l'immagine e legge la sua dimensione
                # per limitare F. Si presuppone che le immagini
                # siano quadrate
                with Image.open(file_path) as img:
                    self.image = img.copy()
                    if img.width <= img.height:
                        self.max_F = img.width
                    else:
                        self.max_F = img.height

                # se selezionato il file viene mostrato un
                # messaggio di correttezza
                messagebox.showinfo(
                    "File selezionato",
                    f"Hai selezionato:\n{os.path.basename(file_path)}\n"
                    f"Larghezza immagine: {self.max_F} px"
                )

            # se si scatena eccezione viene sollevato
            # l'errore e mostrato a schermo
            except Exception as e:
                messagebox.showerror("Errore", f"impossibile leggere l'immagine: {e}")
                self.file_path = None
                self.max_F = None

    def __check_input(self):

        # se il path non è valido
        # viene lanciata una dialog
        if not self.file_path:
            messagebox.showerror("Errore", "seleziona prima un file BMP!")
            return False

        # se i parametri inseriti non sono numeri
        # viene aperta una dialog
        try:
            self.F = int(self.param1.get())
            self.d = int(self.param2.get())
        except ValueError:
            messagebox.showerror("Errore", "i parametri devono essere numeri!")
            return False

        # se sono numeri allora controllo i loro
        # vincoli. Se c'è un problema viene lanciata una dialog
        if self.F <= 0:
            messagebox.showerror("Errore", "parametro F deve essere maggiore di 0!")
            return False
        if self.F > self.max_F:
            messagebox.showerror("Errore", f"parametro F non può superare {self.max_F}!")
            return False
        if not (0 <= self.d <= 2 * self.F - 2):
            messagebox.showerror("Errore", f"parametro d deve essere compreso tra 0 e {2 * self.F - 2}!")
            return False

        return True

    def __start_compression(self):

        if self.__check_input():

            # avviso che la compressione è stata avviata.
            messagebox.showinfo(
                "Avvio",
                f"Compressione avviata con:\n"
                f"File: {os.path.basename(self.file_path)}\n"
                f"F: {self.F}, d: {self.d}"
            )

            # carico l'immagine e la converto in scala di grigio
            # per ottenere una matrice 2D e la carico in numpy
            img = self.image.convert("L")
            pixel_matrix = np.array(img, dtype=float)

            # creo le sottomatrici di dimensione F
            # e nel caso scarto l'eccesso. In blocks
            # ci sono i blocchi FxF e in remainder
            # gli avanzi
            blocks = []
            remainder_blocks = []
            h, w = pixel_matrix.shape

            for i in range(0, h, self.F):
                for j in range(0, w, self.F):

                    # prendo la riga che va da i a i + F, se
                    # l'immagine non è divisibile con il blocco
                    # allora scarto. Questo è possibile grazie
                    # alla funzione min.
                    block = pixel_matrix[i:min(i + self.F, h), j:min(j + self.F, w)]

                    if block.shape == (self.F, self.F):
                        blocks.append(block)
                    else:
                        remainder_blocks.append(block)

            # applico la DCT2 ai singoli blocchi
            # dell'immagine e successivamente idct2
            dct2_blocks = []
            idct2_blocks = []
            frequency_cut_block =[]
            for block in blocks:
                dct2_block = Calcolous.dct2(block)
                dct2_blocks.append(dct2_block)

                cut_block = dct2_block
                for k in range(self.F):
                    for l in range(self.F):
                        if k + l >= self.d:
                            cut_block[k, l] = 0.0


                frequency_cut_block.append(cut_block)

                # arrotondo all'intero più vicino
                # le idct2 e sistemo i valori al
                # loro interno.
                idct2_block = np.round(Calcolous.idct2(cut_block))

                for i in range(self.F):
                    for j in range(self.F):
                        if idct2_block[i, j] < 0:
                            idct2_block[i, j] = 0
                        elif idct2_block[i, j] > 255:
                            idct2_block[i, j] = 255

                idct2_blocks.append(idct2_block)

            H, W = self.image.height, self.image.width

            # numero di blocchi pieni
            num_blocchi_righe = H // self.F
            num_blocchi_col = W // self.F

            compressed_img = np.zeros((num_blocchi_righe * self.F, num_blocchi_col * self.F), dtype=float)

            index = 0
            for i in range(num_blocchi_righe):
                for j in range(num_blocchi_col):
                    compressed_img[i * self.F:(i + 1) * self.F, j * self.F:(j + 1) * self.F] = idct2_blocks[index]
                    index += 1

            img1_array = np.array(Image.fromarray(pixel_matrix.astype(np.uint8)))
            img2_array = np.array(Image.fromarray(compressed_img.astype(np.uint8)))

            fig1 = plt.figure()
            plt.imshow(img1_array, cmap='gray')
            plt.title("Immagine originale")
            plt.axis('off')

            fig2 = plt.figure()
            plt.imshow(img2_array, cmap='gray')
            plt.title(f"Immagine compressa\nF: {self.F}, d: {self.d}")
            plt.axis('off')

            plt.show(block=False)
















if __name__ == "__main__":
    root = tk.Tk()
    app = Gui(root)
    root.mainloop()
