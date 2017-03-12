module alu(result, status, op, a, b);
    parameter w = 8;
    parameter op_w = 1;
    parameter status_w = 1;

    output reg [w-1:0] result;
    output reg [status_w-1:0] status;
    input [op_w-1:0] op;
    input [w-1:0] a, b;

    always @(op or a or b) begin
        {status[0], result} = a + ({w{op[0]}} ^ b) + op[0];

        // Report
        if (status[0] == 0)
        $display("%0t ALU result: %h carry 0", $time, result);
        if (status[0] == 1)
        $display("%0t ALU result: %h carry 1", $time, result);
    end
endmodule
