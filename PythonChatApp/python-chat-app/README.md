# Overview

This is a little chat app in python. If you are signed in with a nickname, you will see all future messages sent to the server until you log out.

I wanted to build this application becasue I'd never done anything with networking before. I wanted to expand my abilities.

To start the server, run `python server.py` from the command line, in the same folder 'server.py' is in. 'server.py' knows it's own IP address. In 'client.py', you will need to put the server's IP address in the `SERVER` variable at the bottom. Then run `python client.py` in from the folder 'client.py' is located in. (Note that because of the way the server's IP is determined, this may only work over a local network, or a VPN simulating a local network.)

When you start 'client.py', you will be prompted for a nickname.

{Provide a link to your YouTube demonstration.  It should be a 4-5 minute demo of the software running (you will need to show two pieces of software running and communicating with each other) and a walkthrough of the code.}

[Software Demo Video](http://youtube.link.goes.here)

# Network Communication

I used a client-server architecture. It communicates via TCP on port 5050.

Messages are strings, formated into utf-8.

# Development Environment

This program was developed using VSCode, written in python. It uses the built-in `socket`, `threading`, and `tkinter` modules.

# Useful Websites

Note that Tech with Tim's tutorial has some errors, including an unnessecary 'header' system, which itself expects a wastefully large number of bytes.

* ["Simple GUI Chat in Python" by NeuralNine on youtube](http://url.link.goes.here)
* ["Python Socket Programming Tutorial" by 'Tech With Tim' on Youtube](http://url.link.goes.here)
* ["Simple TCP Chat Room in Python" by 'NeuralNine' on Youtube]()

# Future Work

* I need to implement Direct Messsages,
* Without direct messages, the Game bot does not work.
* I need to implement a way to store what you've missed while logged out and give it to you.
* A method of nickname authentication.
