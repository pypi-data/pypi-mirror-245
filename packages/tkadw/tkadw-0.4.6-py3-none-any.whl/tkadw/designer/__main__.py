if __name__ == '__main__':
    from tkadw.windows.theme import Adwite
    from tkadw.designer.designer import AdwDesigner

    root = Adwite(default_theme="metro")

    designer = AdwDesigner(root)
    designer.row()

    root.animation()
    root.run()