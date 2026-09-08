import socket
import threading
import tkinter as tk
from ctypes import windll
import customtkinter as ctk
from CTkListbox import CTkListbox
import time

windll.shcore.SetProcessDpiAwareness(1)  # Setting Render Scale of the UI


class PyServer:  # Initializing pyserver
    """
    A class representing a server for handling connections and enumeration.

    Attributes:
        port (int): The port number on which the server listens for connections.
        connections (list): A list to store active connections.
        addresses (list): A list to store addresses of connected clients.
        methods (list): A list of enumeration methods.
    """

    def __init__(self):  # Initializing Class attributes
        """
        Initializes PyServer attributes.
        """
        self.port = 12345
        self.connections = []
        self.addresses = []
        self.methods = []

    def methodPrep(self, methods, conn, addr):  # Initializing message preparer
        """
        Prepares the selected methods for enumeration.

        Args:
            methods (list): A list of enumeration methods selected by the user.
            conn: The connection object representing the client connection.
            addr: The address tuple (IP address, port number) of the client.
        """
        if methods is not None:  # Checking if the methods are not empty
            for method in methods:  # Selecting each method from methods
                self.enumeration(method, conn, addr)  # Sending required information to run method
                time.sleep(1)  # Adding a delay so that commands are not confused

    def enumeration(self, data, conn, addr):  # Initializing enumeration method
        """
        Sends and receives relevant information to the clients for enumeration.

        Args:
            data: The data representing the selected enumeration method.
            conn: The connection object representing the client connection.
            addr: The address tuple (IP address, port number) of the client.
        """

        conn.send(data.encode("ascii"))  # Sending the method chosen
        data = conn.recv(20480)  # Retrieving the results from the enumeration

        if data:  # Checking if no data was received
            textbox.insert(
                tk.INSERT,
                f"{addr[0]}:{addr[1]}\n"
            )  # Adding the IP and Port to the results

            textbox.insert(
                tk.INSERT,
                data.decode("ascii") + "\n"
            )  # Adding results to the textbox

    def listener(self, conn, addr):  # Initializing listener
        """
        Listens for incoming connections and handles them.
        As well as generating relevant UI.

        Args:
            conn: The connection object representing the client connection.
            addr: The address tuple (IP address, port number) of the client.
        """

        os = conn.recv(1024)  # Retrieving OS information
        os = os.decode("ascii")  # Decoding OS information

        connected = True

        while connected:  # While a connection exists
            time.sleep(0.25)

            try:
                if listbox.get() is not None:
                    if f"{addr[0]}:{addr[1]}" in listbox.get():
                        # Checking if an IP has been selected
                        tabview.add(str(addr[1]))  # Adding the corresponding port to the tab viewer

                        # Creating the listbox containing enumeration methods
                        enumeration = CTkListbox(
                            master=tabview.tab(str(addr[1])),
                            width=240,
                            multiple_selection=True,
                            justify="center",
                            highlight_color="#5c008a",
                            hover_color="#aa00ff"
                        )

                        enumeration.pack(padx=5, pady=5)

                        if os == "Linux":  # Checking operating system type
                            # Initializing options for enumeration based on OS type
                            enumeration.insert(tk.END, "users")
                            enumeration.insert(tk.END, "pids")
                            enumeration.insert(tk.END, "suids")

                        else:
                            enumeration.insert(tk.END, "users")
                            enumeration.insert(tk.END, "pids")
                            enumeration.insert(tk.END, "ports")

                        # Initializing the send/save button to save/send
                        saveButton = ctk.CTkButton(
                            master=tabview.tab(str(addr[1])),
                            text="SEND",
                            hover_color="#aa00ff",
                            fg_color="#5c008a",
                            command=lambda: self.methodPrep(
                                enumeration.get(),
                                conn,
                                addr
                            )
                        )

                        saveButton.pack(padx=5, pady=5)
                        saveButton.place(relx=0.25, rely=0.7)

                    else:
                        tabview.delete(str(addr[1]))
                        # If the tab is not selected then delete

                else:
                    tabview.delete(str(addr[1]))
                    # If the tab is not selected then delete

            except Exception:
                continue

    def threads(self):  # Initializing threads
        """
        Initializes threads for handling incoming connections.
        """

        server = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )  # Initializing socket

        server.bind(
            ("", self.port)
        )  # Binding server to local host + port

        server.listen()  # Setting up listener

        while True:
            conn, addr = server.accept()  # Accepting incoming connection

            listbox.insert(
                tk.END,
                f"{addr[0]}:{addr[1]}"
            )  # Adding connected IP and Port to listbox

            thread = threading.Thread(
                target=self.listener,
                args=(conn, addr)
            )  # Initializing thread

            thread.start()  # Starting thread


if __name__ == "__main__":
    root = ctk.CTk()

    root.title("Server Console")  # Setting the application name
    ctk.set_appearance_mode("Dark")  # Setting the general appearance
    root.geometry(
        f"{900}x{450}"
    )  # Setting the height and width of the application

    # Initializing the IP multi-selection box
    listbox = CTkListbox(
        root,
        multiple_selection=True,
        height=360,
        width=140,
        justify="center",
        border_color="#aa00ff",
        highlight_color="#5c008a",
        hover_color="#aa00ff",
        border_width=3
    )

    listbox.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    listbox.grid(
        row=0,
        column=0,
        padx=30,
        pady=30,
        sticky="ew"
    )

    # Initializing the tab viewer for each selected IP
    tabview = ctk.CTkTabview(
        master=root,
        height=360,
        width=300,
        border_color="#aa00ff",
        segmented_button_selected_color="#5c008a",
        segmented_button_selected_hover_color="#5c008a",
        segmented_button_unselected_hover_color="#aa00ff",
        border_width=3
    )

    tabview.grid(
        row=0,
        column=1,
        padx=30,
        pady=30,
        sticky="ew"
    )

    # Initializing text box for enumeration results
    textbox = ctk.CTkTextbox(
        master=root,
        height=380,
        width=250,
        border_color="#aa00ff",
        border_width=3
    )

    textbox.grid(
        row=0,
        column=3,
        padx=30,
        pady=30
    )

    textbox.yview("end")

    serverSetup = PyServer()  # Initializing PyServer object

    uiThread = threading.Thread(
        target=serverSetup.threads
    )  # Initializing PyServer Thread

    uiThread.start()  # Starting PyServer

    root.mainloop()
