module 74181(F, G, P, E, Co, A, B, S, Ci);
    output [3:0] F; // Result
    output
        G, // Generate
        P, // Propagate
        E, // Equality
        Co; // ?
        
    input [3:0]
        A, B, // Operands
        S; // Operator
    input Ci; // ?
endmodule
