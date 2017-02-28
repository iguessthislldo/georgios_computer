`timescale 1ns / 1ns 
module adder_subtractor(r, carry, a, b, subtract);
    parameter b = 8;

    output [b-1:0] r;
    output carry;
    input [b-1:0] a, b;
    input subtract;
    wire [b-1:0] b_prime;
    wire [b-2:0] inner_carry;

    // TODO: Auto generate full adders, etc based on word size
    
    xor #(10) G0(b_prime[0], b[0], subtract);
    xor #(10) G1(b_prime[1], b[1], subtract);
    xor #(10) G2(b_prime[2], b[2], subtract);
    xor #(10) G3(b_prime[3], b[3], subtract);
    xor #(10) G4(b_prime[4], b[4], subtract);
    xor #(10) G5(b_prime[5], b[5], subtract);
    xor #(10) G6(b_prime[6], b[6], subtract);
    xor #(10) G7(b_prime[7], b[7], subtract);

    full_adder a0(r[0], inner_carry[0], a[0], b_prime[0], subtract);
    full_adder a1(r[1], inner_carry[1], a[1], b_prime[1], inner_carry[0]);
    full_adder a2(r[2], inner_carry[2], a[2], b_prime[2], inner_carry[1]);
    full_adder a3(r[3], inner_carry[3], a[3], b_prime[3], inner_carry[2]);
    full_adder a4(r[4], inner_carry[4], a[4], b_prime[4], inner_carry[3]);
    full_adder a5(r[5], inner_carry[5], a[5], b_prime[5], inner_carry[4]);
    full_adder a6(r[6], inner_carry[6], a[6], b_prime[6], inner_carry[5]);
    full_adder a7(r[7], carry,          a[7], b_prime[7], inner_carry[6]);
endmodule
