module alu(result, status, op, a, b);
    parameter w = 8;
    parameter op_w = 1;
    parameter status_w = 1;

    output reg [w-1:0] result;
    output reg [status_w-1:0] status;
    input [op_w-1:0] op;
    input [w-1:0] a, b;

    always @(op or a or b) begin
        {status[0], result} = a + (op[0] ? ~b : b) + op[0];
    end
endmodule
