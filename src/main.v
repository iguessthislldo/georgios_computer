`timescale 1ns / 1ns 
module main;

reg [31:0] rom [0:3];
reg [31:0] current;
reg [7:0] iter;

// Clock
reg clock;
initial begin
    clock = 0;
    forever #100 clock = ~clock;
end

// Dump Waveform
initial begin
    $dumpfile("dump.vcd");
    $dumpvars(0, clock, iter, current);
end

initial begin
    iter = 0;
    current = rom[0];
end
always @(posedge clock) begin
    iter = iter + 1;
    current = rom[iter];
end

initial #10000 $finish;

initial $readmemh("data", rom);

endmodule 
