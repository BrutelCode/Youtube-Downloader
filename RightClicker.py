from tkinter import Menu

# Create a class for Right_Click that enables a menu for Cut, Copy and Paste
class RightClicker:
    def __init__(self, e):
        commands = ["Cut", "Copy", "Paste"]
        menu = Menu(None, tearoff=0, takefocus=0)

        for txt in commands:
            menu.add_command(label=txt, command=lambda e=e, txt=txt: self.click_command(e, txt))

        menu.tk_popup(e.x_root + 40, e.y_root + 10, entry="0")

    def click_command(self, e, cmd):
        e.widget.event_generate(f'<<{cmd}>>')