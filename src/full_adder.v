`timescale 10ns / 1ns 
module full_adder(result, carry_out, a, b, carry_in);
    output result, carry_out;
    input a, b, carry_in;
    wire A2_a, G1_a, G1_b;

    half_adder A1(A2_a, G1_b, a, b);
    half_adder A2(result, G1_a, A2_a, carry_in);
    or #(1) G1(carry_out, G1_a, G1_b);
endmodule
