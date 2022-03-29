package net.danielgill.railostools.railway;

import net.danielgill.ros.timetable.location.Location;

public class RailwayExitLocation extends Location {
    private final String name;

    public RailwayExitLocation(Location location, String name) {
        super(location.toString());
        this.name = name + "(" + location.toString() + ")";
    }

    public String getName() {
        return this.name;
    }
    
}
