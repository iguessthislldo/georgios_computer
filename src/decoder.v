module decoder(alu_op, clock, op);
    parameter b = 8; // # of bits for data
    parameter op_b = 3; // # of bits for Instructions
    parameter alu_op_b = 1; // # of bits for ALU Instructions
    output [alu_op_b-1:0] alu_op; // ALU Instruction

    input clock;
    input [op_b-1:0] op; // Instruction

    always @(posedge clock) begin
        case (op)
            0:;
            1: begin
                $display("halt");
                $finish;
            end
            2: begin
                $display("set");
            end
            3: begin
                $display("copy");
            end
            4: begin
                $display("addr");
                alu_op[0] = 0;
            end
            5: begin
                $display("addv");
                alu_op[0] = 0;
            end
            6: begin
                $display("subr");
                alu_op[0] = 1;
            end
            7: begin
                $display("subv");
                alu_op[0] = 1;
            end
            default: begin
                $display("Invalid Instruction!");
                $finish;
            end
        endcase
endmodule
