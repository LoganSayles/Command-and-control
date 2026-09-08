
# Command and Control Server

This application was retrieved via old university work and is a re-creation of such work for the point of demonstrating what I had completed during my time in education.

This tool, is a proof of concept, based upon the idea of command on control severs. Incorporating up to 4 enumeration methods across 2 seperate operating systems, this tool aims to extract information from a client system.

## Getting Started

Start by cloning this github repository. To do this either download the zip file or if you're using a CLI enter the following command:

```bash
git clone https://github.com/LoganSayles/Command-and-control.git
```

### Prerequisites

To use this software you will need some required python modules, to quickly install the required modules use the following command:

```
pip3 install -r requirements.txt
```

## Running the tests

To run the tests that come with this software run the following command:

```
python3 unit-tests.py
```

## Deployment

To begin initialise the server using:

```
python3 main.py
```

Upon creation of the server, upload and run "client.py" on the machine of a potential victim using:

```
python3 client.py
```

This creates a continuous scan, awaiting a connection with the server.

### UI

Upon connection with the client, the left side should display machines that are connected to your server in the format IP+Port.

In the center, it displays enumeration methods are possible for that system. For windows 3 Pre-Defined enumeration methods have been created and for linux there are 4.

On the left, it display the communication from the client to the server. Displaying the outputs including open ports and currently running services.

### Usage

To begin using the application, click the desired machine to enumerate information from.

Then select what methods you would like to employ.

Finally, click "SEND", this will send the relevent enumeration methods you would like to employ on the client machine and this will be communicated back via the right hand side menu.

### Methods

**users** ~ This function enumerates the user account visibile from the current user on that system.

**pids** ~ This *windows specific function* enumerates all processes on the current system.

**suids** ~ This *linux specific function* enumerates all SUID Binaries viewable on the current system.

**ports** ~ This function enumerates all the open ports on the current system.

## Authors

* **Logan Sayles** - *Primary Contributer*
