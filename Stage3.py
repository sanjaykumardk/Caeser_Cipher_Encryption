import tkinter as tk
from tkinter import filedialog
import sys


class CaesarCipher(tk.Frame):
    def __init__(self, root):
        self.colour1 = '#000022'
        self.colour2 = '#aba8a7'
        self.colour3 = '#e28413'

        # Include all letters, numbers, and common special characters
        self.letters = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ' + \
                       ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
        self.num_letters = len(self.letters)

        super().__init__(root, bg=self.colour1)

        self.main_frame = self
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        self.main_frame.columnconfigure(0, weight=1)
        self.render_widgets()

    def render_widgets(self):
        self.title = tk.Label(
            self.main_frame,
            bg=self.colour1,
            fg=self.colour2,
            font=('Herald', 22, 'bold'),
            text='Enter the data to Encrypt and Decrypt :'
        )

        self.title.grid(column=0, row=0, sticky=tk.EW, pady=35)

        self.text_widget = tk.Text(
            self.main_frame,
            bg=self.colour2,
            fg=self.colour1,
            selectbackground=self.colour1,
            selectforeground=self.colour2,
            font=('Herald', 17),
            height=5,
            padx=10,
            pady=10,
            highlightthickness=0,
            border=0
        )

        self.text_widget.grid(column=0, row=1, padx=100)

        self.key_label = tk.Label(
            self.main_frame,
            bg=self.colour1,
            fg=self.colour2,
            font=('Herald', 13),
            text=f'Key (1-{self.num_letters - 1}):',
            justify=tk.CENTER
        )

        self.key_label.grid(column=0, row=2, pady=(38, 10))

        self.key_entry_validation_command = self.register(self.key_entry_validation)
        self.key_entry = tk.Entry(
            self.main_frame,
            bg=self.colour2,
            fg=self.colour1,
            selectbackground=self.colour1,
            selectforeground=self.colour2,
            font=('Herald', 15),
            width=6,
            validate='key',
            validatecommand=(self.key_entry_validation_command, '%P')
        )

        self.key_entry.grid(column=0, row=3, pady=(0, 30))

        self.buttons_container = tk.Frame(self.main_frame, bg=self.colour1)
        self.buttons_container.columnconfigure(0, weight=1)
        self.buttons_container.columnconfigure(1, weight=1)
        self.buttons_container.columnconfigure(2, weight=1)

        self.buttons_container.grid(column=0, row=4, sticky=tk.NSEW, padx=100)

        self.button_encrypt = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Herald', 15, 'bold'),
            text='Encrypt',
            width=6,
            height=1,
            highlightthickness=0,
            border=0,
            state=tk.DISABLED,
            command=self.encrypt_command
        )

        self.button_encrypt.grid(column=0, row=0, ipadx=5, ipady=5)

        self.button_decrypt = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Herald', 15, 'bold'),
            text='Decrypt',
            width=6,
            height=1,
            highlightthickness=0,
            border=0,
            state=tk.DISABLED,
            command=self.decrypt_command
        )

        self.button_decrypt.grid(column=2, row=0, ipadx=5, ipady=5)

        # Add Save and Load buttons
        self.button_save = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Herald', 15, 'bold'),
            text='Save',
            width=6,
            height=1,
            highlightthickness=0,
            border=0,
            command=self.save_text
        )
        self.button_save.grid(column=3, row=0, ipadx=5, ipady=5)

        self.button_load = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Herald', 15, 'bold'),
            text='Load',
            width=6,
            height=1,
            highlightthickness=0,
            border=0,
            command=self.load_text
        )
        self.button_load.grid(column=4, row=0, ipadx=5, ipady=5)

        # Add Copy and Paste buttons
        self.button_copy = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Herald', 15, 'bold'),
            text='Copy',
            width=6,
            height=1,
            highlightthickness=0,
            border=0,
            command=self.copy_to_clipboard
        )
        self.button_copy.grid(column=5, row=0, ipadx=5, ipady=5)

        self.button_paste = tk.Button(
            self.buttons_container,
            bg=self.colour2,
            fg=self.colour1,
            activebackground=self.colour3,
            activeforeground=self.colour1,
            font=('Herald', 15, 'bold'),
            text='Paste',
            width=6,
            height=1,
            highlightthickness=0,
            border=0,
            command=self.paste_from_clipboard
        )
        self.button_paste.grid(column=6, row=0, ipadx=5, ipady=5)

        # Theme Menu
        self.theme_menu = tk.Menu(root)
        root.config(menu=self.theme_menu)
        self.theme_menu.add_command(label="Dark Theme", command=self.set_dark_theme)
        self.theme_menu.add_command(label="Light Theme", command=self.set_light_theme)

    def encrypt_decrypt(self, text, mode, key):
        result = []
        for char in text:
            if char in self.letters:
                old_index = self.letters.index(char)
                if mode == 'e':
                    new_index = (old_index + key) % self.num_letters
                elif mode == 'd':
                    new_index = (old_index - key) % self.num_letters
                result.append(self.letters[new_index])
            else:
                result.append(char)
        return ''.join(result)

    def key_entry_validation(self, value):
        if value == '':
            self.button_decrypt['state'] = tk.DISABLED
            self.button_encrypt['state'] = tk.DISABLED
            return True

        try:
            value = int(value)
        except ValueError:
            return False

        if value <= 0 or value >= self.num_letters:
            return False

        self.button_decrypt['state'] = tk.NORMAL
        self.button_encrypt['state'] = tk.NORMAL

        return True

    def encrypt_command(self):
        key = int(self.key_entry.get())
        text = self.text_widget.get('1.0', tk.END).strip()
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', self.encrypt_decrypt(text, 'e', key))

    def decrypt_command(self):
        key = int(self.key_entry.get())
        text = self.text_widget.get('1.0', tk.END).strip()
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', self.encrypt_decrypt(text, 'd', key))

    def save_text(self):
        text = self.text_widget.get('1.0', tk.END).strip()
        if not text:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write(text)

    def load_text(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                text = file.read()
                self.text_widget.delete('1.0', tk.END)
                self.text_widget.insert('1.0', text)

    def copy_to_clipboard(self):
        selected_text = self.text_widget.get('sel.first', 'sel.last')
        if selected_text:
            self.clipboard_clear()
            self.clipboard_append(selected_text)

    def paste_from_clipboard(self):
        text_from_clipboard = self.clipboard_get()
        self.text_widget.delete('1.0', tk.END)
        self.text_widget.insert('1.0', text_from_clipboard)

    def set_dark_theme(self):
        self.colour1 = '#000022'
        self.colour2 = '#fbf5f3'
        self.colour3 = '#e28413'
        self.apply_theme()

    def set_light_theme(self):
        self.colour1 = '#fbf5f3'
        self.colour2 = '#000022'
        self.colour3 = '#e28413'
        self.apply_theme()

    def apply_theme(self):
        self.main_frame.config(bg=self.colour1)
        self.title.config(bg=self.colour1, fg=self.colour2)
        self.text_widget.config(bg=self.colour2, fg=self.colour1,
                                selectbackground=self.colour1, selectforeground=self.colour2)
        self.key_label.config(bg=self.colour1, fg=self.colour2)
        self.button_encrypt.config(bg=self.colour2, fg=self.colour1,
                                   activebackground=self.colour3, activeforeground=self.colour1)
        self.button_decrypt.config(bg=self.colour2, fg=self.colour1,
                                   activebackground=self.colour3, activeforeground=self.colour1)
        self.key_entry.config(bg=self.colour2, fg=self.colour1,
                              selectbackground=self.colour1, selectforeground=self.colour2)
        self.buttons_container.config(bg=self.colour1)


if __name__ == "__main__":
    operating_system = sys.platform
    root = tk.Tk()
    caesar_cipher_app = CaesarCipher(root)
    root.title('Encrypt and Decrypt')

    if 'win' in operating_system:
        root.geometry('800x600')
    elif 'linux' in operating_system:
        root.geometry('800x620')
    elif 'darwin' in operating_system:
        root.geometry('800x620')

    root.resizable(width=False, height=False)
    root.mainloop()
