package net.danielgill.railostools.railway;

import net.danielgill.ros.timetable.location.StartLocation;

public class RailwayStartLocation extends StartLocation {
    private final String name;

    public RailwayStartLocation(StartLocation location, String name) {
        super(location.toString());
        this.name = name + "(" + location.toString() + ")";
    }

    public String getName() {
        return name;
    }
}
