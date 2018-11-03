#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet.protocol import Protocol, Factory
from twisted.internet import reactor
from twisted.python import log

### Protocol Implementation

# Contain handler for diferent events

def GetUser (host,port,users):
    returnUser  = 0
    for user in users :
        if (host == user.host and port == user.port):
            returnUser = user
    return returnUser
        

class User ():
    def __init__ (self, ID, host, port, connectHost = 0, connectPort = 0, state = "wait"):
        self.host = host
        self.port = port
        self.id = ID
        self.connectPort = connectPort
        self.connectHost = connectHost
        self.state = state
        self.data = []
    def GetStringInf (self):
        return "ID:{0}, HOST:{1}, PORT:{2}, CONNECTION_ID:{3}, STATE:{4} {5}".format(self.id,self.host,self.port,self.id,self.connectHost,self.connectPort)
    def SetConnection(self,connectHost, connectPort):
        self.connectHost = connectHost
        self.connectPort = connectPort
    
class Echo(Protocol):
    def connectionMade(self):
        self.factory.userNum = self.factory.userNum + 1
        log.msg(self.factory.userNum)
        self.transport.write(b"ok")
        self.factory.users.append(User(self.factory.userNum,self.transport.getPeer().host,self.transport.getPeer().port))
        #print (self.factory.users[0].GetStringInf())
        self.transport.write(str(self.factory.userNum).encode())
    def dataReceived(self, data):
        log.msg(curentUser.GetStringInf())
        print ("IP{0} HOST {1}".format(self.transport.getPeer().host,self.transport.getPeer().port))
        curentUser = GetUser(self.transport.getPeer().host, self.transport.getPeer().port, self.factory.users)
        print(curentUser.GetStringInf())
        stringData = data.decode("utf-8")
        splitData = stringData.split(" ")
        if (curentUser.connectPort == 0 and curentUser.connectHost == 0):
        ### Create new connection 
            if (splitData[0] == "co"):
                for user in self.factory.users :
                    if (user.id == int(splitData[1])):
                        self.transport.write(b"ok")
                        curentUser.SetConnection(user.host,user.port)
                        user.SetConnection(curentUser.host,curentUser.port)
                        break
                else:
                    self.transport.write(b"er")
        else:
            print ("data save")
            curentUser.data.append(data)
            connectUser = GetUser(curentUser.connectHost,curentUser.connectPort,self.factory.users)
            for ch in connectUser.data:
                self.transport.write(ch)
                print (ch)
            connectUser.data = []
                
        """
        As soon as any data is received, write it back.
        """
        self.transport.write(b"ok")

# Data for work contain Factory
class GameFactory(Factory):
    def __init__ (self, userNum = 0):
        self.userNum = userNum
        self.users = [] 
        
def main():
    try:
        log.startLogging(open('logServ.log', 'w'))
        log.msg('Start')
        f = GameFactory()
        f.protocol = Echo
        reactor.listenTCP(8000, f)
        reactor.run()
    except:
        log.err()
        
if __name__ == '__main__':
    print ("start")
    main()
