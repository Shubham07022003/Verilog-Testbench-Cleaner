// Testbench for AND Gate
module and_gate_tb;

  // Declare inputs as reg and output as wire
  reg a, b;       // Inputs to the AND gate
  wire y;         // Output of the AND gate

  // Instantiate the AND gate module
  and_gate uut (
    .a(a),        // Connect input 'a' to the testbench
    .b(b),        // Connect input 'b' to the testbench
    .y(y)         // Connect output 'y' to the testbench
  );

  // Testbench logic
  initial begin
    // Display header for simulation results
    $display("Time\t a b | y");
    $display("-----------------");

    // Apply test cases
    a = 0; b = 0; #10; $display("%0t\t %b %b | %b", $time, a, b, y);
    a = 0; b = 1; #10; $display("%0t\t %b %b | %b", $time, a, b, y);
    a = 1; b = 0; #10; $display("%0t\t %b %b | %b", $time, a, b, y);
    a = 1; b = 1; #10; $display("%0t\t %b %b | %b", $time, a, b, y);

    // End simulation
    $stop;
  end

endmodule
