package net.danielgill.railostools.railway.element;

import net.danielgill.ros.timetable.location.Location;

public abstract class Element {
    private final Location location;
    public final ElementType type;

    public Element(Location location, ElementType type) {
        this.location = location;
        this.type = type;
    }

    public Location getLocation() {
        return location;
    }

    public ElementType getType() {
        return type;
    }
}
