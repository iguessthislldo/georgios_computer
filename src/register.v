module register(out, in, clock, reset);
    parameter b = 8;

    output [b-1:0] out;
    input [b-1:0] in;
    input clock;
    input reset;

    reg [b-1:0] out;

    always @(posedge clock) begin
        if (reset) out = 0;
        else out = in;
    end
endmodule
