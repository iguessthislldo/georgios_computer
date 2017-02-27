`timescale 1ns / 1ns 
module test_register;
    parameter b = 8;
    parameter N_b = 4;

    wire [b-1:0] x, y;
    reg [b-1:0] z;
    reg x_enb, y_enb, z_enb;
    reg [N_b-1:0] x_sel, y_sel, z_sel;

    registers r(x, y, z, x_enb, y_enb, z_enb, x_sel, y_sel, z_sel);

    initial begin
        $dumpfile("tmp/dump.vcd");
        $dumpvars(0, x, y, z, x_enb, y_enb, z_enb, x_sel, y_sel, z_sel);

        z = 1;
        z_sel = 0;
        #100
        z_enb = 1;
        #100
        z_enb = 0;
        #100
        z_sel = 1;
        z = 2;
        #100
        z_enb = 1;
        #100
        z_enb = 0;
        #100
        x_sel = 0;
        x_enb = 1;
        y_sel = 1;
        y_enb = 1;
    end

    initial #1000 $finish;
endmodule
