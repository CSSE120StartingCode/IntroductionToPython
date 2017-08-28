"""
Demonstrates using OBJECTS via Turtle Graphics.

Concepts include:
  -- CONSTRUCT an INSTANCE of a CLASS (we call such instances OBJECTS).
  -- Make an object   ** DO **   something by using a METHOD.
  -- Reference an object's   ** DATA **   by using an INSTANCE VARIABLE.

Also:
  -- ASSIGNING a VALUE to a NAME (VARIABLE).

Authors: David Mutchler, Dave Fisher, Valerie Galluzzi, Amanda Stouder,
         their colleagues and PUT_YOUR_NAME_HERE.
"""
########################################################################
#
# TODO: 1.
#  (Yes, that means for YOU to DO things per these instructions:)
#
# On Line 13 above, replace  PUT_YOUR_OWN_NAME_HERE  with your OWN name.
#
# BTW, the top block of text above forms what is called a DOC-STRING.
# It documents what this module does, in a way that exterior programs
# can make sense of.  It has no other effect on this program.
#
########################################################################

import rosegraphics as rg

########################################################################
#
# TODO: 2.
#   Allow this file to use the rosegraphics.py file by marking the src
#   directory as a "Sources Root".  Do that by right clicking on the src folder,
#   then selector  Mark Directory As --> Sources Root
#   Watch the red underlines on the line of code above disappear as you do that step.
#   You will do that once for every project that uses rosegraphics so get used to it. :)
#
#   Run this module by Right clicking in this window and select Run 'filename'
#   A window will pop up and Turtles will move around.  After the
#   Turtles stop moving, *click anywhere in the window to close it*.
#
#   Then look at the code below.  Raise your hand as you have questions
#   about what the code is doing.
#
########################################################################

# ----------------------------------------------------------------------
# Set up a   TurtleWindow   object for animation.  The definition of a
#     TurtleWindow is in the   rg  (shorthand for rosegraphics) module.
# ----------------------------------------------------------------------
window = rg.TurtleWindow()
window.delay(20)  # Bigger numbers mean slower animation.

# ----------------------------------------------------------------------
# Makes (constructs) a   SimpleTurtle   object.
# ----------------------------------------------------------------------
dave = rg.SimpleTurtle()

# ----------------------------------------------------------------------
# Ask the SimpleTurtle objects to do things:
# ----------------------------------------------------------------------
dave.forward(100)
dave.left(90)
dave.forward(200)

# ----------------------------------------------------------------------
# Construct a new turtle and ask it to do things.
# ----------------------------------------------------------------------
matt = rg.SimpleTurtle('turtle')
matt.pen = rg.Pen('red', 30)
matt.speed = 10  # Faster
matt.backward(50)
matt.left(90)
matt.forward(50)


########################################################################
#
# TODO: 3.
#   Add a few more line of your own code above to make one of the
#   existing Turtles move some more and/or have different
#   characteristics.
#
#      ** Nothing fancy is required. **
#      ** A SUBSEQUENT exercise will let you show your creativity. **
#
#   As always, test by running the module.
#
########################################################################

########################################################################
#
# TODO: 4.
#   The code above  CONSTRUCTS  two SimpleTurtle objects and gives those objects NAMES:
#       dave    matt
#
#   Below this TO DO comment construct another SimpleTurtle object,
#       naming it whatever you want.
#   Names cannot have spaces or special characters, but they can have
#   digits and underscores like     this_1_has   (get it?).
#
#   After you construct a SimpleTurtle, add a few more lines that
#   make YOUR SimpleTurtle move around a bit.
#
#      ** Nothing fancy is required. **
#      ** A SUBSEQUENT exercise will let you show your creativity. **
#
#   As always, test by running the module.
#
########################################################################

########################################################################
#
# TODO: 5.
#   Run one more time to be sure that all is still OK.
#   Ensure that no blue bars on the scrollbar-thing to the right remain.
#
#   Then COMMIT and Push your work using the VCS menu option.
#
#   Reminder of those steps...
#   COMMIT your work by selecting VCS from the menu bar, then select Commit Changes
#   Make sure only the files you want to commit are checked and optionally
#   add a quick Commit message to describe your work.  Then hover over the
#   Commit button and select Commit and Push.  Commit saves the work to
#   your computer.  "and Push" saves a copy of your work up into your Github
#   repository (saving to the cloud is a better way to permanently safe work).
#
#   You can COMMIT as often as you like.  DO FREQUENT COMMITS.
#
########################################################################

# ----------------------------------------------------------------------
# This line keeps the window open until the user clicks in the window:
# Throughout this exercise, close_on_mouse_click should be the last line in the file.
# ----------------------------------------------------------------------
window.close_on_mouse_click()
