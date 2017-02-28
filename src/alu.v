module alu(result, status, op, a, b)
    parameter b = 8;
    parameter op_b = 1;
    parameter status_b = 1;

    output [b-1:0]result;
    output [status_b-1:0]status;
    input [op_b-1:0]op;
    input [b-1:0] a, b;

    adder_subtractor as(result, status[0], a, b, op[0]);
endmodule
