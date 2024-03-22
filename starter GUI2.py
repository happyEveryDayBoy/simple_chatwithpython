import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import time
import os
from storage import Storage  # Ensure this is correctly imported based on your project structure
from ds_messenger import DirectMessenger, DirectMessage  # Adjust imports as per your actual file structure

class Body(tk.Frame):
    def __init__(self, master, recipient_selected_callback=None):
        super().__init__(master)
        self.master = master
        self._contacts = {}  # Maps item_id to contact name
        self._chat_histories = {}  # Maps contact name to their chat history (list of messages)
        self._select_callback = recipient_selected_callback
        self._selected_contact = None
        self._draw() 

    def node_select(self, event):
        item_id = self.posts_tree.selection()[0]
        self._selected_contact = self._contacts[item_id]
        if self._select_callback:
            self._select_callback(self._selected_contact)
        self.display_chat_history()

    def insert_contact(self, contact: str):
        if contact not in self._contacts.values():
            item_id = self.posts_tree.insert('', 'end', text=contact)
            self._contacts[item_id] = contact
            self._chat_histories[contact] = []

    def add_message_to_history(self, contact: str, message: str):
        self._chat_histories[contact].append(message)
        if contact == self._selected_contact:
            self.display_chat_history()

    def display_chat_history(self):
        self.chat_history.configure(state='normal')
        self.chat_history.delete('1.0', tk.END)
        for message in self._chat_histories.get(self._selected_contact, []):
            self.chat_history.insert(tk.END, message + '\n')
        self.chat_history.configure(state='disabled')

    def _draw(self):
        posts_frame = tk.Frame(self, width=250)
        posts_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False)

        self.posts_tree = ttk.Treeview(posts_frame)
        self.posts_tree.pack(fill=tk.BOTH, side=tk.TOP, expand=True, padx=5, pady=5)
        self.posts_tree.bind("<<TreeviewSelect>>", self.node_select)

        self.chat_history = tk.Text(self, state='disabled', wrap='word')
        self.chat_history.pack(fill=tk.BOTH, side=tk.LEFT, expand=True, padx=5, pady=5)

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

        self.message_input = tk.Entry(self)
        self.message_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5, pady=5)

        send_button = tk.Button(self, text="Send", command=self._send_callback)
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)

class MainApp(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.storage = Storage(username="your_username")  # Adjust as needed
        self.master.title("ICS 32 Distributed Social Messenger")
        self.pack(fill=tk.BOTH, expand=True)
        self._draw()
        self.load_or_create_profile()
        self.messenger = DirectMessenger(
            dsuserver=self.storage.dsuserver, 
            username=self.storage.username, 
            password=self.storage.password,
        )
        self.master.protocol("WM_DELETE_WINDOW", self.on_close)  # Handle window close event

    def add_contact(self):
        new_contact_name = simpledialog.askstring("Add New Contact", "Enter the contact's name:")
        if new_contact_name:
            self.body.insert_contact(new_contact_name)
            # Add an empty chat history for the new contact
            self.body._chat_histories[new_contact_name] = []

    def send_message(self):
        message = self.footer.message_input.get()
        if message and self.body._selected_contact:
            self.messenger.send(message, self.body._selected_contact)  # Implement sending logic
            self.body.add_message_to_history(self.body._selected_contact, message)
            self.footer.message_input.delete(0, tk.END)
    def load_or_create_profile(self):
        filepath = "user_profile.dsu"
        if not os.path.exists(filepath):
            print("No existing profile found. Creating a new one for a new user.")
            # Initialize default values for a new profile
            self.storage.username = "new_user"  # Example username, consider prompting the user for this
            self.storage.password = "password"  # Example password, consider a more secure approach
            self.storage.dsuserver = "168.235.86.101"  # Default server address
            self.storage.data = []  # Initialize an empty list for messages
            # If your application requires, initialize other default settings here
            self.save_profile()  # Save the new profile with default values
        else:
            try:
                self.storage.load_profile(filepath)
                # Load chat histories and contacts from the profile
                for data in self.storage.data:
                    if data.recipient not in self.body._chat_histories:
                        self.body.insert_contact(data.recipient)
                    self.body._chat_histories[data.recipient].append(data.message)
            except Exception as e:
                print(f"Failed to load profile: {e}")
                messagebox.showerror("Error", "Failed to load user profile.")

    def save_profile(self):
        filepath = "user_profile"  # Define the path to your user profile file
        try:
            self.storage.save_profile('.',filepath)
        except Exception as e:
            print(f"Failed to save profile: {e}")
            messagebox.showerror("Error", "Failed to save user profile.")
    def on_close(self):
        for x,y in self.body._chat_histories.items():
            for message in y:
                d = DirectMessage()
                d.recipient = x
                d.message = message
                d.timestamp = time.time()
                self.storage.data.append(d)
        print(self.storage.data)
        self.save_profile()  # Optionally save profile after sending a message
        # Assume each message in chat history is a dictionary with 'contact', 'message', ...
        self.master.destroy()
    def _draw(self):
        self.body = Body(self, recipient_selected_callback=lambda contact: print(f"Selected: {contact}"))
        self.body.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.footer = Footer(self, send_callback=self.send_message, add_user_callback=self.add_contact)
        self.footer.pack(fill=tk.X, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("720x480")
    app = MainApp(root)
    root.mainloop()
