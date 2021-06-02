"""
rosegraphics.py - a simple Graphics library for Python.

Its key feature is:
  -- USING this library provides a simple introduction to USING objects.

Other key features include:
  -- It has a rich set of classes, methods and instance variables.
       In addition to classes like Circles that are natural for students,
       it has other kinds of classes like RoseWindow and SimpleTurtle
       to provide a richer set of examples than "just" a graphics library.
  -- It allows one to do a reasonable set of graphics operations
       with reasonable efficiency. The API mimics Java's Shape API
       for the most part.
  -- It is built on top of tkinter and its extension ttk
       (the standard graphics libraries that come with Python).
  -- Unlike tkinter, it is NOT event-driven and hence can be used
       before students see that paradigm.  (There is a behind-the-scenes
       facility for listening for and responding to events,
       for those who want to do so.)
  -- It attempts to be as bullet-proof as possible, to make it easy
       for beginners to use it.  In particular, it attempts to provide
       reasonable error messages when a student misuses the API.
  -- It was inspired by zellegraphics but is a complete re-implementation
       that attempts to:
       -- Be more bullet-proof.
       -- Provide a richer set of examples for using objects.
       -- Have an API that is more like Java's Shape API than tkinter's
            (older) API.
  -- While it can serve as an example for defining classes,
        it is NOT intended to do so for beginners.
        It is excellent for helping students learn to USE objects;
        it is NOT perfect for helping students learn to WRITE CLASSES.

See the MAIN function below for typical examples of its use.

Authors: David Mutchler, Mark Hays, Michael Wollowswki, Matt Boutell,
         Chandan Rupakheti, Claude Anderson and their colleagues,
         with thanks to John Zelle for inspiration and hints.
         First completed version: September 2014.
"""

import tkinter
from tkinter import font as tkinter_font
import time
import turtle


# ----------------------------------------------------------------------
# All the windows that are constructed during a run share the single
#    _master_Tk   (a tkinter.Tk object)
# as their common root.  The first construction of a RoseWindow
# sets this  _master_Tk  to a Tkinter.Tk object.
# ----------------------------------------------------------------------
_master_Tk = None


# ----------------------------------------------------------------------
# RoseWindow is the top-level object.  It starts with a single RoseCanvas.
# ----------------------------------------------------------------------
class RoseWindow(object):
    """
    A RoseWindow is a window that pops up when constructed.
    It can have   RoseWidgets   on it and starts by default with
    a single  RoseCanvas   upon which one can draw shapes.

    To construct a RoseWindow, use:
    -   rg.RoseWindow()

    or use any of its optional arguments, as in these examples:

    window = rg.RoseWindow(400, 300)  # 400 wide by 300 tall
    window = rg.RoseWindow(400, 300, "Funny window")  # with a title

    Instance variables include:

      width:  width of this window (in pixels)
      height: width of this window (in pixels)
      title:  displayed on the window's bar
      widgets: the things attached to this window
    """

    def __init__(self, width=400, height=300, title="Rose Graphics",
                 color="black", canvas_color=None,
                 make_initial_canvas=True):
        """

        Pops up a   tkinter.Toplevel   window with (by default)
        a   RoseCanvas  (and associated tkinter.Canvas) on it.

        Arguments are:
          -- width, height: dimensions of the window (in pixels).
          -- title:  title displayed on the windoww.
          -- color:  background color of the window
          -- canvas_color:  background color of the canvas
                            displayed on the window by default
          -- make_initial_canvas:
               -- If True, a default canvas is placed on the window.
               -- Otherwise, no default canvas is placed on the window.

        If this is the first RoseWindow constructed, then a
        hidden   Tk   object is constructed to control the event loop.

        Preconditions:
          :type width: int
          :type height: int
          :type title: str
          :type color: Color
          :type canvas_color: Color
          :type make_initial_canvas: bool
        """
#         check_types([(width, (int, float)),
#                      (height, (int, float)),
#                      (title, (Color, str)

        # --------------------------------------------------------------
        # The _master_Tk controls the mainloop for ALL the RoseWindows.
        # If this is the first RoseWindow constructed in this run,
        # then construct the _master_Tk object.
        # --------------------------------------------------------------
        global _master_Tk
        if not _master_Tk:
            _master_Tk = tkinter.Tk()
            _master_Tk.withdraw()
        else:
            time.sleep(0.1)  # Helps the window appear on TOP of Eclipse

        # --------------------------------------------------------------
        # Has a tkinter.Toplevel, and a tkinter.Canvas on the Toplevel.
        # --------------------------------------------------------------
        self.toplevel = tkinter.Toplevel(_master_Tk,
                                         background=color,
                                         width=width, height=height)
        self.toplevel.title(title)
        self._is_closed = False
        self.toplevel.protocol("WM_DELETE_WINDOW", self.close)

        # FIXME: The next two need to be properties to have
        # setting happen correctly.  Really belongs to RoseCanvas.
        # See comments elsewhere on this.

        self.width = width
        self.height = height

        if make_initial_canvas:
            self.initial_canvas = RoseCanvas(self, width, height,
                                             canvas_color)
        else:
            self.initial_canvas = None

        self.widgets = [self.initial_canvas]

        # FIXME: Do any other tailoring of the toplevel as desired,
        #       e.g. borderwidth and style...

        # --------------------------------------------------------------
        # Catch mouse clicks and key presses.
        # --------------------------------------------------------------
        self.mouse = Mouse()
        self.keyboard = Keyboard()
        self.toplevel.bind("<Button>", self._on_mouse_click)
        self.toplevel.bind("<KeyPress>", self._on_key_press)

        self.update()

    def close(self):
        """ Closes this RoseWindow. """
        if self.toplevel:
            self.toplevel.destroy()
            self.toplevel = None
        self.update()
        self._is_closed = True

    def update(self):
        """
        Checks for and handles events that has happened
        in this RoseWindow (e.g. mouse clicks, drawing shapes).
        """
        global _master_Tk
        _master_Tk.update()

    def render(self, seconds_to_pause=None):
        """
        Updates all the Shapes attached to RoseCanvas objects associated
        with this RoseWindow, then draws all those Shapes.
        After doing so, pauses the given number of seconds.
          :type  seconds_to_pause:  float
        """
        for widget in self.widgets:
            if type(widget) == RoseCanvas:
                widget.render()

        self.update()

        if seconds_to_pause:
            time.sleep(seconds_to_pause)

    def close_on_mouse_click(self):
        """
        Displays a message at the bottom center of the window and waits
        for the user to click the mouse anywhere in the window.
        Then closes this RoseWindow.
        Returns an rg.Point that specifies where the user clicked the mouse.
        """
        message = "To exit, click anywhere in this window"
        click_position = self.continue_on_mouse_click(message=message,
                                                      close_it=True)
        return click_position

    def continue_on_mouse_click(self,
                                message="To continue, click anywhere in this window",
                                x_position=None,
                                y_position=None,
                                close_it=False,
                                erase_it=True):
        """
        Displays a message at the bottom center of the window
        and waits for the user to click the mouse, then erases the message.

        Optional parameters let you:
          -- Display a different message
          -- Place the message at a different place in the window
               (xpos and ypos are as in Text)
          -- Close the window after the mouse is clicked (and ignore
               the GraphicsError that results if the user instead chooses
               to click the   X   in the window)
          -- NOT erase the message when done
        """
        if self._is_closed:
            return
        if x_position is None:
            x_position = self.width / 2
        if y_position is None:
            y_position = self.height - 20
        anchor_point = Point(x_position, y_position)
        text = Text(anchor_point, message)

        # FIXME: Really should do all this on a per-RoseCanvas basis.

        if self.initial_canvas:
            text.attach_to(self.initial_canvas)
            self.initial_canvas._renderShape(text, render_NOW=True)

        click_position = self.get_next_mouse_click()

        if erase_it and self.initial_canvas:
            text.detach_from(self.initial_canvas)

        if close_it:
            self.close()  # then close the window

        return click_position

    def get_next_mouse_click(self):
        """
        Waits for the user to click in the window. Then returns the rg.Point
        that represents the point where the user clicked.

        Example:
        If this method is called and then the user clicks near
        the upper-right corner of a 300 x 500 window,
        this function would return something like rg.Point(295, 5).
        """
        self.mouse.position = None
        while True:
            if self._is_closed:
                return None
            if self.mouse.position is not None:
                break
            self.update()
            time.sleep(.05)  # allow time for other events to be handled

        click_point = self.mouse.position
        self.mouse.position = None

        return click_point

    def _on_mouse_click(self, event):
        self.mouse._update(event)

    def _on_key_press(self, event):
        self.keyboard._update(event)

