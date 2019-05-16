#!/usr/bin/python3
import tornado.ioloop
import tornado.websocket
import onionGpio
import time

clients = [] # list of the connected clients

red_button = onionGpio.OnionGpio(1)
green_button = onionGpio.OnionGpio(3)
blue_button = onionGpio.OnionGpio(0)

# global variables tracking state of buttons 
red_s = 0
green_s = 0
blue_s = 0

# function used to check the button states and if they have
# changed send a message to all connected clients
def check_buttons():
    global red_s
    global green_s
    global blue_s

    # red button
    if(red_s != int(red_button.getValue())):
        red_s = int(red_button.getValue());
        for client in clients:
            client.write_message("r"+str(red_s))      

    # green button
    if(green_s != int(green_button.getValue())):
        green_s = int(green_button.getValue());
        for client in clients:
            client.write_message("g"+str(green_s))      

    # blue button
    if(blue_s != int(blue_button.getValue())):
        blue_s = int(blue_button.getValue());
        for client in clients:
            client.write_message("b"+str(blue_s))      

class IoTWebsocket(tornado.websocket.WebSocketHandler):

    def check_origin(self, origin):
        return True

    def open(self):
        print("Client connected")
        clients.append(self)

    def on_message(self, message):
        print("Received Message:  " + message)
        for client in clients:
            print("\twriting a response back to the client...")
            client.write_message("Hi back")

    def on_close(self):
        print("Client disconnected")
        clients.remove(self)

def make_app():
    return tornado.web.Application([
        (r"/", IoTWebsocket),
    ])

if __name__ == "__main__":
    print("Starting server... ")

    red_button.setInputDirection()
    green_button.setInputDirection()
    blue_button.setInputDirection()

    # create the periodic callback loop that checks the buttons
    checker = tornado.ioloop.PeriodicCallback(check_buttons, 50)
    checker.start()
    
    app = make_app()
    app.listen(8888)
    print("Server is running and awaiting connections...")
    tornado.ioloop.IOLoop.current().start()
