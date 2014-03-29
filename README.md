CS145 PS 2-3
========

aka CS145 MP1


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

### APPLICATION LAYER PROTOCOL ###
* MESSAGE FORMAT
 * strings
 * client and server knows which is which
* INITIATE CONNECTION
 * server waits for 4 clients to connect
 * upon connection, client requests server to give him an ID
 * the client's ID is actually its index in the clients list of the server
 * server stores client's initial settings (including username)
 * a message (ready/not ready) is constantly sent to the connected clients
 * once ready, the game starts
 * if we have AI, we have timer
  * once the first client connects, timer starts 
  * timer:  2 mins.  if no one else connects, assume AI and start game
 * else if we have no AI, then we'd wait forever until there're 4 players
* DURING THE GAME
 * there is constant communication between the clients and the server
 * the client messages are always in accompanied by the client's respective ID
 * the client always receives messages from the server
  * client messages:
   * "nothin to do here"
   * "ball position"
   * "player settings"
  * what the client does upon receipt of the server's messages 
   * "nothin to do here"
   * "ball position"
   * "player settings"
   * "timer"
 * the server always receives the messages from the client
  * what the server does upon receipt of client messages:
   * "nothin to do here"
    * pass
   * "ball position"
    * stores it in the list of ball positions according to client's ID
    * the ID would serve as the index
    * resolves conflict by comparing the values of all ball status from the client
    * the different one would be the real value to be distributed
   * "player settings"
    * stores player settings
    * sends these settings each client
   * "timer"
  * server messages:
   * "nothin to do here"
   * "ball position"
   * "player settings"
   * "timer"

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