# Solution: Stick Cutting

You can read and run `stick_cutting.py` to see what the solution is.

Without any command-line parameters, it defaults to just running a
Monte Carlo experiment: pick uniform random cutting positions, and see
if the triangle inequality is satisified by the resultant sticks.

Other execution modes can be selected.  With `--mode text_state_space`
it will print out a graph in a terminal window (you must have `xterm`
installed) to show you what combinations of first and second cut
positions would result in three sticks that can form a triangle.  With
`--mode state_space`, you get a graphical representation (you can
resize it to ensure that the axes are the same length).

![State Space Plot](out.png)
