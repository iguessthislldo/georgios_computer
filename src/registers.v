module registers(x_out, y_out, z_in, x_enb, y_enb, z_enb, x_sel, y_sel, z_sel);
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

    // Registers
    genvar i;
    generate for (i = 0; i < N; i = i + 1) begin
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
        $display("Register[%h] = %h", z_sel, z_in);
    end

    always @(negedge z_enb) begin
        r_clock[z_sel] = 0;
    end
endmodule
