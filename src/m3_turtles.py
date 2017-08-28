"""
Demonstrates using OBJECTS via Turtle Graphics.

Concepts include:
  -- CONSTRUCT an INSTANCE of a CLASS (we call such instances OBJECTS).
  -- Make an object   ** DO **   something by using a METHOD.
  -- Reference an object's   ** DATA **   by using an INSTANCE VARIABLE.

Also:
  -- ASSIGNING a VALUE to a NAME (VARIABLE).

Authors: David Mutchler, Dave Fisher, Valerie Galluzzi, Amanda Stouder,
         their colleagues and PUT_YOUR_NAME_HERE.  March 2016.
"""
########################################################################
#
# TODO: 1.
#  (Yes, that means for YOU to DO things per these instructions:)
#
# On Line 13 above, replace  PUT_YOUR_OWN_NAME_HERE  with your OWN name.
#
# BTW, the green lines above form what is called a DOC-STRING.
# It documents what this module does, in a way that exterior programs
# can make sense of.  It has no other effect on this program.
#
########################################################################

import rosegraphics as rg

# ----------------------------------------------------------------------
# Next two lines after this comment set up a   TurtleWindow   object
# for animation.  The definition of a TurtleWindow is in the
#   rg  (shorthand for rosegraphics) module.
# ----------------------------------------------------------------------
window = rg.TurtleWindow()
window.delay(20)  # Bigger numbers mean slower animation.

# ----------------------------------------------------------------------
# Next two lines make (construct) two   SimpleTurtle   objects.
# ----------------------------------------------------------------------
nadia = rg.SimpleTurtle()
akil = rg.SimpleTurtle('turtle')

# ----------------------------------------------------------------------
# Next lines ask the SimpleTurtle objects to do things:
# ----------------------------------------------------------------------
nadia.forward(100)
nadia.left(90)
nadia.forward(200)

akil.right(45)
akil.backward(50)
akil.right(60)

nadia.forward(50)
nadia.left(135)

# ----------------------------------------------------------------------
# Next lines set the   pen   and  speed   characteristics of the
# SimpleTurtle objects.  The   pen   characteristic is itself an object
# that is constructed, of type Pen.
# ----------------------------------------------------------------------
nadia.pen = rg.Pen('blue', 10)  # Second argument is the Pen's thickness
nadia.speed = 10  # big is faster (maxes out about 100), 1 is slowest)

akil.pen = rg.Pen('red', 30)
akil.speed = 1

akil.backward(100)
nadia.forward(100)

nadia.left(60)
nadia.forward(500)
nadia.speed = 1  # was 10, so much slower now
nadia.right(120)
nadia.forward(200)

########################################################################
#
# TODO: 2.
#   (Yes, that means for YOU to DO things per these instructions:)
#
#   Run this module by using the green arrow on the toolbar up top.
#   A window will pop up and Turtles will move around.  After the
#   Turtles stop moving, click anywhere in the window to close it.
#
#   Then look at Lines 47 to 56.  Run again and see if you can tell
#   what each Turtle command does.  We call each such command a
#     METHOD.
#
#   Then look at Lines 63 to 67.  Run again and see if you can tell
#   what is different when, for a particular Turtle, its Turtle
#   characteristics:
#       pen   speed
#   are assigned a value.  We call such characteristics
#   INSTANCE VARIABLES, aka DATA ATTRIBUTES and (in Java) FIELDS.
#
#   Note especially that although both Turtle objects have the
#   same NAMES for their instance variables, each Turtle has
#   its own VALUES for those instance variables.  For example,
#   nadia's Pen has  'blue'  as its color while akil's Pen is  'red'.
#
#   No need for you to write anything for this part of the TODO.
#   Just change the TODO to DONE at Line 80 above, as usual
#   (and also the one at Line 17 if you have not already done that).
#
########################################################################

########################################################################
#
# TODO: 3.
#   Add a few more line after line 76 above to make one of the
#   existing Turtles move some more and/or have different
#   characteristics.
#
#      ** Nothing fancy is required. KISS. **
#      ** A SUBSEQUENT exercise will let you show your creativity. **
#
#   As always, test by running the module.
#
########################################################################

########################################################################
#
# TODO: 4.
#   Lines 41 and 42  CONSTRUCT  two SimpleTurtle objects
#   and give those objects NAMES:
#       nadia    akil
#   BTW, the definition for what a SimpleTurtle object knows and can do
#   is in the rosegraphics, abbreviated as rg, module, but you do NOT
#   need to (and should not) look at that module for this exercise.
#
#   After the code that you have already added (from previous TODOs),
#   construct another SimpleTurtle object, naming it whatever you want.
#   Names cannot have spaces or special characters, but they can have
#   digits and underscores like     this_1_has   (get it?).
#
#   Then, just below the line that you just wrote
#   to construct a SimpleTurtle, add a few more lines that
#   make YOUR SimpleTurtle move around a bit.
#
#      ** Nothing fancy is required. KISS. **
#      ** A SUBSEQUENT exercise will let you show your creativity. **
#
#   As always, test by running the module.
#
########################################################################

########################################################################
#
# TODO: 5.
#   After you have completed the above (including testing),
#   change the TODO at the beginning of this pink comment to DONE,
#   along with any other numbered TODOs that you have not yet done so.
#
#   Run one more time to be sure that all is still OK.
#   Ensure that no blue bars on the scrollbar-thing to the right remain.
#
#   Then COMMIT your work (which turns it in) by selecting (clicking on)
#   the file with the black dot (or the entire project if you prefer)
#   and then do     SVN ~ Commit...    from the SVN menu at the top.
#
#   Check that the black symbol beside the file name in the
#     PyDev Package Explorer   on the left has gone away.
#   That's how you can tell that you have turned in your work.
#
#   You can COMMIT as often as you like.  DO FREQUENT COMMITS.
#
########################################################################

# ----------------------------------------------------------------------
# Next line keeps the window open until the user clicks in the window:
# ----------------------------------------------------------------------
window.close_on_mouse_click()
