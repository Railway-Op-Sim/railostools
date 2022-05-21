package net.danielgill.railostools.railway.element;

import net.danielgill.ros.timetable.location.Location;

public abstract class Element {
    protected ElementType type;
    protected int speedTag;
    protected Location location;
    protected String name;

    protected Element(ElementType type, int speedTag, Location location, String name) {
        this.type = type;
        this.speedTag = speedTag;
        this.location = location;
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public int getSpeedTag() {
        return this.speedTag;
    }

    public Location getLocation() {
        return this.location;
    }

    public ElementType getType() {
        return this.type;
    }
}
