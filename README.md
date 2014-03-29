CS145 PS 2-3
========

aka CS145 MP1

### Files ###
* elements.py
 * contains the game elements
* proto4p.py
 * TODO: NETWORKING STUFF !!!!!
 * TODO: AI if ever a player quits
 * TODO: setting username
 * DONE: draw elements on arena
 * DONE: move players
 * DONE: move ball
 * DONE: scoring system
 * Nice-To-Have: powerups
  * ball multiply
  * lengthen/shorten paddles

## NETWORKING ##
* connect four clients to server
* each client must be notified about the connection of every other client



#### Specifications ####
* See attached pdf

#### Important dates: ####
* 27 March 2014 (Thurs) - Deadline of submission (online), 11:59PM
* 28 March 2014 (Fri) - Presentation

#### Deliverables ####
* source code
* Documentation of the protocol
 * Message Format
 * Actions Taken by the client/server
* Documentation of the application
 * Instructions on how to build and run the application
 * Minimum requirements and dependencies


What the APPLICATION LAYER PROTOCOL is responsible for:
The types of messages exchanged, for example, request messages and response
messages

The syntax of the various message types, such as the fields in the message and
how the fields are delineated

The semantics of the fields, that is, the meaning of the information in the fields

Rules for determining when and how a process sends messages and responds to
messages

• A connected user must have an identifier. Users that are connected to the same host must have 
distinct identifiers.
• A connected user must have the option to provide an alias/username. Users that are connected to
the same host may have the same alias/username.
• A connected user must be able to receive messages from other users that are connected on the 
same host.
• A user must be able to send messages to all users, or to selected users.
• Aside from aliases and messages, a user must also have the option to share other kinds of 
information (e.g. status messages).
• A user must have the option to voluntarily disconnect.
• A user must be notified when another user disconnects.