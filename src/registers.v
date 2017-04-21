module registers(
    x_out, y_out, z_in,
    x_enb, y_enb, z_enb,
    x_sel, y_sel, z_sel,
    cflags_in, pc_in, aflags_in, ahi_in,
    cflags_enb, pc_enb, aflags_enb, ahi_enb
);
    parameter w = 8;
    parameter sel_w = 4; // Selection bits
    parameter N = 2^sel_w; // Number of registers
    parameter N_read_only = 4;

    output reg [w-1:0] x_out, y_out;
    input [w-1:0] z_in;
    input x_enb, y_enb, z_enb;
    input [sel_w-1:0] x_sel, y_sel, z_sel;

    wire [w-1:0] general_x, general_y;
    reg [w-1:0] general_z;
    reg [sel_w-1:0] general_x_sel, general_y_sel, general_z_sel;
    reg general_x_enb, general_y_enb, general_z_enb;

    register_array general(
        general_x, general_y, general_z,
        general_x_enb, general_y_enb, general_z_enb,
        general_x_sel, general_y_sel, general_z_sel
    );

    // Behavior
    always @(posedge x_enb) begin
        if (x_sel >= N_read_only) begin
            x_out = r_out[x_sel-N_read_only];
        end else begin
        end
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
