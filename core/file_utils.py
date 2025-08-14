from tkinter import filedialog, messagebox
from PIL import Image
import os

def select_file(gui_instance):

    # gestisce l'apertura e la selezione del file .bmp
    # si apre il filedialog nella directory home.
    file_path = filedialog.askopenfilename(
        initialdir=os.path.expanduser("~"),
        filetypes=[("Bitmap Files", "*.bmp")],
        title="Seleziona un file BMP"
    )

    # se file path non è una stringa non vuota
    # ed è un file
    if file_path and os.path.isfile(file_path):
        gui_instance.file_path = file_path
        try:

            # apre l'immagine e legge la sua dimensione
            # per limitare F. Si presuppone che le immagini
            # siano quadrate
            with Image.open(file_path) as img:
                gui_instance.image = img.copy()
                gui_instance.max_F = min(img.width, img.height)

            # se selezionato il file viene mostrato un
            # messaggio di correttezza
            messagebox.showinfo(
                "File selezionato",
                f"Hai selezionato:\n{os.path.basename(file_path)}\n"
                f"Larghezza immagine: {gui_instance.max_F} px"
            )

        # se si scatena eccezione viene sollevato
        # l'errore e mostrato a schermo
        except Exception as e:
            messagebox.showerror("Errore", f"impossibile leggere l'immagine: {e}")
            gui_instance.file_path = None
            gui_instance.max_F = None
