from thonny import get_workbench
from tkinter import filedialog
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QWidget
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit


def addCode(filename):
    code = '''from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QApplication,QMessageBox,QTableWidget,QTableWidgetItem

# Module s'exécute lors du clic sur le bouton
def Nom_Module():
    # traitement

app = QApplication([])
windows = loadUi ("{}")
windows.show()
windows.Nom_Bouton.clicked.connect (Nom_Module)
app.exec_()'''.format(filename)
    get_workbench().get_editor_notebook().get_current_editor().get_code_view().text.insert('insert', code)


def setTexte(widgetname):
    code = 'windows.{}.setText("Message")'.format(widgetname)
    get_workbench().get_editor_notebook().get_current_editor().get_code_view().text.insert('insert', code)


def getTexte(widgetname):
    code = 'windows.{}.text()'.format(widgetname)
    get_workbench().get_editor_notebook().get_current_editor().get_code_view().text.insert('insert', code)


def ClearTexte(widgetname):
    code = 'windows.{}.clear()'.format(widgetname)
    get_workbench().get_editor_notebook().get_current_editor().get_code_view().text.insert('insert', code)


def AddButton(widgetname):
    code = 'windows.{}.clicked.connect (Nom_Module)'.format(widgetname)
    get_workbench().get_editor_notebook().get_current_editor().get_code_view().text.insert('insert', code)


def display_widgets(filename):
    windows = loadUi(filename)
    widgets = windows.findChildren(QWidget)
    for widget in widgets:
        command_id = f"set_{widget.objectName()}"
        par = str(widget.objectName())

        if(isinstance(widget, QLabel)):
            get_workbench()._publish_command("Walid_01", "PyQT", "               Label {}".format(
                widget.objectName()), None, tester=lambda: False, group=41)
            ch = f"Modifier le texte du label {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: setTexte(par),
                group=41)
            ch = f"Récupérer le texte du label {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: getTexte(par),
                group=41)
            ch = f"Effacer le texte du label {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: ClearTexte(par),
                group=41)
        elif (isinstance(widget, QLineEdit)):
            get_workbench()._publish_command("Walid_02", "PyQT", "              LineEdit : {}".format(
                widget.objectName()), None, tester=lambda: False, group=42)
            ch = f"Modifier le texte du LineEdit {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: setTexte(par),
                group=42)
            ch = f"Récupérer le texte du LineEdit {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: getTexte(par),
                group=42)
            ch = f"Effacer le texte du LineEdit {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: ClearTexte(par),
                group=42)
        elif (isinstance(widget, QPushButton)):
            get_workbench()._publish_command("Walid_03", "PyQT", "              Bouton {}".format(
                widget.objectName()), None, tester=lambda: False, group=43)
            ch = f"Ajouter evenement Clic au Bouton {widget.objectName()}"
            get_workbench()._publish_command(
                command_id,
                "PyQT",
                ch,
                lambda: AddButton(par),
                group=43)


def open_gui():
    global ch
    filename = filedialog.askopenfilename(
        initialdir="C:/Bac2024",  # Répertoire par défaut
        title="Sélectionnez un fichier",
        filetypes=(("Fichiers d'interface utilisateur", "*.ui"), ("Tous les fichiers", "*.*"))  # Type de fichier
    )
    ch = filename
    if filename:
        addCode(filename)
    display_widgets(filename)


def load_plugin() -> None:

    get_workbench().add_command("open_gui", "PyQT", "Ouvrir Interface graphique", open_gui, group=40)
