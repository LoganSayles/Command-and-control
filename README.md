# Command and Control Server

This application was retrieved via old university work and is a re-creation of such work for the purpose of demonstrating what I had completed during my time in education.

This tool is a proof of concept, based upon the idea of command on control severs. Incorporating 3 enumeration methods across 2 separate operating systems, this tool aims to extract information from a client system.

**For the sake of testing, this application only works intentionally on the local system, and the server will be initialised on localhost port 12345**

## Getting Started

Start by cloning this GitHub repository. To do this, either download the zip file or if you're using a CLI enter the following command:

```bash
git clone https://github.com/LoganSayles/Command-and-control.git
```
<p align="center"><img width="770" height="181" alt="1" src="https://github.com/user-attachments/assets/a00083ad-fb29-4c1e-b799-da1782fd7a9b" /></p>

### Prerequisites

To use this software, you will need some required Python modules. To quickly install the required modules, use the following command:

```
pip3 install -r requirements.txt
```

<p align="center"><img width="770" height="181" alt="2" src="https://github.com/user-attachments/assets/fcf77de2-1772-48a1-82f6-923bfafb6068" /></p>

## Running the tests

To run the tests that come with this software, run the following command:

```
python3 unit-tests.py
```

<p align="center"><img width="800" height="181" alt="3" src="https://github.com/user-attachments/assets/9c9bacf7-9bdf-4e71-bea4-03a72bef82ef" /></p>

## Deployment

To begin, initialise the server using:

```
python3 main.py
```

Upon creation of the server, upload and run "client.py" on the machine of a potential victim using:

```
python3 client.py
```

This creates a continuous scan, awaiting a connection with the server.

## UI

Upon connection with the client, the left side should display machines that are connected to your server in the format IP+Port.

<p align="center"><img width="175" height="385" alt="image" src="https://github.com/user-attachments/assets/915ef0e8-a1c5-48bd-90a7-55d248a5fcb4" /></p>

In the center, it displays the enumeration methods possible for that system. For Windows 3, pre-defined enumeration methods have been created, and for Linux there are 4.

<p align="center"><img width="315" height="362" alt="image" src="https://github.com/user-attachments/assets/fc9d9769-68c0-4091-8681-8e3d33990a79" /></p>

On the left, it displays the communication from the client to the server. Displaying the outputs, including open ports and currently running services.

<p align="center"><img width="260" height="389" alt="image" src="https://github.com/user-attachments/assets/dbb1c647-8390-430d-85de-10d52dda0d36" /></p>

## Usage

To begin using the application, click the desired machine to enumerate information from.

Then select what methods you would like to employ.

<p align="center"></p>

Finally, click "SEND"; this will send the relevant enumeration methods you would like to employ on the client machine, and this will be communicated back via the right-hand side menu.

<p align="center"><img width="800" height="400" alt="4" src="https://github.com/user-attachments/assets/68fe03c2-e73b-43bf-8e03-d07c05f1f942" /></p>

## Methods

**users** ~ This function enumerates the user accounts visible from the current user on that system.

**pids** ~ This *windows specific function* enumerates all processes on the current system.

**suids** ~ This *Linux-specific function* enumerates all SUID Binaries viewable on the current system.

**ports** ~ This function enumerates all the open ports on the current system.

## Authors

* **Logan Sayles** - *Primary Contributer*
