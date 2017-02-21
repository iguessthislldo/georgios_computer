`timescale 1ns / 1ns 
module half_adder(result, carry, a, b);
    output result, carry;
    input a, b;

    xor #(10) (result, a, b);
    and #(10) (carry, a, b);
endmodule
