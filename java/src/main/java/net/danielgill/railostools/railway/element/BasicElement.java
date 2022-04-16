package net.danielgill.railostools.railway.element;

import net.danielgill.ros.timetable.location.Location;

public class BasicElement extends Element {

    public BasicElement(Location location) {
        super(location, ElementType.BASIC);
    }
    
}
