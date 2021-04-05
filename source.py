"""
Where solution code to Assignment should be written.  No other files should
be modified.

https://docs.python.org/3/library/stdtypes.html
https://docs.python.org/3/library/socket.html#socket.socket.settimeout
https://docs.python.org/3/library/stdtypes.html
https://docs.python.org/3/library/struct.html
"""

import socket
import io
import time
import typing
import struct
import assignment4
import assignment4.logging


def send(sock: socket.socket, data: bytes):
    """
    Implementation of the sending logic for sending data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.
        data -- A bytes object, containing the data to send over the network.
    """

    # Naive implementation where we chunk the data to be sent into
    # packets as large as the network will allow, and then send them
    # over the network, pausing half a second between sends to let the
    # network "rest" :)

    """
    Ideas:

    - need to implement fin???

    - struct module
    - struct.unpack()
    - see = fin .....

    - I will just put a fin message in as the last 5 or something similar

    
    """

    #from the skeleton code (subtract 1 becuase that is our sequnence number)
    offsets = range(0, len(data), assignment4.MAX_PACKET - 1)
    chunk_size = assignment4.MAX_PACKET - 1

    #need to keep track of the number of packets we are sending
    packet_number = 0

    #default timeout is set to 1 second
    timeout_counter_updated = 1

    #go through every chunk
    for chunk in [data[i:i + chunk_size] for i in offsets]:

        #we need to convert the sequence numbers to bytes
        #got error messages when I kept the error messages 
        sequence_number = packet_number.to_bytes(1, byteorder='little')
        #sequence_number2 = struct.pack('hh1', packet_number)

        while True:  
            #try catch
            try:

                #need to keep track of our timeout (default is 1 second)
                timeout_counter = timeout_counter_updated
                print("timeout counter ", timeout_counter)

                #need to set the timeout
                sock.settimeout(timeout_counter)
                
                #we initiate our timeout counter to be 1 seconds
                sock.settimeout(timeout_counter) 

                #starts at the current time
                start = time.time()

                #send the sequence_number + chunk
                sock.send(sequence_number + chunk)

                print("sequence_number: ", sequence_number)
                #print("sequence_number2: ", sequence_number2)

                #ack just the header that we are looking at
                ack = sock.recv(1)
                print("ack: ", ack)

                #check to see if the data that came back matches what we sent
                if ack == sequence_number:
                    print("We recieved the chunk sucessfully!")
                    #if the data is what we are looking for, we break out
                    break
                else:
                    #else, re resend the sequence number and the chunk
                    print("ack does not match! ---- resend")
                    sock.send(sequence_number + chunk)
                    
            except socket.timeout:
                    #if there is a timeout, then resend the chunk
                    sock.send(sequence_number + chunk)
                    print("timeout! ---- resend")
                    continue


        #ending time
        end = time.time()

        #total time
        total = end - start

        #RTT time ||| estimated RTT * 4
        timeout_counter_updated = total * 4

        #increment the packet number because we have moved to the next packet
        packet_number += 1
        print("packet number: ", packet_number)
        print("\n")

        #implement fin ack ???????



        

def recv(sock: socket.socket, dest: io.BufferedIOBase) -> int:
    """
    Implementation of the receiving logic for receiving data over a slow,
    lossy, constrained network.

    Args:
        sock -- A socket object, constructed and initialized to communicate
                over a simulated lossy network.

    Return:
        The number of bytes written to the destination.
    """
    # Naive solution, where we continually read data off the socket
    # until we don't receive any more data, and then return.

    #from the skeleton code, to keep track of the number of bytes
    num_bytes = 0

    #the previous sequence gets initialized as 0 (nothing)
    prev_sequence = 0
    
    while True:
        #need to get the data from the socket
        data = sock.recv(assignment4.MAX_PACKET)

        #if there is no data, that means we have no data,
        #so we break out of the loop
        if not data:
            break
        
        #if there is still data
        else:

            #we need to send back the data to compare
            sequence_number = data[0:1]

            #send the header info (this is basically an ack of the data
            #that we just recieved)
            sock.send(sequence_number)

            #print statements to compare
            print("prev_sequence: ", prev_sequence)
            print("sequence_number: ", sequence_number)

            #this is to make sure that we do not append the data length
            #we do not append the data when the previous sequence is the current sequence
            if (prev_sequence == sequence_number):
                print("do not append length")
                continue

        data_length = len(data)

        #subtract 1 from the data length because the first byte is the sequence number
        num_bytes += data_length - 1

        prev_sequence = sequence_number
        
        #we write the data from 1 to the data length
        #we do not write the first byte because that is the sequence number
        dest.write(data[1:data_length])
    
        dest.flush()

        #implement fin ack ???????





        
    return num_bytes

















