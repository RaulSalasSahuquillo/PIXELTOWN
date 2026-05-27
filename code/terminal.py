def terminalbeggining():
    print("""
██████╗ ██╗██╗  ██╗███████╗██╗  ████████╗ ██████╗ ██╗    ██╗███╗   ██╗
██╔══██╗██║╚██╗██╔╝██╔════╝██║  ╚══██╔══╝██╔═══██╗██║    ██║████╗  ██║
██████╔╝██║ ╚███╔╝ █████╗  ██║     ██║   ██║   ██║██║ █╗ ██║██╔██╗ ██║
██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║     ██║   ██║   ██║██║███╗██║██║╚██╗██║
██║     ██║██╔╝ ██╗███████╗███████╗██║   ╚██████╔╝╚███╔███╔╝██║ ╚████║
╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝    ╚═════╝  ╚══╝╚══╝ ╚═╝  ╚═══╝
                   PIXELTOWN OFFICIAL TERMINAL.
          
          Welcome to the PIXELTOWN terminal!
""")
    while True:
        language = input("What language do you want to play the game?\n- Spanish (ES)\n- English (EN)\n> ")
        lang_clean = language.strip().lower()
        if lang_clean in ("es", "español", "spanish"):
            from main_es import main
            main()
            break
        elif lang_clean in ("en", "ingles", "english", "inglés"):
            from main_en import main
            main()
            break
        else:
            print("Invalid option. Please write 'ES' or 'EN'.")