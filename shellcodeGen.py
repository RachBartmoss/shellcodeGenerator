#!/usr/bin/python3




def movValueToReg(reg,value):
    chunk = bytearray()
    push = 0x50
    push += registerDictionary["rcx"]
    chunk.append(push)

    print(chunk)


registerDictionary = {"rax":0,"rcx":1}

movValueToReg("rax",40)
