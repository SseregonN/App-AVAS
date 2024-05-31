import tkinter
import tkinter.filedialog
import tkinter.ttk
from customtkinter import *
from pygame import mixer
from pydub import AudioSegment
import tempfile
import os


    
class app:
    def __init__(self):
        
        self.couleur_1="#020f12"
        self.couleur_2="#05d7ff"
        self.couleur_3="#65e7ff"
        self.couleur_4="BLACK"

        self.fenetre = tkinter.Tk()
        self.fenetre.geometry('500x500')
        self.fenetre.title('SseregonN - Tkinter tutoriel')
        self.fenetre.resizable(height=False, width=False)
        self.fenetre.configure(background=self.couleur_1)
        self.fenetre.grid_rowconfigure(0, weight=1)
        self.fenetre.grid_rowconfigure(1, weight=1)
        self.fenetre.grid_rowconfigure(2, weight=1)
        self.fenetre.grid_rowconfigure(3, weight=1)

        #création des colonnes
        self.fenetre.grid_columnconfigure(0, weight=1)
        self.fenetre.grid_columnconfigure(1, weight=1)
        
    def choix_fichier(self):
        self.fichier_audio = tkinter.filedialog.askopenfilename(filetypes=[("Fichiers WAV", "*.wav")])
        self.music=MyMix(self.fichier_audio)
        if self.fichier_audio != "":
            self.setup_title()
            self.bar.stop()
            self.music.unload()
            self.music.load()

    #affichage du titre
    def setup_title(self):
        titre = self.fichier_audio.split("/")[-1] #music[0] est le chemin d'accès fichier_audio dans la fonction choix_fichier()
        nom_fichier=tkinter.Label(
            self.fenetre, 
            text=titre, 
            font=("Arial", 24, "bold"),
            fg="white",
            bg="black"
            )
        nom_fichier.grid(column=0, row=0, columnspan=2)

    def setup_menu(self):
        #config menu
        mon_menu = tkinter.Menu(self.fenetre)

        fichier = tkinter.Menu(mon_menu, tearoff=0)
        fichier.add_command(label="Ouvrir...", command=lambda: self.choix_fichier())
        fichier.add_command(label="Exporter", command=lambda: self.export(self.curseur.get()))

        help = tkinter.Menu(mon_menu, tearoff=0)
        help.add_command(label="Comment régler la vitesse ?")

        mon_menu.add_cascade(label="Fichier", menu=fichier)
        mon_menu.add_cascade(label="Help", menu=help)

        self.fenetre.config(menu=mon_menu)

    def setup_btn(self):
        btn_play = tkinter.Button(
            self.fenetre, 
            background=self.couleur_2,
            foreground=self.couleur_4,
            activebackground=self.couleur_3,
            activeforeground=self.couleur_4,
            highlightthickness=2,
            highlightbackground=self.couleur_2,
            highlightcolor="WHITE",
            width=13,
            height=2,
            border=0,
            cursor='hand1',
            font=("Arial", 16, "bold"),
            text="Play",
            command=lambda: self.music.fonction_lecture(self.bar),
            
            )
        
        btn_stop = tkinter.Button(
            self.fenetre, 
            text="Stop", 
            command=lambda: self.music.fonction_stop(self.bar),
            background=self.couleur_2,
            foreground=self.couleur_4,
            activebackground=self.couleur_3,
            activeforeground=self.couleur_4,
            highlightthickness=2,
            highlightbackground=self.couleur_2,
            highlightcolor="WHITE",
            width=13,
            height=2,
            border=0,
            cursor='hand1',
            font=("Arial", 16, "bold"),
            
            )
        btn_play.grid(
            column= 0, 
            row=1
            )
        btn_stop.grid(
            column=1, 
            row=1
            )

    def setup_progressbar(self):
        #barre de progression du fichier audio
        s=tkinter.ttk.Style()
        s.theme_use("alt")
        s.configure("TProgressbar", foreground="#4979DF", background="#4979DF", thickness=20)
        self.bar=tkinter.ttk.Progressbar(
            self.fenetre,
            mode="determinate",
            style="TProgressbar",
            length= 500
            )
        self.bar.grid(
            column=0, 
            row=2, 
            columnspan=2
            )
        
    #curseur pour la vitesse
    def setup_curseur(self):

        self.curseur=tkinter.Scale(
            self.fenetre,
            bd=0,
            bg=self.couleur_1,
            label="Vitesse du véhicule", 
            cursor="hand1",
            activebackground=self.couleur_3,
            highlightthickness=2,
            highlightbackground=self.couleur_1,
            highlightcolor="WHITE",
            fg="white",
            orient="horizontal", 
            from_=0, to=30, length=500, 
            font=("Arial", 16, "bold"), 
            command=lambda value: self.music.distorsion(value) #music[1] est la classe MyMix de music (cf. choix_fichier())
        )

        self.curseur.grid(column=0, row=3, columnspan=2)

    def export(self, value):
        destination_export=tkinter.filedialog.asksaveasfilename(filetypes=[("Fichiers WAV", "*.wav")])
        # audio=self.music.distorsion(value)
        audio = AudioSegment.from_file(self.fichier_audio)
        facteur_modification = 1 + (float(value) * 0.008)  # Modify based on scale
        new_freq = int(audio.frame_rate * facteur_modification)

        # Ensure new_freq is a positive value
        if new_freq <= 0:
            new_freq = 1  # Set to minimum valid frequency if result is non-positive

        audio_modifie = audio._spawn(audio.raw_data, overrides={'frame_rate': new_freq})
        if destination_export.split(".")[-1]=="wav":
            audio.export(destination_export, format="wav")
        else:
            audio.export(destination_export + ".wav", format="wav")

    def run(self):
        #tu vas mettre les init des éléments menu bbtn ...
        self.setup_menu()
        self.setup_btn()
        self.setup_progressbar()
        self.setup_curseur()
        self.fenetre.mainloop()

class MyMix:
    def __init__(self, path_to_file) -> None:
        self.temp_files = []  # Initialise la liste des fichiers temporaires
        self.path_to_file=path_to_file
        mixer.init()

    def load(self):
        mixer.music.load(self.path_to_file)

    def unload(self):
        mixer.music.unload()

    def fonction_lecture(self, bar):
        sound=mixer.Sound(self.path_to_file)
        mixer.music.play(loops=-1)
        #calcul du step de la barre
        playtime_en_ms=sound.get_length()*1000 #conversion en millisecondes
        ms_par_pourcentage=playtime_en_ms/100
        bar.start(int(ms_par_pourcentage))

    def fonction_stop(self, bar):
        mixer.music.stop()
        bar.stop()
        
        #efface les fichiers temporaires
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except PermissionError:
                pass  #ne le fait pas si le fichier est encore en cours d'utilisation
        self.temp_files = []

    def distorsion(self, value):
        audio = AudioSegment.from_file(self.path_to_file)
        facteur_modification = 1 + (float(value) * 0.008)  # Modify based on scale
        new_freq = int(audio.frame_rate * facteur_modification)

        # Ensure new_freq is a positive value
        if new_freq <= 0:
            new_freq = 1  # Set to minimum valid frequency if result is non-positive

        audio_modifie = audio._spawn(audio.raw_data, overrides={'frame_rate': new_freq})

        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            audio_modifie.export(temp_wav.name, format="wav")
            temp_wav_path = temp_wav.name

        mixer.music.load(temp_wav_path)
        mixer.music.play(loops=-1)
        
        self.temp_files.append(temp_wav_path)
        return audio_modifie

if __name__ == "__main__":
    fenetre = app()
    fenetre.run()
    