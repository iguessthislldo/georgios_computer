`timescale 1ns / 1ns 
module main;

    // Clock
    reg clock;
    initial begin
        clock = 0;
        forever #100 clock = ~clock;
    end

    // Word/Data Bus Size
    parameter w = 8;

    // OP Word Size
    parameter op_w = 3;

    // Instruction
    reg [op_w-1:0] i0; // OP
    reg [w-1:0] i1, i2, i3; // Arguments
    
    // ALU
    parameter alu_op_w = 1;
    parameter alu_status_w = 1;

    wire [w-1:0] result;
    wire alu_status;
    wire [w-1:0] a, b;
    wire alu_op;

    alu #(
        .w(w),
        .op_w(alu_op_w),
        .status_w(alu_status_w)
    ) alu0(result, alu_status, alu_op, a, b);

    // Registers
    parameter sel_w = 4;
    wire [w-1:0] x, y, z;
    wire [sel_w-1:0] x_sel, y_sel, z_sel;
    wire x_enb, y_enb, z_enb;

    registers #(
        .sel_w(sel_w)
    ) registers0(
        x, y, z,
        x_enb, y_enb, z_enb,
        x_sel, y_sel, z_sel
    );

    // Router
    parameter flags_w = 6;
    wire [0:flags_w-1] flags;

    router #(
        .w(w),
        .flags_w(flags_w),
        .sel_w(sel_w)
    ) router0 (
        a, b,
        z,
        x_sel, y_sel, z_sel,
        x_enb, y_enb, z_enb,
        flags,
        i1, i2, i3,
        result,
        x, y
    );

    // Decode

    decoder #(
        .w(w),
        .op_w(op_w),
        .flags_w(flags_w),
        .alu_op_w(alu_op_w)
    ) decoder0(alu_op, flags, clock, i0);

    initial begin
        i0 = 1;
        // Dump Waveform
        //$dumpfile("dump.vcd");
        //$dumpvars(0, result, , a, b, op);
        #300
        i0 = 2;
        i1 = 0;
        i2 = 1;
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

    //reg [31:0] rom [0:3];
    //reg [31:0] current;
    //reg [7:0] iter;
    

    //initial $readmemh("data", rom);

endmodule 