#      def add_canvas(self, width=None, height=None, background_color=0):
# FIXME: Set defaults based on the main canvas.
#         new_canvas = RoseCanvas(self, background_color="white")
#         self.widgets.append(new_canvas)
#
#         _root.update()

    def __serialize_shapes(self):
        """
        Returns a list of strings representing the shapes in sorted order.
        """
        return _serialize_shapes(self)


class RoseWidget(object):
    """
       A Widget is a thing that one can put on a Window,
       e.g. a Canvas, FortuneTeller, etc.
    """

    def __init__(self, window):
        self._window = window

    def get_window(self):
        return self._window


class RoseCanvas(RoseWidget):
    defaults = {"colors": [None, "yellow", "light blue", "dark grey"]}
    count = 0

    """
       A RoseCanvas is a RoseWidget (i.e., a thing on a RoseWindow)
       upon which one can draw shapes and other Drawable things.
    """

    def __init__(self, window, width=200, height=200,
                 background_color=0):
        super().__init__(window)

        RoseCanvas.count = RoseCanvas.count + 1

        # FIXME: Deal with default background colors.
        # FIXME: Store background color as a property
        #        so that modifying it changes the tkinter canvas.
        #        Ditto width and height.


#         if background_color == 0:
#             index = RoseCanvas.count % len(defaults["colors"])
#             self.background_color = defaults["colors"][index]
#         else:
#             self.background_color = background_color

        tk_canvas = tkinter.Canvas(window.toplevel,
                                   width=width, height=height,
                                   background=background_color)
        self._tkinter_canvas = tk_canvas

        # FIXME: Automate gridding better.
        self._tkinter_canvas.grid(padx=5, pady=5)
        self.shapes = []

    def render(self, seconds_to_pause=None):
        """
        Updates all the Shapes attached to this RoseCanvas, then draws
        all those Shapes.  After doing so, pauses the given number of seconds.
          :type  seconds_to_pause:  float
        """
        self._update_shapes()
        self._window.update()

        if seconds_to_pause:
            time.sleep(seconds_to_pause)

    def _renderShape(self, shape, render_NOW=False):
        """Renders a shape."""
        coordinates = shape._get_coordinates_for_drawing()
        options = shape._get_options_for_drawing()

        if shape.shape_id_by_canvas[self] is None:
            shape.shape_id_by_canvas[self] = \
                shape._method_for_drawing(self._tkinter_canvas, *coordinates)

        try:
            self._tkinter_canvas.coords(shape.shape_id_by_canvas[self],
                                        *coordinates)
        except tkinter.TclError:
            msg = "Could not place the shape\n"
            msg += "on the given window.\n"
            msg += "Did you accidentally close a window\n"
            msg += "that later needed to be rendered again?"
            raise Exception(msg) from None

        self._tkinter_canvas.itemconfigure(shape.shape_id_by_canvas[self],
                                           options)
        if render_NOW:
            # redraw NOW
            self._window.update()

    def _draw(self, shape):
        """Queues a shape for being drawn. Does NOT draw it just yet."""
        shapeInList = False
        for listShape in self.shapes:
            if listShape is shape:
                shapeInList = True
                break

        if not shapeInList:
            shape.shape_id_by_canvas[self] = None
            self.shapes.append(shape)

    def _undraw(self, shape):
        if shape in self.shapes:
            for i in range(len(self.shapes)):
                if self.shapes[i] is shape:
                    self._tkinter_canvas.delete(shape.shape_id_by_canvas[self])
                    del self.shapes[i]
                    break

    def _update_shapes(self):
        for shape in self.shapes:
            self._renderShape(shape)


class Mouse(object):

    def __init__(self):
        self.position = None

    def _update(self, event):
        self.position = Point(event.x, event.y)


class Keyboard(object):

    def __init__(self):
        self.key_pressed = None

    def _update(self, event):
        pass


class __FreezeClass__ (type):
    """Prevents class variable assignment."""

    def __setattr__(self, name, _ignored):  # last parameter is the value
        err = "You tried to set the instance variable "" + name + ""\n"
        err += "   on the CLASS "" + self.__name__ + """
        err += ", which is not an OBJECT.\n"
        err += "   Did you forget the () after the word "
        err += self.__name__ + ",\n"
        err += "   on the line where you constructed the object?"
        raise SyntaxError(err)


class _Shape(object, metaclass=__FreezeClass__):
    """
    A Shape is a thing that can be drawn on a RoseCanvas
    (which itself draws on a tkinter Canvas).

    Its constructor provides the tkinter method to be used to
    draw this Shape.

    This abstract type has concrete subclasses that include:
      Arc, Bitmap, Circle, Ellipse, Image, Line, Path, Polygon,
      Rectangle, RoundedRectangle, Square, Text and Window.

    Public data attributes:  None.
    Public methods: attach_to.
    """

    def __init__(self, method_for_drawing):
        """  Arguments:
          -- the tkinter method for drawing the Shape.
        """
        self._method_for_drawing = method_for_drawing
        self.shape_id_by_canvas = {}

    def __eq__(self, other):
        """
        Two Shape objects are equal (==) if all their attributes
        are equal to each other.
        """
        # check before we go deleting keys that may or may not exist
        if(not isinstance(other, self.__class__)):
            return False
        self_dict = self.__dict__.copy()
        other_dict = other.__dict__.copy()
        del self_dict["shape_id_by_canvas"]
        del other_dict["shape_id_by_canvas"]
        return (self_dict == other_dict)

    def __ne__(self, other):
        return not self.__eq__(other)

    def attach_to(self, window_or_canvas):
        """
        "draws" this Shape.  More precisely:
        Attaches this Shape to the given
        RoseWindow or RoseCanvas. When that
        RoseWindow/RoseCanvas is rendered, this shape
        will appear on that RoseWindow/RoseCanvas.
        """
        if isinstance(window_or_canvas, RoseWindow):
            window_or_canvas = window_or_canvas.initial_canvas
        window_or_canvas._draw(self)

    def detach_from(self, rose_canvas):
        """
        "undraws" this Shape.  More precisely:
        Detaches this Shape from the given
        RoseWindow or RoseCanvas. When that
        RoseWindow/RoseCanvas is rendered,
        this shape will no longer appear
        on that RoseWindow/RoseCanvas.
        """
        if type(rose_canvas) == RoseWindow:
            rose_canvas = rose_canvas.initial_canvas
        rose_canvas._undraw(self)


