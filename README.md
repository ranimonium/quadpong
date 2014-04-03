QUADPONG
========

CS145MP.


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


### Files ###
* elements.py
 * contains the game elements
* server.py
 * accepts clients (running pong.py)
 * serves as the channel for clients' exchange of information
* pong.py
 * the client program
 * this is what the users should run

### DEPENDENCIES ###
* The machines to run the programs here must have:  
 * Python 2.7.3
 * Pygame

### HOW TO RUN ###
* SERVER: run "python server.py"
* CLIENT: run "python pong.py"

### PROTOCOL REQUIREMENTS ###
* [DONE] A connected user must have an identifier. Users that are connected to the same host must have  distinct identifiers.
* [DONE] A connected user must have the option to provide an alias/username. Users that are connected to the same host may have the same alias/username.
* [DONE] A connected user must be able to receive messages from other users that are connected on the same host.
* [DONE] A user must be able to send messages to all users, or to selected users.
* [TODO] Aside from aliases and messages, a user must also have the option to share other kinds of information (e.g. status messages).
* [TODO] A user must have the option to voluntarily disconnect.
* [TODO] A user must be notified when another user disconnects.

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
  * "JOIN" : client connects to server, server assigns it ID
  * "DONE" : notification to the clients that they can now play
  * "STAT" : "status"; the header when sending messages essential to the game itself
 * messages:
  * information on the player's paddle 
  * information on the player's influence on the ball
* RULES
  * The fields are joined into a single string 
  * This single string is sent to the server
  * The server sends to every other player the information received from one player
  * The client splits back the fields and uses it to update its copy of the game