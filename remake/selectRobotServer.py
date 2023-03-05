import socket
import select
import time
import sys
sys.path.append('./')
import lib
if __name__ == '__main__':
    # create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # bind the socket to a specific address and port
    server_socket.bind(('192.168.1.83', lib.ARTEC_PORT))

    # listen for incoming connections
    server_socket.listen(1)

    # list of sockets to monitor
    sockets_list = [server_socket]

    # dictionary of connected clients
    clients = {}

    print('Server started, waiting for connections...')

    while True:
        
        start = time.time()
        #change to just pass in robot 
        # use select to monitor the sockets
        read_sockets, write_sockets, error_sockets = select.select(sockets_list, [], [],0)
        # print('sockList',sockets_list)
        sock:socket.socket
        
        if len(read_sockets)>0:
            try:
                print('Reading from these ports',[s.getpeername() for s in read_sockets])
            except:
                pass
        for sock in read_sockets:
            
            # if a new connection is made
            if sock == server_socket:
                client_socket, client_address = server_socket.accept()
                print()
                print(f'New connection from {client_address}')
                # get buffer
                # print('buffersize:',client_socket.getsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF))
                print('****************soocket info****************')
                sock.setblocking(0)
                sock.settimeout(0.5)
                client_socket.settimeout(0.2)
                print('timeout:',sock.gettimeout())
                print('buffersize:',sock.getsockopt( socket.SOL_SOCKET,socket.SO_RCVBUF
    ))
                print('BLocking status:',sock.getblocking())
                
                print('****************soocket info****************')
                #if reconnect at diff ports
                
                for addr in clients.items():
                    if addr[0] == client_address[0]:
                        del addr
                        print('it is a reconnect connection , old is deleted')
                
                # add the client socket to the list of sockets to monitor
                sockets_list.append(client_socket)
                # client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVTIMEO,0.2)
                
                
                # add the client to the dictionary of connected clients
                # {sockobj:ipaddr}
                clients[client_socket] = client_address
                print('new socket is added into  dictionary')
            else:
                # if an existing client sends data
                try:
                    
                    data = sock.recv(1024,socket.MSG_PEEK)
                    print('stuck here?')
                    if data:
                        # # send a response to the client
                        # sock.send(b'ACK')
                        # print('wait recv')
                        try:
                            # print(sock.recv(1024).decode('UTF-8'))
                            lib.recv(sock)
                            
                        except socket.error as error:
                            if(TimeoutError):
                                print('timeout')
                                # raise TimeoutError
                            raise TimeoutError
                        print('recved')
                        write_sockets.append(sock)
                    else:
                        raise TimeoutError
                except socket.error as error:
                    print(error)
                    # if there is an error, remove the socket from the list of sockets to monitor
                    if sock in sockets_list:
                        sockets_list.remove(sock)
                    # remove the client from the dictionary of connected clients
                    print('remove client',sock)
                    sock.close()
                    del clients[sock]
        if(len(write_sockets)>0):
            print('socket to write:',[s.getpeername() for s in write_sockets])
            
        for sock in write_sockets: 
            try:
                #1) get action from server 
                #2) respond back to car 
                lib.sendline(sock,'ack') 
            except socket.error as error:
                print(error)
            
        end = time.time()-start
        if len(write_sockets)>0:
            print('Cycle Time: ', end)
            
            
            
             

                