class _ShapeWithOutline(object):
    """
    A Shape that has an interior (which can be filled with a color)
    and an outline (which has a color and thickness).

    This abstract type has concrete subclasses that include:
      Arc, Circle, Ellipse, Image, Line, Path,
      Polygon, Rectangle, Square, Text and Window.

    Public data attributes:  fill_color, outline_color, outline_thickness.
    Public methods:  _initialize_options.
    """
    defaults = {"fill_color": None,
                "outline_color": "black",
                "outline_thickness": 1}

    def _initialize_options(self):
        self.fill_color = _ShapeWithOutline.defaults["fill_color"]
        self.outline_color = _ShapeWithOutline.defaults["outline_color"]
        self.outline_thickness = _ShapeWithOutline.defaults[
            "outline_thickness"]

    def _get_options_for_drawing(self):
        options = {"fill": self.fill_color,
                   "outline": self.outline_color,
                   "width": self.outline_thickness}

        # If a color is None, that means transparent here:
        for option in ("fill", "outline"):
            if not options[option]:
                options[option] = ""

        return options


class _ShapeWithThickness(object):
    """
    A Shape that can be (and almost always is) filled with a color
    and has a thickness but no outline.

    This abstract type has concrete subclasses that include:
      Line and Path.

    Public data attributes:  color, thickness.
    Public methods:  _initialize_options.
    """
    defaults = {"color": "black",
                "thickness": 1,
                "arrow": None}

    def _initialize_options(self):
        self.color = _ShapeWithThickness.defaults["color"]
        self.thickness = _ShapeWithThickness.defaults["thickness"]
        self.arrow = _ShapeWithThickness.defaults["arrow"]

    def _get_options_for_drawing(self):
        options = {"fill": self.color,
                   "width": self.thickness,
                   "arrow": self.arrow}

        # If a color is None, that means "black" here:
        if options["fill"] is None:
            options["fill"] = "black"

        return options


class _ShapeWithText(object):
    """
    A Shape that has text and a font for displaying that text.

    This abstract type has concrete subclasses that include:
      Text.

    Public data attributes:  font_family, font_size,
      is_bold, is_italic, is_underline, is_overstrike.

    Public methods:  _initialize_options.
    """
    # FIXME: Add more to the above docstring.
    defaults = {"font_family": "helvetica",
                "font_size": 14,
                "weight":  "normal",
                "slant":  "roman",
                "underline":  0,
                "overstrike":  0,
                "justify": tkinter.CENTER,
                "text_box_width": None,
                "text_color": "black",
                "text": ""}

    def _initialize_options(self):
        self.font_family = _ShapeWithText.defaults["font_family"]
        self.font_size = _ShapeWithText.defaults["font_size"]
        self.is_bold = _ShapeWithText.defaults["weight"] == "bold"
        self.is_italic = _ShapeWithText.defaults["slant"] == "italic"
        self.is_underline = _ShapeWithText.defaults["underline"] == 1
        self.is_overstrike = _ShapeWithText.defaults["overstrike"] == 1

        self.justify = _ShapeWithText.defaults["justify"]
        self.text_box_width = _ShapeWithText.defaults["text_box_width"]
        self.text_color = _ShapeWithText.defaults["text_color"]
        self.text = _ShapeWithText.defaults["text"]

    def _get_options_for_drawing(self):
        weight = "bold" if self.is_bold else "normal"
        slant = "italic" if self.is_italic else "roman"
        underline = 1 if self.is_underline else 0
        overstrike = 1 if self.is_overstrike else 0
        font = tkinter_font.Font(family=self.font_family,
                                 size=self.font_size,
                                 weight=weight,
                                 slant=slant,
                                 underline=underline,
                                 overstrike=overstrike)

        options = {"font": font,
                   "justify": self.justify,
                   "fill": self.text_color,
                   "text": self.text}
        if self.text_box_width:
            options["width"] = self.text_box_width

        return options


class _ShapeWithCenter(_Shape):
    """
    A Shape that has a center (and for which moving its center
    moves the entire Shape).  Its constructor provides the center
    of the Shape along with its method for drawing this Shape.

    This abstract type has concrete subclasses that include:
      Arc, Bitmap, Circle, Ellipse, Image,
      Rectangle, RoundedRectangle, Square, Text and Window.

    Public data attributes: center.
    Public methods: move_by, move_center_to.
    """

    def __init__(self, center, method_for_drawing):
        """
        Arguments:
          -- the Point that is the center of the Shape
               (the Shape stores a CLONE of that Point)
          -- the tkinter method for drawing the Shape.
        """
        # Clone the   center   argument, so that if the caller
        # mutates the argument, it does NOT affect this Shape.
        super().__init__(method_for_drawing)
        self.center = center.clone()

    def move_by(self, dx, dy):
        """
        Moves this _Shape to the right by dx and down by dy.
        Negative values move it to the left/up instead.
        Does NOT return a value; instead, it mutates this shape.
          :type  dx: float
          :type  dy: float
        """
        self.center.move_by(dx, dy)

    def move_center_to(self, x, y):
        """
        Moves this _Shape's center to (x, y),
        thus translating the entire Shape
        by however much its center moved.
          :type  x:  float
          :type  y:  float
        """
        self.center.move_to(x, y)


