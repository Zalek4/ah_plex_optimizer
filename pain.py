import os, sys
import zazzle
from tqdm import tqdm
import shutil
from utilities import AH_ASCII, AH_FILES, AH_VIDEO, AH_PROBE, log
from gui import AH_Main_Window
from PyQt6.QtWidgets import QApplication

# Initialize logging
zazzle.ZZ_Init.configure_logger(file_name="plex_optimizer", directory="C:/ah/github/ah_plex_optimizer")
log = zazzle.ZZ_Logging.log

if __name__ == "__main__":
    # Console blurb because go big or go home amirite
    AH_ASCII.print_intro_consol_blurb(text="THE PLEX OPTIMIZER", font="doom")
    print()

    # Step 2: Create the application object
    app = QApplication([])

    # Step 3: Create the main window
    window = AH_Main_Window()
    window.show()

    # Step 4: Start the application's event loop
    app.exec()