# Georgios Instruction Set
## Instruction Format

Instructions consist of 1 to 4 16 bit words (I0, I1, I2, I3). I0 contains the
OP codes and other directives. The rest are arguments, which are interpeted or
ignored depending on I0.

`OP[8], Signed_Words[1], Indirection[3], Unused[2], Byte_Offset[1], Half_Words[1]`

- OP is the 8 bit OP Code for the instruction.
- Signed\_Words says the arguments are signed (2's complement). This will have
different meanings (or no meaning) depending on the instruction.
- Indirection indicates which of the arguments (I1, I2, I3) should taken as
values in the instruction or used to select the values from registers.
- If Half\_Words is true, then Byte\_Offset dictates which half of the buses
to use. 0 uses the lower byte [0-7], while 1 uses the higher byte [8-15].
- Half\_Words indicates that the instruction is 8 bits. This doesn't apply to
all instructions and arguments.

## Instruction OP Codes

**Note: When refering a value here, it means the argument can be a constant
value or the value of register**

- `nop`
    - Do nothing.
    - OP Code: 0
        - 0x00
        - 0b00000000
    - Arguments: 0
- `=`
    - Set a register to a value.
        - R[I1] = I2
        - R[I1] = R[I2]
    - OP Code: 1
        - 0x01
        - 0b00000001
    - Arguments: 2
        - Register to Set
        - Value to Use
- `save`
    - Save a value to memory offset by a value.
        - M[I1 + I2] = I3
        - M[I1 + I2] = R[I3]
        - M[I1 + R[I2]] = I3
        - M[I1 + R[I2]] = R[I3]
        - M[R[I1] + I2] = I3
        - M[R[I1] + I2] = R[I3]
        - M[R[I1] + R[I2]] = I3
        - M[R[I1] + R[I2]] = R[I3]
    - OP Code: 2
        - 0x02
        - 0b00000010
    - Arguments: 3
        - Address Value
        - Offset Value
        - Value to save to memory
- `load`
    - Load a word from memory to a register offset by a value.
        - R[I1] = M[I2 + I3]
        - R[I1] = M[I2 + R[I3]]
        - R[I1] = M[R[I2] + I3]
        - R[I1] = M[R[I2] + R[I3]]
    - OP Code: 3
        - 0x03
        - 0b00000011
    - Arguments: 3
        - Destination Register
        - Address Value
        - Offset Value
- `if`
    - Jump to an address if a register is true. If signed, jumps relative to
      the current pc.
        - if R[I1]: PC = I2
        - if R[I1]: PC = R[I2]
        - if R[I1]: PC = PC + I2
        - if R[I1]: PC = PC + R[I2]
    - OP Code: 4
        - 0x04
        - 0b00000100
    - Arguments: 2
        - Register to test
        - Address or Offset Value
- `goto`
    - Jump to an address or if signed, jump relative to the current pc.
        - PC = I1
        - PC = R[I2]
        - PC = PC + I1
        - PC = PC + R[I2]
    - OP Code: 5
        - 0x05
        - 0b00000101
    - Arguments: 1
        - Address or Offset Value
- `if!`
    - Jump to an address if a register is false. If signed, jumps relative to
      the current pc.
        - if !R[I1]: PC = I2
        - if !R[I1]: PC = R[I2]
        - if !R[I1]: PC = PC + I2
        - if !R[I1]: PC = PC + R[I2]
    - OP Code: 6
        - 0x06
        - 0b00000110
    - Arguments: 2
        - Register to test
        - Address or Offset Value
- `out`
    - Write a value to a device with a given argument.
        - D[I1, I2] = I3
        - D[I1, I2] = R[I3]
        - D[I1, R[I2]] = I3
        - D[I1, R[I2]] = R[I3]
        - D[R[I1], I2] = I3
        - D[R[I1], I2] = R[I3]
        - D[R[I1], R[I2]] = I3
        - D[R[I1], R[I2]] = R[I3]
    - OP Code: 8
        - 0x08
        - 0b00001000
    - Arguments: 3
        - Device Bus value to use
        - Argument value to send to device
        - Value to send
- `in`
    - Read a value from a device with a given argument.
        - R[I1] = D[I2, I3]
        - R[I1] = D[I2, R[I3]]
        - R[I1] = D[R[I2], I3]
        - R[I1] = D[R[I2], R[I3]]
    - OP Code: 9
        - 0x09
        - 0b00001001
    - Arguments: 3
        - Destination Register
        - Device Bus to use
        - Argument value to send to device
- `++`
    - Increment Register
        - R[R1] = R[I1] + 1
    - OP Code: 16
        - 0x10
        - 0b00010000
    - Arguments: 1
        - Register to increment
- `--`
    - Decrement Register
        - R[I1] = R[I1] - 1
    - OP Code: 17
        - 0x11
        - 0b00010001
    - Arguments: 1
        - Register to decrement
- `~`
    - Set a register to the bitwise not of another register
    - OP Code: 18
        - 0x12
        - 0b00010010
    - Arguments: 2
        - Destination Register
        - Source Register
- `!`
    - Set a register to the logical not of another register
    - OP Code: 19
        - 0x13
        - 0b00010011
    - Arguments: 2
        - Destination Register
        - Source Register

---

**All the following up to halt/255 have the same format:**

Take the result of an operation of two values and assign it to a register.

- R[I1] = OP(I2,I3)
- R[I1] = OP(R[I2],I3)
- R[I1] = OP(I2,R[I3])
- R[I1] = OP(R[I2],R[I3])

---

- `+`
    - Add two values
    - OP Code: 64
        - 0x40
        - 0b01000000
- `-`
    - Subtract two values
    - OP Code: 65
        - 0x41
        - 0b01000001
- `*`
    - Divide two values.
    - OP Code: 66
        - 0x42
        - 0b01000010
- `&&`
    - Logical AND of two values.
    - OP Code: 67
        - 0x43
        - 0b01000011
- `||`
    - Logical OR of two values.
    - OP Code: 68
        - 0x44
        - 0b01000100
- `<<`
    - Left Bit Shift of two values.
    - OP Code: 69
        - 0x45
        - 0b01000101
- `>>`
    - Right Bit Shift of two values.
    - OP Code: 70
        - 0x46
        - 0b01000110
- `>>>`
    - Arithmatic Right Bit Shift of two values.
    - OP Code: 71
        - 0x47
        - 0b01000111
- `&`
    - Bitwise AND of two values.
    - OP Code: 72
        - 0x48
        - 0b01001000
- `|`
    - Bitwise OR of two values.
    - OP Code: 73
        - 0x49
        - 0b01001001
- `^`
    - Bitwise XOR of two values.
    - OP Code: 74
        - 0x4A
        - 0b01001010
- `==`
    - Returns true if two values are equal
    - OP Code: 80
        - 0x50
        - 0b1010000
- `!=`
    - Returns false if two values are equal
    - OP Code: 81
        - 0x51
        - 0b1010001
- `>`
    - Returns true if I2 is greater than I3
    - OP Code: 82
        - 0x52
        - 0b1010010
- `>=`
    - Returns true if I2 is greater than or equal to I3
    - OP Code: 83
        - 0x53
        - 0b1010011
- `<`
    - Returns true if I2 is less than I3
    - OP Code: 84
        - 0x54
        - 0b1010100
- `<=`
    - Returns true if I2 is less than or equal to I3
    - OP Code: 85
        - 0x55
        - 0b1010101
- `halt`
    - Stop the computer by stoping the clock.
    - OP Code: 255
        - 0xFF
        - 0b11111111
    - Arguments: 0
