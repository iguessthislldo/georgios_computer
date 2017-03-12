module router(a, b, z,
    x_sel, y_sel, z_sel,
    x_enb, y_enb, z_enb,
    flags, i1, i2, i3, result, x, y
);

    parameter w = 8; // # of data bits
    parameter sel_w = 4; // # of bits for register select
    parameter flags_w = 6;

    output reg [w-1:0] a, b; // Inputs for ALU
    output reg [w-1:0] z; // Register Write
    output reg [sel_w-1:0] x_sel, y_sel, z_sel; // Register Selection
    output reg x_enb, y_enb, z_enb; // Register Enable
    input [0:flags_w-1] flags;
    input [w-1:0] i1, i2, i3; // Instruction Arguments
    input [w-1:0] result; // Result from ALU
    input [w-1:0] x, y;

    initial begin
        x_enb = 1'b0;
        y_enb = 1'b0;
        z_enb = 1'b0;
    end

    always @(flags or i2 or x or result) begin
        case (flags[0:1])
            0: z = 8'hxx;
            1: z = i2;
            2: z = x;
            3: z = result;
        endcase
        
        a = x;
    end

    always @(y or flags or i3) begin
        if (flags[2])
            b = y;
        else
            b = i3;
    end

    always @(i1 or flags) begin
        if (flags[3]) begin
            z_sel = i1;
            #20
            z_enb = 1'b1;
            #10
            z_enb = 1'b0;
        end
    end

    always @(i2 or flags) begin
        if (flags[4]) begin
            x_sel = i2;
            #10
            x_enb = 1'b1;
            #20
            x_enb = 1'b0;
        end
    end

    always @(i3 or flags) begin
        if (flags[5]) begin
            y_sel = i3;
            #10
            y_enb = 1'b1;
            #20
            y_enb = 1'b0;
        end
    end
endmodule
