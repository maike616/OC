data r0, 0x0f
data r1, 0xff
data r2, 0x97
out addr, r2
in data, r3
xor r2, r2
out addr, r2
data r2, 0x98
out addr, r2
data r2, 20
add r2, r3
out data, r3
xor r2,r2
xor r3, r3
out addr, r2

add r1, r0
jz 0x19
jmp 0x04
jmp 0x19
