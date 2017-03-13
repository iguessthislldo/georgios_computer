module registers(
    x_out, y_out, z_in,
    x_enb, y_enb, z_enb,
    x_sel, y_sel, z_sel
    pc_in, pc_out, pc_enb,
    flags_in, flags_out, flags_enb,
    alus_in, alus_out, alus_enb,
    low_in, low_out, low_enb,
    high_in, high_out, high_enb,
);
    parameter w = 8;
    parameter sel_w = 4; // Selection bits
    parameter N = 2^sel_w; // Number of registers

    output reg [w-1:0] x_out, y_out;
    input [w-1:0] z_in;
    input x_enb, y_enb, z_enb;
    input [sel_w-1:0] x_sel, y_sel, z_sel;

    wire [w-1:0] r_out [N-1:0];
    reg [w-1:0] r_in [N-1:0];
    reg r_clock [N-1:0];
    reg r_reset [N-1:0];

    output reg [w-1:0] pc_out, 

    // Special Registers
    parameter N_special = 5;
    register pc(r_out[0], r_in[0], r_clock[0], r_reset[0]);
    register flags(r_out[1], r_in[1], r_clock[1], r_reset[1]);
    register alus(r_out[2], r_in[2], r_clock[2], r_reset[2]);
    register low(r_out[3], r_in[3], r_clock[3], r_reset[3]);
    register high(r_out[4], r_in[4], r_clock[4], r_reset[4]);

    // General Purpose Registers
    genvar i;
    generate for (i = N_special; i < N; i = i + 1) begin
        register r(r_out[i], r_in[i], r_clock[i], r_reset[i]);
    end
    endgenerate

    // Behavior
    always @(posedge x_enb) begin
        x_out = r_out[x_sel];
    end

    always @(posedge y_enb) begin
        y_out = r_out[y_sel];
    end

    always @(posedge z_enb) begin
        r_in[z_sel] = z_in;
        r_clock[z_sel] = 1;
        $display("%0t r[%h] = %h", $time, z_sel, z_in);
    end

    always @(negedge z_enb) begin
        r_clock[z_sel] = 0;
    end
endmodule
