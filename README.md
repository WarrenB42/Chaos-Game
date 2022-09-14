# Chaos Game

Python based fractal generator based on
[Ben Sparks's Geogebra animation.](https://www.youtube.com/watch?v=IKhahq9EwPw&list=PLl3qVGFFBb-6qhsVz5JAfjBD4uezo8Eho&index=1)

## Purpose

Using only simple vector moves, an incredible fractal pattern evolves
in a most unexpected way.

## Usage

Run the script from a command prompt, shell or terminal. The pattern selected
in the code will be displayed and the elapsed time displayed.

To change the internal configuration, edit the script and re-run it. Several
items can be changed:

* The number of points plotted is in the _numPoints_ variable.
    
* The pattern to display is set by assigning a named configuration to the
_config_ variable. Additional patterns can be created using the existing
ones as models.

* For better performance, the display is updated once for a series of points.
The _dispInterval_ variable sets the frequency as a counter. The default is
10 which results in an elapsed time around seven seconds for 50,000 points
on a Windows-based system running at 3.2Ghz.

## Notes

* Requires Python 3, probably 3.6 or higher (3.10 was used for development).

* Requires the pygame library package which is easily installed.
