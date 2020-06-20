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
resize it to make it bigger, etc).

In the state-space representation, we have a plot.  The _x_ axis is
the position of the first cut, and the _y_ axis is the position of the
second cut.  Each (_x_, _y_) position is colored in if cuts made at
those locations would result in sticks that can make a triangle. (The
program is actually sampling grid points; you can play with the
command line arguments to change this.)  Since the cuts are chosen
uniformly, the area of the colored region is the probability that
random cuts will yield sticks that will form a triangle.

The output will look something like the state-space plot in the figure.

![State Space Plot](out.png)

Let us go through why the figure is the way it is.

What has to occur if we are to _not_ be able to form a triangle?  In
order for the triangle inequality to be violated, one of the cut
sticks must be of length 1/2 plus 𝜀 or longer -- the other two sticks,
however the remaining material is to be distributed between them,
cannot close the gap.

Let the position of the first cut be denoted by _x_.  This means that
when and 0 ≤ _x_ ≤ ½, the second cut at _y_ must satisfy:

* _y_ ≤ _x_ + ½

* ½ ≤ _y_


Satisfying these constraints means that none of the 3 stick pieces
will be longer than ½.

This explains the triangle in the upper left of the plot with vertices
(0, ½), (½, ½), and (½, 1).

A similar line of reasoning for ½ ≤ _x_ ≤ 1, which yields the triangle
in the lower right with vertices (½, ½), (½, 0), and (1, ½).

For _x_ = ½, _y_ can be any value between 0 and 1 and we would end up
with a degenerate triangle.
