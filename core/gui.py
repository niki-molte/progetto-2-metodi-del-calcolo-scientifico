from tkinter import messagebox, ttk

from core.compression_utils import *
from core.file_utils import select_file
from core.plot_utils import *


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



    def __select_file(self):
        select_file(self)

    def __start_compression(self):
        if self.__check_input():
            messagebox.showinfo("Avvio", f"Compressione avviata con:\nF: {self.F}, d: {self.d}")
            img = self.image.convert("L")
            pixel_matrix = np.array(img, dtype=float)

            print(f"Suddivisione dell'immagine in blocchi {self.F}x{self.F}")
            blocks, _ = make_blocks(pixel_matrix, self.F)
            print("Calcolo della DCT2 e IDCT2 dell'immagine originale")
            idct2_blocks, dct2_blocks, var_img, var_block_img, index = compress(blocks, self.F, self.d)
            print("Ricostruzione dell'immagine compressa")
            compressed_img = make_compressed_img(idct2_blocks, self.F, self.image.width, self.image.height)

            print("Calcolo della DCT2 dell'immagine compressa")
            compressed_blocks, _ = make_blocks(compressed_img, self.F)
            compressed_idct2_blocks, compressed_dct2_blocks, var_compressed_img, var_block_compressed_img, compressed_index = compress(compressed_blocks, self.F, self.d)
            print("Creazione dei plot")
            make_imgs_plot(pixel_matrix, compressed_img, self.F, self.d)
            make_pixel_plot(var_img, blocks[compressed_index], var_compressed_img, compressed_idct2_blocks[compressed_index], compressed_index, self.image.width, self.F)


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