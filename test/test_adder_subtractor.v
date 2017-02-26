`timescale 1ns / 1ns 
module test_adder_subtractor;
    reg [7:0] a;
    reg [7:0] b;
    reg subtract;
    wire [7:0] result;
    wire carry;

    reg signed [7:0] test_result;
    reg test_carry;

    reg add_done = 0;
    reg sub_start = 0;
    reg sub_done = 0;

    // Clock
    reg clock;
    initial begin
        clock = 0;
        forever #100 clock = ~clock;
    end

    adder_subtractor as(result, carry, a, b, subtract);

    initial begin
        //$dumpfile("tmp/dump.vcd");
        //$dumpvars(0, clock, result, carry, a, b, subtract);
        
        a = 8'h00;  
        b = 8'h00;
        subtract = 1'b0;
    end

    always @(posedge clock) begin
        //$display("%h,%b,%h,%h,%b",result, carry, a, b, subtract);

        if (sub_start == 0) begin
            {test_carry, test_result} = a + b;
            if ((carry != test_carry) || (result != test_result)) begin
                $display(
                    "%h + %h: %h carry %b does not match %h carry %b",
                    a, b, result, carry, test_result, test_carry
                );
                $finish;
            end
        end else begin
            test_result = a - b;
            if (result != test_result) begin
                $display(
                    "%h - %h: %h does not match %h",
                    a, b, result, test_result
                );
                $finish;
            end
        end
        
        if (add_done == 0) begin
            if (b == 8'hff) begin
                if (a < 8'hff) begin
                    a = a + 8'h01;
                    b = 8'h00;
                end else begin
                    add_done = 1;
                    a = 8'h00;  
                    b = 8'h00;
                    subtract = 1'b1;
                    #199
                    sub_start = 1;
                end
            end else begin
                b = b + 8'h01;
            end
        end else begin
            if (sub_start == 1 && sub_done == 0) begin
                if (b == 8'hff) begin
                    if (a < 8'hff) begin
                        a = a + 8'h01;
                        b = 8'h00;
                    end else begin
                        sub_done = 1;
                        #400
                        $display("Adder Subtractor passed the test");
                        $finish;
                    end
                end else begin
                    b = b + 8'h01;
                end
            end
        end
    end
endmodule
