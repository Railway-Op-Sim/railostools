package net.danielgill.railostools.railway.element;

import net.danielgill.ros.timetable.location.Location;

public class NamedElement extends Element {
    private final String name;
    
    public NamedElement(Location location, String name) {
        super(location, ElementType.NAMED);
        this.name = name;
    }

    public String getName() {
        return name;
    }
    
}
