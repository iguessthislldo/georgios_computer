`timescale 1ns / 1ns 
module main;
    // Word/Data Bus Size
    parameter w = 8;

    // OP Word Size
    parameter op_w = 8;

    // File Read Params and vars
    parameter max_instructions = 256;
    parameter args_per = 4;
    integer pc;

    integer file, read_value;
    integer args = 0;
    integer no_instructions = 0;
    integer next_noinst, next_args;

    reg [w-1:0] memory [0:max_instructions-1][0:args_per-1];

    // Clock
    reg clock;
    initial begin
        #100
        $display("Georgios Begin");
        clock = 0;
        forever begin
            if (clock) 
                $display("\n%0t ====================== TOCK", $time);
            else
                $display("\n%0t ---------------------- tick", $time);
            #100 clock = ~clock;
        end
    end

    // Instruction
    reg [op_w-1:0] i0; // OP
    reg [w-1:0] i1, i2, i3; // Arguments
    
    // ALU
    parameter alu_op_w = 1;
    parameter alu_status_w = 1;

    wire [w-1:0] result;
    wire alu_status;
    wire [w-1:0] a, b;
    wire alu_op;

    alu #(
        .w(w),
        .op_w(alu_op_w),
        .status_w(alu_status_w)
    ) alu0(result, alu_status, alu_op, a, b);

    // Registers
    parameter sel_w = 4;
    wire [w-1:0] x, y, z;
    wire [sel_w-1:0] x_sel, y_sel, z_sel;
    wire x_enb, y_enb, z_enb;

    registers #(
        .sel_w(sel_w)
    ) registers0(
        x, y, z,
        x_enb, y_enb, z_enb,
        x_sel, y_sel, z_sel
    );

    // Router
    parameter flags_w = 6;
    wire [0:flags_w-1] flags;

    router #(
        .w(w),
        .flags_w(flags_w),
        .sel_w(sel_w)
    ) router0 (
        a, b,
        z,
        x_sel, y_sel, z_sel,
        x_enb, y_enb, z_enb,
        flags,
        i1, i2, i3,
        result,
        x, y
    );

    // Decode

    decoder #(
        .w(w),
        .op_w(op_w),
        .flags_w(flags_w),
        .alu_op_w(alu_op_w)
    ) decoder0(alu_op, flags, clock, i0);

    initial begin
        file = $fopen("image", "rb");

        read_value = $fgetc(file);
        while (read_value != -1) begin
            memory[no_instructions][args] = read_value;

            if (args == 3) begin
                no_instructions++;
                if (no_instructions > max_instructions) begin
                    $display("File is bigger than assigned memory!");
                    $finish;
                end
                next_args = 0;
            end else next_args = args + 1;

            args = next_args;
            read_value = $fgetc(file);
        end

        $fclose(file);

        if (no_instructions == 0) begin
            $display("\"Empty File\"");
            $finish;
        end

        if (args) begin
            $display("Invalid size");
            $finish;
        end

        pc = 0;
        // Dump Waveform
        //$dumpfile("dump.vcd");
        //$dumpvars(0, result, , a, b, op);
    end

    always @(posedge clock) begin
        if (pc < no_instructions) begin
            i0 = memory[pc][0];
            i1 = memory[pc][1];
            i2 = memory[pc][2];
            i3 = memory[pc][3];

            #150 
            i0 = 8'hxx;
            i1 = 8'hxx;
            i2 = 8'hxx;
            i3 = 8'hxx;

            pc++;
        end else begin
            if (i0 != 0) begin
                $display("No more instructions");
                $finish;
            end
        end
    end
    
endmodule 
