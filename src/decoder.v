module decoder(alu_op, x_sel, y_sel, z_sel, clock, op);
    parameter b = 8; // # of bits for data
    parameter op_b = 3; // # of bits for Instructions
    parameter alu_op_b = 1; // # of bits for ALU Instructions
    parameter sel_b = 4 // # of bits for register select

    output [alu_op_b-1:0] alu_op; // ALU Instruction
    output [sel_b-1:0] x_sel, y_sel, z_sel; // Register Selection

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
            end
            5: begin
                $display("addv");
            end
            6: begin
                $display("subr");
            end
            7: begin
                $display("subv");
            end
            default: begin
                $display("Invalid Instruction!");
                $finish;
            end
        endcase
endmodule
