module router(a, b, z, x_sel, y_sel, z_sel, i1, i2, i3, result, x, y)
    parameter w = 8; // # of data bits
    parameter sel_w = 4; // # of bits for register select

    output [w-1:0] a, b; // Inputs for ALU
    output [w-1:0] z; // Register Write
    output [sel_w-1:0] x_sel, y_sel, z_sel; // Register Selection
    input [w-1:0] i1, i2, i3; // Instruction Arguments
    input [w-1:0] result; // Result from ALU
endmodule
