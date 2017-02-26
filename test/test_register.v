`timescale 1ns / 1ns 
module test_register;
    // Clock
    reg clock;
    initial begin
        clock = 0;
        forever #100 clock = ~clock;
    end

    parameter N = 8;

    reg [N-1:0] in;
    reg reset;
    wire [N-1:0] out;

    register #(N) r(out, in, clock, reset);

    initial begin
        $dumpfile("tmp/dump.vcd");
        $dumpvars(0, out, in, clock, reset);
        
        in = 0;
        reset = 0;
        #250 in = 10;
        #200 reset = 1;
    end

    initial #1000 $finish;
endmodule
