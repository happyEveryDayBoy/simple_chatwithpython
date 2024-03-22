import tkinter as tk
from tkinter import ttk, simpledialog

class Body(tk.Frame):
    def __init__(self, master, recipient_selected_callback=None):
        super().__init__(master)
        self.master = master
        self._contacts = {}  # Store contacts in a dictionary
        self._select_callback = recipient_selected_callback
        self._draw()

    def node_select(self, event):
        item_id = self.posts_tree.selection()[0]  # Get the ID of the selected item
        if item_id in self._contacts:
            entry = self._contacts[item_id]
            if self._select_callback is not None:
                self._select_callback(entry)

    def insert_contact(self, contact: str):
        if contact not in self._contacts.values():
            item_id = self.posts_tree.insert('', 'end', text=contact)
            self._contacts[item_id] = contact  # Use Treeview item ID as key

    def _draw(self):
        posts_frame = tk.Frame(self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)

        # Message history area
        self.chat_history = tk.Text(self, state='disabled', wrap='word')
        self.chat_history.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

        # Scrollbar for chat history
        scrollbar = tk.Scrollbar(self, command=self.chat_history.yview)
        scrollbar.pack(side=tk.LEFT, fill='y')
        self.chat_history['yscrollcommand'] = scrollbar.set

class Footer(tk.Frame):
    def __init__(self, master, send_callback=None, add_user_callback=None):
        super().__init__(master)
        self.master = master
        self._send_callback = send_callback
        self._add_user_callback = add_user_callback
        self._draw()

    def _draw(self):
        self.pack(fill=tk.X)
        add_user_button = tk.Button(self, text="Add User", command=self._add_user_callback)
        add_user_button.pack(side=tk.LEFT, padx=5, pady=5)

        send_button = tk.Button(self, text="Send", command=self._send_callback)
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)

        # Message input area
        self.message_input = tk.Entry(self)
        self.message_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5, pady=5)

class MainApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.master.title("ICS 32 Distributed Social Messenger")
        self.pack(fill=tk.BOTH, expand=True)
        self._draw()

    def add_contact(self):
        new_contact_name = simpledialog.askstring("Add New Contact", "Enter the contact's name:")
        if new_contact_name:
            self.body.insert_contact(new_contact_name)

    def send_message(self):
        message = self.footer.message_input.get()
        if message:
            # Display the message in chat history (placeholder logic)
            self.body.chat_history.configure(state='normal')
            self.body.chat_history.insert('end', message + '\n')
            self.body.chat_history.configure(state='disabled')
            # Clear the input field
            self.footer.message_input.delete(0, 'end')
            # Here you would also handle sending the message through your backend

    def _draw(self):
        self.body = Body(self)
        self.body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.footer = Footer(self, send_callback=self.send_message, add_user_callback=self.add_contact)
        self.footer.pack(fill=tk.X, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("720x480")
    app = MainApp(root)
    root.mainloop()
