`timescale 10ns / 1ns 
module half_adder(result, carry, a, b);
    output result, carry;
    input a, b;

    xor #(1) (result, a, b);
    and #(1) (carry, a, b);
endmodule
