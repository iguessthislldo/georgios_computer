module alu(result, op, a, b)
    output [0:7] r;
    input op;
    input [0:7] a, b;

    wire carry;

    adder_subtractor as(result, carry, a, b, op);
endmodule