class _RectangularShape(_Shape):
    """
    A _Shape determined by its rectangular bounding box (plus possibly
    other information).
    Concrete sub-classes include:  rg.Ellipse, rg.Rectangle.

    Examples:
    These all assume that the variable  shape  is a _RectangularShape
    (e.g. an rg.Ellipse or a rg.Rectangle):

    The methods in these examples all return rg.Point objects that are
    copies of a corner/center of the _RectangularShape:
       ul = shape.get_upper_left_corner()
       ur = shape.get_upper_right_corner()
       ll = shape.get_lower_left_corner()
       lr = shape.get_lower_right_corner()
       center = shape.get_center()

    The methods in these examples return a positive number:
      h = shape.get_height()
      w = shape.get_width()

    The method in this example returns an rg.Rectangle that encloses
    this _RectangularShape:
      bbox = shape.get_bounding_box()

    This example moves this _RectangularShape right 100 and up 50:
      shape.move_by(100, -50)

    This example does the same thing another way:
      shape.corner_1 = shape.corner_1 + 100
      shape.corner_2 = shape.corner_2 - 50
    """

    def __init__(self, corner_1, corner_2, method_for_drawing):
        """
          :type  corner_1:  Point
          :type  corner_2:  Point
          :type  method_for_drawing: callable(int, int, int, int) -> int
        """
        super().__init__(method_for_drawing)

        self.corner_1 = corner_1.clone()
        self.corner_2 = corner_2.clone()

        self._update_corners()

    def __repr__(self):
        """ Returns a string representation of this shape. """
        f_string = ""
        f_string += "{}: corner_1=({}, {}), corner_2=({}, {}),"
        f_string += " fill_color={},"
        f_string += " outline_color={}, outline_thickness={}."
        return f_string.format(self.__class__.__name__,
                               self.corner_1.x, self.corner_1.y,
                               self.corner_2.x, self.corner_2.y,
                               self.fill_color, self.outline_color,
                               self.outline_thickness)

    def move_by(self, dx, dy):
        """
        Moves this _Shape to the right by dx and down by dy.
        Negative values move it to the left/up instead.
        Does NOT return a value; instead, it mutates this shape.
          :type  dx: float
          :type  dy: float
        """
        self.corner_1.x += dx
        self.corner_1.y += dy
        self.corner_2.x += dx
        self.corner_2.y += dy

    def clone(self):
        """
        Returns a copy of this _RectangularShape.
        """
        return self.__class__(self.corner_1.clone(),
                              self.corner_2.clone())

    def get_upper_left_corner(self):
        """
        Returns a copy of the ** upper-left **
        corner of this _RectanglarShape.
        The returned value is an rg.Point.
        """
        self._update_corners()
        return self._upper_left_corner

    def get_lower_left_corner(self):
        """
        Returns a copy of the ** lower-left **
        corner of this _RectanglarShape.
        The returned value is an rg.Point.
        """
        self._update_corners()
        return self._lower_left_corner

    def get_upper_right_corner(self):
        """
        Returns a copy of the ** upper-right **
        corner of this _RectanglarShape.
        The returned value is an rg.Point.
        """
        self._update_corners()
        return self._upper_right_corner

    def get_lower_right_corner(self):
        """
        Returns a copy of the ** lower-right **
        corner of this _RectanglarShape.
        The returned value is an rg.Point.
        """
        self._update_corners()
        return self._lower_right_corner

    def get_center(self):
        """
        Returns a copy of the ** center ** of this _RectanglarShape.
        The returned value is an rg.Point.
        """
        return Point((self.corner_1.x + self.corner_2.x) / 2,
                     (self.corner_1.y + self.corner_2.y) / 2)

    def get_height(self):
        """
        Returns the height (i.e., the size in
        the y-direction) of this _RectangularShape.
        The returned value is always positive.
        """
        return abs(self.corner_1.y - self.corner_2.y)

    def get_width(self):
        """
        Returns the width (i.e., the size in
        the x-direction) of this _RectangularShape.
        The returned value is always positive.
        """
        return abs(self.corner_1.x - self.corner_2.x)

    def get_bounding_box(self):
        """
        Returns an rg.Rectangle that encloses this _RectangularShape.
        """
        return Rectangle(self.corner_1, self.corner_2)

    def _update_corners(self):
        min_x = min(self.corner_1.x, self.corner_2.x)
        min_y = min(self.corner_1.y, self.corner_2.y)
        max_x = max(self.corner_1.x, self.corner_2.x)
        max_y = max(self.corner_1.y, self.corner_2.y)

        self._upper_left_corner = Point(min_x, min_y)
        self._upper_right_corner = Point(max_x, min_y)
        self._lower_left_corner = Point(min_x, max_y)
        self._lower_right_corner = Point(max_x, max_y)

    def _get_coordinates_for_drawing(self):
        return [self.get_upper_left_corner().x,
                self.get_upper_left_corner().y,
                self.get_lower_right_corner().x,
                self.get_lower_right_corner().y]


class Arc(_RectangularShape, _ShapeWithOutline):
    """ Not yet implemented. """


class Bitmap(_Shape):
    """ Not yet implemented. """


class Circle(_ShapeWithCenter, _ShapeWithOutline):
    """
    A Shape that is an circle.

    To construct a Circle, use:
    -   rg.Circle(center, radius)
    where   center   is an rg.Point object
    and     radius   is a positive integer.

    For example:
    -   rg.Circle(rg.Point(100, 75), 30)
    specifies the circle whose center
    is at (100, 75) and whose radius is 30.

    Instance variables include:

    center:  An rg.Point that specifies
    the center of the Circle.

    radius:  The radius of the Circle.

    fill_color:
    The Circle is filled with this color.
    Example:  circle.fill_color = "green"

    outline_color:
    The outline of the Circle is this color.
    Example:  circle.outline_color = "blue"

    outline_thickness:  The thickness (in pixels)
    of the outline of the Circle.

    Examples:
       circle = rg.Circle(rg.Point(100, 75), 30)

       print(circle.center, circle.radius)

       circle.fill_color = "blue"
       circle.outline_color = "black"
       circle.outline_thickness = 5

       window = rg.RoseWindow()
       circle.attach_to(window)

       circle.move_center_to(300, 200)
       circle.move_by(-50, 60)

       # Another way to move the Circle:
       x = circle.center.x
       y = circle.center.y
       circle.center = rg.Point(x - 50, y + 60)
    """

    def __init__(self, center, radius):
        """
          :type  center:  rg.Point
          :type  radius:  int
        """
        # The following sets instance variable
        #   self.center
        # to a clone (copy) of the given rg.Point.
        super().__init__(center, tkinter.Canvas.create_oval)

        # The following sets default values for:
        #   self.fill_color
        #   self.outline_color
        #   self.outline_thickness
        super()._initialize_options()

        # The radius is also stored in an instance variable:
        self.radius = radius

    def __repr__(self):
        """ Returns a string representation of this Circle. """
        f_string = ""
        f_string += "Circle: center=({}, {}), radius={}, fill_color={}, "
        f_string += "outline_color={}, outline_thickness={}."
        return f_string.format(self.center.x, self.center.y,
                               self.radius,
                               self.fill_color, self.outline_color,
                               self.outline_thickness)

    def clone(self):
        """ Returns a copy of this Circle. """
        return Circle(self.center, self.radius)

    def get_bounding_box(self):
        """
        Returns an rg.Rectangle that encloses this Circle.
        """
        c1 = Point(self.center.x - self.radius,
                   self.center.y - self.radius)
        c2 = Point(self.center.x + self.radius,
                   self.center.y + self.radius)
        return Rectangle(c1, c2)

    def _get_coordinates_for_drawing(self):
        return self.get_bounding_box()._get_coordinates_for_drawing()


class Ellipse(_RectangularShape, _ShapeWithOutline):
    """
    A Shape that is an ellipse (aka oval).

    To construct an Ellipse, use:
    -   rg.Ellipse(corner1, corner2)
    where   corner1   and   corner2   are
    rg.Point objects that specify opposite
    corners of the imaginery rectangle that
    encloses the Ellipse.

    For example:
    -   rg.Ellipse(rg.Point(100, 50),
    -              rg.Point(300, 200))
    specifies the ellipse whose imaginery
    rectangle that encloses the ellipse:
      - has upper-left corner (100, 50) and
      - lower-right corner(300, 200).

    Another example:
    -   rg.Ellipse(rg.Point(300, 50),
    -              rg.Point(100, 200))
    specifies the same ellipse.
    Any two opposite corners can be used.

    Instance variables include:

    corner_1:  An rg.Point that specifies
    one corner of the imaginery rectangle
    that encloses the Ellipse.

    corner_2:  An rg.Point that specifies an
    opposite corner of the imaginery rectangle
    that encloses the Ellipse.

    fill_color:
    The Ellipse is filled with this color.
    Example:  ellipse.fill_color = "green"

    outline_color:
    The outline of the Ellipse is this color.
    Example:  ellipse.outline_color = "blue"

    outline_thickness:  The thickness (in pixels)
    of the outline of the Ellipse.

    Examples:
       p1 = rg.Point(100, 50)
       p2 = rg.Point(300, 200)
       ellipse = rg.Rectangle(p1, p2)

       print(ellipse.corner_1, ellipse.corner_2)

       ellipse.fill_color = "blue"
       ellipse.outline_color = "black"
       ellipse.outline_thickness = 5

       window = rg.RoseWindow()
       ellipse.attach_to(window)

       ellipse.move_to(300, 200)
       ellipse.move_by(-50, 60)

       # Another way to move the Ellipse:
       ellipse.corner_1 = rect.corner_1 - 50
       ellipse.corner_2 = rect.corner_2 + 60

       # To get rg.Points for the corners/center:
       ul = ellipse.get_upper_left_corner()
       ur = ellipse.get_upper_right_corner()
       ll = ellipse.get_lower_left_corner()
       lr = ellipse.get_lower_right_corner()
       center = ellipse.get_center()

       # To get the width/height (always positive):
       h = ellipse.get_height()
       w = ellipse.get_width()
    """

    def __init__(self, corner_1, corner_2):
        """
          :type  corner_1:  rg.Point
          :type  corner_2:  rg.Point
        """
        # The following sets instance variables
        #   self.corner_1
        #   self.corner_2
        # to clones (copies) of the given rg.Points.
        super().__init__(corner_1, corner_2,
                         tkinter.Canvas.create_oval)

        # The following sets default values for:
        #   self.fill_color
        #   self.outline_color
        #   self.outline_thickness
        super()._initialize_options()


