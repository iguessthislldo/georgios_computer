`timescale 1ns / 1ns 
module main;

    // Word/Data Bus Size
    parameter w = 8;
    
    // ALU
    parameter alu_op_w = 1;
    parameter alu_status_w = 1;

    //reg [31:0] rom [0:3];
    //reg [31:0] current;
    //reg [7:0] iter;
    
    wire [w-1:0] result;
    wire status;
    reg [w-1:0] a, b;
    reg op;
    alu #(
        .w(w),
        .op_w(alu_op_w),
        .status_w(alu_status_w)
    ) alu0(result, status, op, a, b);

    // Clock
    reg clock;
    initial begin
        clock = 0;
        forever #100 clock = ~clock;
    end

    // Dump Waveform
    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(0, result, status, a, b, op);

        a = 8'h02;
        b = 8'h06;
        op = 1'b0;
    end

    initial #10000 $finish;

    //initial begin
    //    iter = 0;
    //    current = rom[0];
    //end
    //always @(posedge clock) begin
    //    iter = iter + 1;
    //    current = rom[iter];
    //end


    //initial $readmemh("data", rom);

endmodule 
