import socket
import sys
import time
sys.path.append('./')
import lib
import random
import atexit

def exit_handler(s:socket):
    print('Exit,closing the socket')
    s.close()
    
def run():
    
    # set up cli server port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    atexit.register(exit_handler,s=s)
    # s.setblocking(0)
    print('buffersize: ',s.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF
))
    s.connect((lib.SERVER,lib.CLI_PORT))
    # accept connection and run 
    #handshake
    lib.send(s,'8')
    while(1):
        
        try:
            #for selcect
            # print("send Dummy data")
            # # s.send(b"Data")
            # if (random.random()>0.5):
            #     lib.send(s,"Data")
            # else:
            #     lib.send(s,"Data2")
            #for select
            
            if (random.random()>0.5):
                msg = 'Data'
            else:
                msg = 'Data2'
            msg = lib.msg(msg,'None').toJSON()
            lib.send(s,msg)
            print('sent')
            
        except socket.error as error:
            print(error)
        
        #for select
        # try:
        #     data = lib.recv(s)
        #     print(data)
        # except:
        #     print('cannot recv respond, socket shld be idk?')     
        #for select
        
        try:   
            end = time.time()-start
            print('update interval : ',end)
        except:
            pass
        # try:
        #     print(lib.recvThenAck(s))
        #     print('recv then ack')
        # except socket.error as error:
        #     print(error)
        start = time.time() 
       
        
if __name__=='__main__':
    run()