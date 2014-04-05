QUADPONG
========

Codera. Davalos. Pacumio.
--------

* CS145MP
* Second Semester AY 2013-2014 
* Instructor:  Edgar Felizmenio


#### Specifications ####
* See attached pdf

#### Important dates: ####
* 04 April 2014 (Fri) - Presentation
 * 3:20 PM
 * Deadline of the MP itself

#### Deliverables ####
* source code
* Documentation of the protocol
 * Message Format
 * Actions Taken by the client/server
* Documentation of the application
 * Instructions on how to build and run the application
 * Minimum requirements and dependencies


### Files and Directories ###
* assets/
 * contains the sounds, images, and fonts used in the game
* strawman/
 * contains all the dummy files, demonstrates our learning experiences
* CS 145 Problem Set 2-3.pdf
 * contains the specs of the project
* elements.py
 * contains the game elements
* gameconfig.py
 * contains the game configuration for the pong game
* pong.py
 * the client program
 * this is what the users should run
* pygameconfig.py
 * contains the pygame shiz of the game
* server.py
 * accepts clients (running pong.py)
 * serves as the channel for clients' exchange of information

### DEPENDENCIES ###
* The machines to run the programs here must have:  
 * Python 2.7.3
 * Pygame

### HOW TO RUN ###
* SERVER: run  a single `python server.py`
* CLIENT: run `python pong.py` four times

### PROTOCOL REQUIREMENTS ###
* [DONE] A connected user must have an identifier. Users that are connected to the same host must have  distinct identifiers.
* [DONE] A connected user must have the option to provide an alias/username. Users that are connected to the same host may have the same alias/username.
* [DONE] A connected user must be able to receive messages from other users that are connected on the same host.
* [DONE] A user must be able to send messages to all users, or to selected users.
* [DONE] Aside from aliases and messages, a user must also have the option to share other kinds of information (e.g. status messages).
* [DONE] A user must have the option to voluntarily disconnect.
* [DONE] A user must be notified when another user disconnects.

### What the APPLICATION LAYER PROTOCOL is responsible for: ###
* The types of messages exchanged, for example, request messages and response messages
* The syntax of the various message types, such as the fields in the message and how the fields are delineated
* The semantics of the fields, that is, the meaning of the information in the fields
* Rules for determining when and how a process sends messages and responds to messages


### APPLICATION LAYER PROTOCOL: QUADPONG ###
* SYNTAX
 * {header}{message}
 * {header}{ID}{message}
* SEMANTICS
 * headers:
   - "JOIN" : client connects to server, server assigns it ID
   - "DONE" : notification to the clients that they can now play
   - "STAT" : "status"; the header when sending messages essential to the game itself
   - "TIME" : client receives time update from SENDER
 * messages:
  * information on the player's paddle 
  * information on the player's influence on the ball
* RULES
  * The fields are joined into a single string 
  * This single string is sent to the server
  * The server sends to every other player the information received from one player
  * The client splits back the fields and uses it to update its copy of the game
