def run():
    from PySide6 import QtWidgets

    import sys

    from .app import skin
    from .main import Main

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")
    skin.apply(app)

    files = [file for file in sys.argv[1:]]
    main = Main(files=files)
    main.show()

    sys.exit(app.exec())
