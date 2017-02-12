`timescale 10ns / 1ns 
module main;

reg [31:0] rom [0:255];

initial $readmemh("data", rom);

endmodule 
