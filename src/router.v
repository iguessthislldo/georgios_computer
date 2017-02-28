module router(x_sel, y_sel, z_sel, i1, i2, i3)
    parameter b = 8; // # of data bits
    parameter sel_b = 4; // # of bits for register select

    output [sel_b-1:0] x_sel, y_sel, z_sel; // Register Selection
    input [b-1:0] i1, i2, i3; // Instruction Arguments
endmodule