class Line(_Shape, _ShapeWithThickness):
    """
    A Shape that is a line segment.

    To construct a Line, use:
    -   rg.Line(start, end)
    where  start  and  end   are rg.Point objects
    that specify the endpoints of the Line.

    For example:
    -   rg.Line(rg.Point(100, 50),
    -           rg.Point(200, 30)
    specifies the Line that starts at (100, 50)
    and ends at (200, 30).

    Another example:
    -   rg.Line(rg.Point(200, 30),
    -           rg.Point(100, 50)
    specifies the Line that is the same as the
    previous example except that the start and
    end points are reversed.  This is important
    if the Line's "arrow" type is not None.

    Instance variables include:

      start:
      The rg.Point that is one end of the Line.

      end:
      The rg.Point that is the other end of the Line.

      color:  The Line is drawn with this color.

      thickness:  The thickness (in pixels) of the Line.

      arrow:  Specifies whether or not the Line
      is drawn as an arrow. Possible values are:
      - None      draw the Line without arrow-heads
      - "first"   draw an arrow-head at the start
      - "last"    draw an arrow-head at the end
      - "both"    draw an arrow-head at both
      For example, if my_line is a Line, then
      -    my_line.arrow = "last"
      makes the Line be drawn as an arrow
      from its start point to its end point.

    Examples:
       start = rg.Point(100, 50)
       end = rg.Point(200, 30)
       line = rg.Line(start, end)

       line.color = "blue"
       line.thickness = 3
       line.arrow = "both"  # A double-sided arrow
       line.arrow = None    # Just a line (no arrow)
       line.arrow = "first" # Arrow from end to start
       line.arrow = "last"  # Arrow from start to end

       window = rg.RoseWindow()
       line.attach_to(window)

       line.move_by(-50, 60)
    """

    def __init__(self, start, end):
        """
          :type  start:  rg.Point
          :type  end:    rg.Point
        """
        super().__init__(tkinter.Canvas.create_line)

        # The following sets default values for:
        #   self.color
        #   self.thickness
        #   self.arrow
        super()._initialize_options()

        # The other instance variables are the endpoints:
        self.start = start.clone()
        self.end = end.clone()

    def __repr__(self):
        """ Returns a string representation of this Line. """
        f_string = ""
        f_string += "Line: start=({}, {}), end=({}, {}), color={}, "
        f_string += "thickness={}, arrow={}."
        return f_string.format(self.start.x, self.start.y,
                               self.end.x, self.end.y,
                               self.color, self.thickness, self.arrow)

    def clone(self):
        """ Returns a copy of this Line. """
        return Line(self.start, self.end)

    def move_by(self, dx, dy):
        """
        Moves both endpoints of this Line
        (and hence the entire Line as well)
        to the right by dx and down by dy.
        Negative values move it to the left/up instead.
        Does NOT return a value; instead, it mutates this Line.
          :type  dx: float
          :type  dy: float
        """
        self.start.move_by(dx, dy)
        self.end.move_by(dx, dy)

    def get_midpoint(self):
        """
        Returns an rg.Point at the midpoint (center) of this Line.
        """
        return Point((self.start.x + self.end.x) / 2,
                     (self.start.y + self.end.y) / 2)

    def _get_coordinates_for_drawing(self):
        return [self.start.x,
                self.start.y,
                self.end.x,
                self.end.y]


class Path(_Shape, _ShapeWithThickness):
    """ Not yet implemented. """


class Point(_Shape, _ShapeWithOutline):
    """
    A Shape that is a point in two-dimensional space.
    It is drawn as a small circle (dot).

    To construct a Point, use:
    -   rg.Point(x, y)
    where  x  and  y   are the Point's coordinates.

    For example:
    -   rg.Point(100, 50)
    specifies the point whose x value is 100
    and whose y value is 50.

    Instance variables include the following:

    x:  The x-coordinate of the Point.

    y:  The y-coordinate of the Point.

    fill_color:
    The Point is filled with this color.
    Note that a Point is drawn as a small, filled
    circle, which is why it has a fill_color, etc.
    Example:  p.fill_color = "green"

    outline_color:
    The outline of the Point is this color.
    Example:  p.outline_color = "blue"

    outline_thickness:  The thickness (in pixels)
    of the outline of the Point.

    Examples:
       p = rg.Point(100, 50)

       print(p.x, p.y)

       window = rg.RoseWindow()
       p.attach_to(window)

       p.move_to(300, 200)
       p.move_by(-50, 60)

       # Another way to move the Point:
       p.x = p.x - 50
       p.y = p.y + 60

       p.fill_color = "blue"
       p.outline_color = "black"
       p.outline_thickness = 1
    """
    defaults = {"width_for_drawing": 5,
                "height_for_drawing": 5,
                "fill_color": "black",
                "outline_color": "black",
                "outline_thickness": 1}

    def __init__(self, x, y):
        """
          :type  x:  float
          :type  y:  float
        """
        super().__init__(tkinter.Canvas.create_oval)

        self.fill_color = Point.defaults["fill_color"]
        self.outline_color = Point.defaults["outline_color"]
        self.outline_thickness = Point.defaults["outline_thickness"]

        self.x = x
        self.y = y

        self.width_for_drawing = Point.defaults["width_for_drawing"]
        self.height_for_drawing = Point.defaults["height_for_drawing"]

    def __repr__(self):
        """ Returns a string representation of this Point. """
        return "Point({:.1f}, {:.1f})".format(self.x, self.y)

    def clone(self):
        """ Returns a copy of this Point. """
        return Point(self.x, self.y)

    def move_by(self, dx, dy):
        """
        Moves this Point to the right by dx and down by dy.
        Negative values move it to the left/up instead.
        Does NOT return a value; instead, it mutates this Point.
          :type  dx: float
          :type  dy: float
        """
        self.x = self.x + dx
        self.y = self.y + dy

    def move_to(self, x, y):
        """
        Moves this Point to (x, y).
        Does NOT return a value; instead, it mutates this Point.
          :type  x: float
          :type  y: float
        """
        self.x = x
        self.y = y

    def get_bounding_box(self):
        """
        Returns an rg.Rectangle that encloses
        this Point (viewing it as a dot).
        """
        c1 = Point(self.x - self.width_for_drawing / 2,
                   self.y - self.width_for_drawing / 2)
        c2 = Point(self.x + self.height_for_drawing / 2,
                   self.y + self.height_for_drawing / 2)
        return Rectangle(c1, c2)

    def _get_coordinates_for_drawing(self):
        return self.get_bounding_box()._get_coordinates_for_drawing()


