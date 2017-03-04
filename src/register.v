module register(out, in, clock, reset);
    parameter w = 8;

    output [w-1:0] out;
    input [w-1:0] in;
    input clock;
    input reset;

    reg [w-1:0] out;

    always @(posedge clock) begin
        if (reset) out = 0;
        else out = in;
    end
endmodule
