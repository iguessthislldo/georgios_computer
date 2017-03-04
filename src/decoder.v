module decoder(alu_op, flags, clock, op);
    parameter w = 8; // # of bits for data
    parameter op_w = 3; // # of bits for Instructions
    parameter alu_op_w = 1; // # of bits for ALU Instructions
    parameter flags_w = 6;

    output reg [alu_op_w-1:0] alu_op; // ALU Instruction
    output reg [0:flags_w-1] flags;

    input clock;
    input [op_w-1:0] op; // Instruction

    always @(posedge clock) begin
        case (op)
            0: begin
                $display("halt");
                $finish;
            end
            1: begin
                $display("nop");
            end
            2: begin
                $display("set");
                flags = 6'b01x1xx;
            end
            3: begin
                $display("copy");
                flags = 6'b10x11x;
            end
            4: begin
                $display("addr");
                alu_op[0] = 1'b0;
                flags = 6'b111111;
            end
            5: begin
                $display("addv");
                alu_op[0] = 1'b0;
                flags = 6'b110110;
            end
            6: begin
                $display("subr");
                alu_op[0] = 1'b1;
                flags = 6'b111111;
            end
            7: begin
                $display("subv");
                alu_op[0] = 1'b1;
                flags = 6'b110110;
            end
            default: begin
                $display("Invalid Instruction!");
                $finish;
            end
        endcase
    end
endmodule