class Polygon(_Shape, _ShapeWithOutline):
    """ Not yet implemented. """


class Rectangle(_RectangularShape, _ShapeWithOutline):
    """
    A Shape that is a rectangle.

    To construct a Rectangle, use:
    -   rg.Rectangle(corner1, corner2)
    where   corner1   and   corner2   are
    rg.Point objects that specify opposite
    corners of the rectangle.

    For example:
    -   rg.Rectangle(rg.Point(100, 50),
    -                rg.Point(300, 200))
    specifies the rectangle:
      - whose upper-left corner is (100, 50) and
      - whose lower-right corner is (300, 200).

    Another example:
    -   rg.Rectangle(rg.Point(300, 50),
    -                rg.Point(100, 200))
    specifies the same rectangle.
    Any two opposite corners can be used.

    Instance variables include:

    corner_1:  An rg.Point that specifies
    one corner of the Rectangle.

    corner_2:  An rg.Point that specifies
    an opposite corner of the Rectangle.

    fill_color:
    The Rectangle is filled with this color.
    Example:  rect.fill_color = "green"

    outline_color:
    The outline of the Rectangle is this color.
    Example:  rect.outline_color = "blue"

    outline_thickness:  The thickness (in pixels)
    of the outline of the Rectangle.

    Examples:
       p1 = rg.Point(100, 50)
       p2 = rg.Point(300, 200)
       rect = rg.Rectangle(p1, p2)

       print(rect.corner_1, rect.corner_2)

       rect.fill_color = "blue"
       rect.outline_color = "black"
       rect.outline_thickness = 5

       window = rg.RoseWindow()
       rect.attach_to(window)

       rect.move_to(300, 200)
       rect.move_by(-50, 60)

       # Another way to move the Rectangle:
       rect.corner_1 = rect.corner_1 - 50
       rect.corner_2 = rect.corner_2 + 60

       # To get rg.Points for the corners/center:
       ul = rect.get_upper_left_corner()
       ur = rect.get_upper_right_corner()
       ll = rect.get_lower_left_corner()
       lr = rect.get_lower_right_corner()
       center = rect.get_center()

       # To get the width/height (always positive):
       h = rect.get_height()
       w = rect.get_width()
    """

    def __init__(self, corner_1, corner_2):
        """
         :type  corner_1:  rg.Point
         :type  corner_2:  rg.Point
        """
        # The following sets instance variables
        #   self.corner_1
        #   self.corner_2
        # to clones (copies) of the given rg.Points.
        super().__init__(corner_1, corner_2,
                         tkinter.Canvas.create_rectangle)

        # The following sets default values for:
        #   self.fill_color
        #   self.outline_color
        #   self.outline_thickness
        super()._initialize_options()

    def get_bounding_box(self):
        """
        Returns a new rg.Rectangle with the same corners as this one.
        """
        return self.clone()


class RoundedRectangle(_RectangularShape, _ShapeWithOutline):
    """ Not yet implemented. """


class Square(_ShapeWithCenter, _ShapeWithOutline):
    """
    A Shape that is an square.

    To construct a Square, use:
    -   rg.Square(center, length_of_each_side)
    where   center   is an rg.Point object
    and   length_of_each_side   is a positive integer.

    For example:
    -   rg.Square(rg.Point(100, 75), 60)
    specifies the square whose center
    is at (100, 75) and whose length of
    each side is 60.  Its corners are at:
    (70, 35), (70, 105), (130, 35), (130, 105).

    Instance variables include:

    center:  An rg.Point that specifies
    the center of the Square.

    radius:  The length of each side of the Square.

    fill_color:
    The Square is filled with this color.
    Example:  square.fill_color = "green"

    outline_color:
    The outline of the Square is this color.
    Example:  square.outline_color = "blue"

    outline_thickness:  The thickness (in pixels)
    of the outline of the Square.

    Examples:
       square = rg.Square(rg.Point(100, 75), 60)

       print(square.center, square.length_of_each_side)

       square.fill_color = "blue"
       square.outline_color = "black"
       square.outline_thickness = 5

       window = rg.RoseWindow()
       square.attach_to(window)

       square.move_center_to(300, 200)
       square.move_by(-50, 60)

       # Another way to move the Square:
       x = square.center.x
       y = square.center.y
       square.center = rg.Point(x - 50, y + 60)
    """

    def __init__(self, center, length_of_each_side):
        """
          :type  center:  rg.Point
          :type  length_of_each_side:  int
        """
        # The following sets instance variable
        #   self.center
        # to a clone (copy) of the given rg.Point.
        super().__init__(center, tkinter.Canvas.create_rectangle)

        # The following sets default values for:
        #   self.fill_color
        #   self.outline_color
        #   self.outline_thickness
        super()._initialize_options()

        # The length of each side is also stored in an instance variable
        self.length_of_each_side = length_of_each_side

    def __repr__(self):
        """ Returns a string representation of this Square. """
        f_string = ""
        f_string += "Square: center=({}, {}), side-lengths={}, "
        f_string += "fill_color={}, outline_color={}, outline_thickness={}."
        return f_string.format(self.center.x, self.center.y,
                               self.length_of_each_side,
                               self.fill_color, self.outline_color,
                               self.outline_thickness)

    def clone(self):
        """ Returns a copy of this Square. """
        return Square(self.center, self.length_of_each_side)

    def get_bounding_box(self):
        """
        Returns a rg.Rectangle with the same corners as this Square.
        """
        c1 = Point(self.center.x - self.length_of_each_side / 2,
                   self.center.y - self.length_of_each_side / 2)
        c2 = Point(self.center.x + self.length_of_each_side / 2,
                   self.center.y + self.length_of_each_side / 2)
        return Rectangle(c1, c2)

    def _get_coordinates_for_drawing(self):
        return self.get_bounding_box()._get_coordinates_for_drawing()


class Text(_ShapeWithCenter, _ShapeWithText):
    """
    A Shape that has a string of text on it, displayed horizontally.

    Its constructor specifies the rg.Point at which the text
    is centered and the string that is to be displayed.

    Public data attributes: center (an rg.Point),
      font_size (an integer, 5 to 80 or so are reasonable values),
      is_bold (True if the text is to be displayed in BOLD, else False),
      is_italic (True or False),
      is_underline (True or False),
      is _overstrike (True or False),
      text_color (color used to display the text, default is "black")
      text (the string to be displayed).
    Public methods: attach_to, move_by, move_center_to.
    """

    def __init__(self, center, text):
        """
        The first argument must be a rg.Point.
        The second argument must be a string.

        When this Text object is rendered on a window,
        the string (2nd argument) is drawn horizontally on the window,
        centered at the rg.Point that is the 1st argument.

        Preconditions:
           :type center: rg.Point
           :type text str
        """
        super().__init__(center, tkinter.Canvas.create_text)
        super()._initialize_options()

        self.text = text

        # FIXME: Allow __init__ to set the options.

    def __repr__(self):
        return "Text displaying '{}' at position {}".format(self.text,
                                                            self.center)

    # FIXME: Have repr include characteristics??
    # FIXME: Do a clone?

#     def clone(self):
#         return Square(self.center, self.length_of_each_side)

#     def get_bounding_box(self):
#         return Rectangle(self.center,
#                          2 * self.length_of_each_side,
#                          2 * self.length_of_each_side)

