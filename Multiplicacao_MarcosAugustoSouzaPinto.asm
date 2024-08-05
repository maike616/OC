data r0,0x05 
data r1,0x07 
data r2,0xff 

add r1,r3 
st  r2,r3 
add r2,r0 

jz  0x0d 
jmp 0x06

ld  r2,r1
jmp 0x0e
 
