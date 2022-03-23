package net.danielgill.railostools.railway;

import java.util.List;

import net.danielgill.ros.timetable.location.Location;
import net.danielgill.ros.timetable.location.NamedLocation;
import net.danielgill.ros.timetable.location.StartLocation;

public class Railway {
    private List<NamedLocation> namedLocations;
    private List<Location> locations;
    private List<StartLocation> startLocations;

    public List<NamedLocation> getNamedLocations() {
        return namedLocations;
    }

    public List<Location> getLocations() {
        return locations;
    }
    
    public List<StartLocation> getStartLocations() {
        return startLocations;
    }
    
}