# FIXME: Implement bounding_box using the tkinter function for it.

    def _get_coordinates_for_drawing(self):
        return [self.center.x, self.center.y]

# Mark: Window/RoseWindow naming collision is causing mass confusion.
# class Window(_Shape):
#    """ Not yet implemented. """
#    default_options = {}


# CONSIDER: Are these right for here?
class Button(_Shape):
    """ Not yet implemented. """
    default_options = {}


class Entry(_Shape):
    """ Not yet implemented. """
    default_options = {}


class Color(object):
    """
    A Color represents a  fill or outline color created from custom
    amounts of red, green, and blue light. The arguments are:
    - The RED component (0-255),
    - the GREEN component (0-255),
    - the BLUE component (0-255).

    This Color can be passed to RoseGraphics colors
    such as fill_color and outline_color.
    """

    def __init__(self, red, green=None, blue=None):
        self.red = red
        self.green = green
        self.blue = blue

    def __repr__(self):
        return "#{:02x}{:02x}{:02x}".format(self.red, self.green, self.blue)


# begin STUB code for testing

class _RoseWindowStub(RoseWindow):

    def __init__(self, width=400, height=300, title="Rose Graphics",
                 color="black", canvas_color=None,
                 make_initial_canvas=True):
        canvas_color = "white"  # FIXME
        self._is_closed = False
        self.width = width
        self.height = height
        self.initial_canvas = _RoseCanvasStub(
            self, width, height, canvas_color)

    def render(self, seconds_to_pause=None):
        pass

    def get_next_mouse_click(self):
        return Point(0, 0)

    def close_on_mouse_click(self):
        return None

    def continue_on_mouse_click(self,
                                message=("To continue, " +
                                         "click anywhere in this window"),
                                x_position=None,
                                y_position=None,
                                close_it=False,
                                erase_it=True):
        return None

    def _serialize_shapes(self):
        """
        Returns a list of strings representing the shapes in sorted order.
        """
        return _serialize_shapes(self)


class _RoseCanvasStub(RoseCanvas):

    def __init__(self, window, width, height, canvas_color):
        # super().__init__(window, width, height, canvas_color)
        # canvases.append(self)
        self.shapes = []

    def _draw(self, shape):
        # super()._draw(shape)
        self.shapes.append(shape)

    def render(self, seconds_to_pause=None):
        # super().render()  # don"t pause
        pass


class TurtleWindow(object):

    def __init__(self):
        self._screen = turtle.Screen()
        turtle.Turtle._screen = self._screen

    def close_on_mouse_click(self):
        message = "To exit, click anywhere in this window"
        self.display_message(message, Point(0, 280))

        self._screen.exitonclick()

        # We may need the statement:
        #   turtle.TurtleScreen._RUNNING = True
        # in case we open a subsequent TurtleWindow during this run.
        # The  turtle  library seems not to allow for that possibility
        # (it uses a CLASS variable _RUNNING where I would have expected
        # an INSTANCE variable).
        # The next statement appeared to have a visible effect
        # (something flashed) but nothing worse.  At time time
        # it is commented-out, since we need only a single TurtleWindow.

        # turtle.TurtleScreen._RUNNING = True

    def display_message(self, message, point):
        """ Displays the given message at the given Point. """
        self._screen._canvas.create_text(point.x, point.y, text=message)

    def delay(self, milliseconds=None):
        self._screen.delay(milliseconds)

    def tracer(self, n=None, delay=None):
        self._screen.tracer(n, delay)

    def update(self):
        self._screen.update()


class ShapesWindow(RoseWindow):
    pass


