`timescale 10ns / 1ns 
module alu(r, carry, a, b, subtract);
    output [0:7] r;
    output carry;
    input [0:7] a, b;
    input subtract;
    wire [0:7] inner_carry, bnot, buse;
    
    assign buse = subtract ? ~b : b;

    full_adder a0(r[0], inner_carry[0], a[0], buse[0], subtract);
    full_adder a1(r[1], inner_carry[1], a[1], buse[1], inner_carry[0]);
    full_adder a2(r[2], inner_carry[2], a[2], buse[2], inner_carry[1]);
    full_adder a3(r[3], inner_carry[3], a[3], buse[3], inner_carry[2]);
    full_adder a4(r[4], inner_carry[4], a[4], buse[4], inner_carry[3]);
    full_adder a5(r[5], inner_carry[5], a[5], buse[5], inner_carry[4]);
    full_adder a6(r[6], inner_carry[6], a[6], buse[6], inner_carry[5]);
    full_adder a7(r[7], carry, a[7], buse[7], inner_carry[6]);
endmodule
