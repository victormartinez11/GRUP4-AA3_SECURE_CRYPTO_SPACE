import customtkinter as ctk
import src.ui.login as login_ui
from src.core.file_manager import create_directory
#MENU
def main():
    create_directory("data/vaults")

    app = ctk.CTk()
    login_ui.setup_login_ui(app)
    app.mainloop()


main()