class SimpleTurtle(object):
    """
    A SimpleTurtle is a Turtle with restricted (simpler) functionality.
    It can move forward/backward (units are pixels), turn (spin)
    left/right (units are degrees), and more.

    To construct a SimpleTurtle, use:
       rg.SimpleTurtle(shape)
    where  shape  is OPTIONAL and can be any of:  "turtle"
    "arrow"  "classic"  "square"  "circle"  "triangle"  "blank"

    Instance variables include:

      speed:  An integer from 1 (slowest) to 10 (fastest) that
              determines how fast the SimpleTurtle moves.

      pen:  an  rg.Pen  object (see example below) that determines
              the color and thickness of the line
              that the SimpleTurtle draws when moving

      paint_bucket:  an  rg.PaintBucket  object (see example below)
              that determines the color with which the SimpleTurtle
              "fills" shapes indicated by using the  begin_fill  and
              end_fill  methods.

    Examples:
       natacha = rg.SimpleTurtle()
       natacha.forward(100)

       boris = rg.SimpleTurtle("turtle")
       boris.speed = 8
       boris.pen = rg.Pen("blue", 5)  # blue line 5 pixels thick
       boris.paint_bucket = rg.PaintBucket("red")

       # Moves with pen down, then with pen up, then with pen down again:
       boris.left(90)
       boris.forward(-300)
       boris.pen_up()
       boris.go_to(rg.Point(100, -50)
       boris.pen_down()
       boris.backward(75)

       # Moves with the enclosed space "filled" with the paint_bucket
       boris.begin_fill()
         ... movements ...
       boris.end_fill()
    """

    def __init__(self, shape="classic"):
        """
        What comes in:
          A turtle.Shape that determines how the Turtle looks.
          Defaults to a Bitmap of the "classic" Turtle (an arrowhead) from
          early Turtle Graphics.  Shapes allowed are:
          "turtle"  "arrow"  "classic"  "square"  "circle"  "triangle"  "blank"

        Side effects: Constructs and stores in  self._turtle  the "real" Turtle
          to do all the work on behalf of this SimpleTurtle.  This (purposely)
          restricts what this SimpleTurtle knows and can do.

        :type shape: str
        """
        self.speed = 1
        self.pen = Pen("black", 1)
        self.paint_bucket = PaintBucket("black")

        self._turtle = turtle.Turtle(shape)
        self._update_real_turtle()

    def forward(self, distance):
        """
        Makes this SimpleTurtle go forward the given distance
        (in pixels).  Example (assuming  sally  is an rg.SimpleTurtle):

        sally.forward(200)

        """
        self._update_real_turtle()
        self._turtle.forward(distance)

    def backward(self, distance):
        """
        Makes this SimpleTurtle go backward the given distance
        (in pixels).  Example (assuming  sally  is an rg.SimpleTurtle):

        sally.backward(200)

        """
        self._update_real_turtle()
        self._turtle.backward(distance)

    def left(self, angle):
        """
        Makes this SimpleTurtle turn (i.e. spin) left the given distance
        (in degrees).  Example (assuming  sally  is an rg.SimpleTurtle):

        sally.left(45)

        """
        self._update_real_turtle()
        self._turtle.left(angle)

    def right(self, angle):
        """
        Makes this SimpleTurtle turn (i.e. spin) right the given distance
        (in degrees).  Example (assuming  sally  is an rg.SimpleTurtle):

        sally.right(45)

        """
        self._update_real_turtle()
        self._turtle.right(angle)

    def go_to(self, point):
        """
        Makes this SimpleTurtle go to the given rg.Point.
        (0, 0) is at the center of the window.
        Example (assuming  sally  is an rg.SimpleTurtle):

        sally.go_to(rg.Point(100, -50))

        """
        self._update_real_turtle()
        self._turtle.goto(point.x, point.y)

    def set_heading(self, to_angle):
        """
        Sets the "heading" of this SimpleTurtle, that is,
        the direction that the SimpleTurtle is pointing,
        to the given number of degrees from the x-axis.
        Examples:
           turtle.set_heading(0)
              makes the SimpleTurtle point east (i.e. to the right)
           turtle.set_heading(270)
              makes the SimpleTurtle point south (i.e. down)
           turtle.set_heading(45)
              makes the SimpleTurtle point up and to the right

        The   to_angle   parameter is normally set to a number between
        0 and 360, but negative angles work too, in the way you might expect.

        Type hints:
          :type to_angle: float
        """
        self._update_real_turtle()
        self._turtle.setheading(to_angle)

    def draw_circle(self, radius):
        """
        Makes this SimpleTurtle draw a circle with the given radius.
        Example (assuming  sally  is an rg.SimpleTurtle):

        sally.draw_circle(40)

        """
        self._update_real_turtle()
        self._turtle.circle(radius)

    def draw_square(self, length_of_sides):
        """
        Makes this SimpleTurtle draw a square with the given value
        for the length of each of its sides.
        Example (assuming  sally  is an rg.SimpleTurtle):

        sally.draw_square(100)

        """
        for _ in range(4):
            self.forward(length_of_sides)
            self.left(90)

    def draw_regular_polygon(self, number_of_sides, length_of_sides):
        """
        Makes this SimpleTurtle draw a regular polygon with the given
        number of sides and the given length for each of its sides.
        Example (assuming  sally  is an rg.SimpleTurtle):

        sally.draw_polygon(8, 75)  # octogon
        sally.draw_polygon(3, 75)  # triangle

        """
        for _ in range(number_of_sides):
            self.forward(length_of_sides)
            self.left(360 / number_of_sides)

    def pen_up(self):
        """
        Lifts up this SimpleTurtle's pen.  Subsequent movements
        will NOT draw a line (until  pen_down  is called).
        Example (assuming  sally  is an rg.SimpleTurtle):

        sally.pen_up()

        """
        self._update_real_turtle()
        self._turtle.penup()

    def pen_down(self):
        """
        Puts down this SimpleTurtle's pen.  Subsequent movements
        WILL draw a line using this SimpleTurtle's pen (until pen_up
        is called). Example (assuming  sally  is an rg.SimpleTurtle):

        sally.pen_down()

        """
        self._update_real_turtle()
        self._turtle.pendown()

    def x_cor(self):
        """
        Returns the x-coordinate of this SimpleTurtle's current position.
        Example (assuming  sally  is an rg.SimpleTurtle):

        x = sally.x_cor()

        """
        return self._turtle.xcor()

    def y_cor(self):
        """
        Returns the y-coordinate of this SimpleTurtle's current position.
        Example (assuming  sally  is an rg.SimpleTurtle):

        y = sally.y_cor()

        """
        return self._turtle.ycor()

    def begin_fill(self):
        """
        Begins "filling" the shape that this SimpleTurtle draws,
        using this SimpleTurtle's paint_bucket as the fill.
        Example (assuming  sally  is an rg.SimpleTurtle) that fills
        a triangle with green:

        sally.paint_bucket = rg.PaintBucket("green")
        sally.begin_fill()

        sally.forward(100)
        sally.left(120)
        sally.forward(100)
        sally.left(120)
        sally.forward(100)

        sally.end_fill()

        """
        self._update_real_turtle()
        self._turtle.begin_fill()

    def end_fill(self):
        """
        Completes "filling" the shape that this SimpleTurtle draws,
        using this SimpleTurtle's paint_bucket as the fill.
        Example (assuming  sally  is an rg.SimpleTurtle) that fills
        a triangle with green:

        sally.paint_bucket = rg.PaintBucket("green")
        sally.begin_fill()

        sally.forward(100)
        sally.left(120)
        sally.forward(100)
        sally.left(120)
        sally.forward(100)

        sally.end_fill()

        """
        self._update_real_turtle()
        self._turtle.end_fill()

    def clear(self):
        """ Not yet implemented. """

    def clone(self):
        """ Not yet implemented. """
        pass

    def write_text(self):
        """ Not yet implemented. """
        pass

    def _update_real_turtle(self):
        self._turtle.pencolor(self.pen.color)
        self._turtle.pensize(self.pen.thickness)
        self._turtle.fillcolor(self.paint_bucket.color)
        self._turtle.speed(self.speed)


class Pen(object):
    """
    A Pen has a color and thickness.
    SimpleTurtles use a Pen for drawing lines.

    To construct a Pen, use:
       rg.Pen(color, thickness)
    where  color   is a color (e.g. "red")
    and   thickness  is a small positive integer.

    Instance variables are:
      color:  The color of the Pen
      thickness:  The thickness of the Pen

    Examples:
       thick_blue = rg.Pen("blue", 14)
       thin_red = rg.Pen("red", 1)
    """

    def __init__(self, color, thickness):
        self.thickness = thickness
        self.color = color


class PaintBucket(object):
    """
    A PaintBucket has a color.
    SimpleTurtles use a PaintBucket for filling shapes with color.

    To construct a PaintBucket, use:
       rg.PaintBucket(color)
    where  color   is a color (e.g. "red").

    Instance variables are:
      color:  The color of the PaintBucket

    Example:
       paint = rg.PaintBucket("green")
    """

    def __init__(self, color):
        self.color = color


# ----------------------------------------------------------------------
# At the risk of not being Pythonic, we provide a simple type-checking
# facility that attempts to provide meaningful error messages to
# students when they pass arguments that are not of the expected type.
# ----------------------------------------------------------------------
class WrongTypeException(Exception):
    """ Not yet implemented. """
    pass


def check_types(pairs):
    """ Not yet implemented fully. """
    for pair in pairs:
        value = pair[0]
        expected_type = pair[1]
        if not isinstance(value, expected_type):
            raise WrongTypeException(pair)


# ----------------------------------------------------------------------
# Serialization facility
# ----------------------------------------------------------------------


def _serialize_shapes(self):
    """ Returns a list of strings representing the shapes in sorted order. """
    # Idea: dump all the stats on all shapes,
    # then return a sorted list for easy comparison.
    # Problem: the order in which keys appear in dictionaries is random!
    # Solution: sort keys and manually print
    shapes = [shape.__dict__ for shape in self.initial_canvas.shapes]
    keys_by_shape = [sorted(shape) for shape in shapes]

    for k in range(len(shapes)):
        shapes[k]["_method_for_drawing"] = None
        shapes[k]["shape_id_by_canvas"] = None

    result = []
    for k in range(len(keys_by_shape)):
        shape = shapes[k]
        result.append([])
        for key in keys_by_shape[k]:
            result[-1].append(str(key) + ":" + str(shape[key]))
        result[-1] = str(result[-1])
    return "\n".join(sorted(result))

# FIXME (errors):
#  -- clone() does not really make a copy; it just makes a new one
#     but without cloning all the attributes.
#  -- _ShapeWithCenter claims that things like Ellipse are subclasses,
#     but they are not at this point, I think.  In general, need to
#     deal with overlap between _ShapeWithCenter and _RectangularShape.
#     KEEP both of them to have some classes have corner_1 and corner_2
#     while others have center and ...

# FIXME (things that have yet to be implemented):
#  -- Allow multiple canvasses.
#  -- Better close_on ... ala zellegraphics.
#  -- Keyboard.
#  -- Better Mouse.
#  -- Add type hints.
#  -- Catch all Exceptions and react appropriately.
#  -- Implement unimplemented classes.
#  -- Add and allow FortuneTellers and other non-canvas classes.
