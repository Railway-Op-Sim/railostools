package net.danielgill.railostools.railway;

import java.util.List;
import java.util.ArrayList;

import net.danielgill.ros.timetable.location.Location;
import net.danielgill.ros.timetable.location.NamedLocation;
import net.danielgill.ros.timetable.location.StartLocation;

public class Railway {
    private List<NamedLocation> namedLocations;
    private List<RailwayExitLocation> exitLocations;
    private List<RailwayStartLocation> startLocations;

    public List<NamedLocation> getNamedLocations() {
        return namedLocations;
    }

    public List<RailwayExitLocation> getLocations() {
        return exitLocations;
    }
    
    public List<RailwayStartLocation> getStartLocations() {
        return startLocations;
    }

    public void addStation(String name) {
        namedLocations.add(new NamedLocation(name));
    }
    public List<String> getStations() {
        List<String> stations = new ArrayList<String>();
        for (NamedLocation namedLocation : namedLocations) {
            stations.add(namedLocation.toString());
        }
        return stations;
    }
    public NamedLocation getLocationFromString(String station) {
        for (NamedLocation namedLocation : namedLocations) {
            if (namedLocation.toString().equals(station)) {
                return namedLocation;
            }
        }
        return null;
    }


    public void addExit(Location location, String name) {
        exitLocations.add(new RailwayExitLocation(location, name));
    }
    public List<String> getExits() {
        List<String> exits = new ArrayList<String>();
        for (RailwayExitLocation exitLocation : exitLocations) {
            exits.add(exitLocation.getName());
        }
        return exits;
    }
    public RailwayExitLocation getExitFromString(String exit) {
        for (RailwayExitLocation exitLocation : exitLocations) {
            if (exitLocation.getName().equals(exit)) {
                return exitLocation;
            }
        }
        return null;
    }

    public void addStart(StartLocation location, String name) {
        startLocations.add(new RailwayStartLocation(location, name));
    }
    public List<String> getStarts() {
        List<String> starts = new ArrayList<String>();
        for (RailwayStartLocation startLocation : startLocations) {
            starts.add(startLocation.getName());
        }
        return starts;
    }
    public RailwayStartLocation getStartFromString(String start) {
        for (RailwayStartLocation startLocation : startLocations) {
            if (startLocation.getName().equals(start)) {
                return startLocation;
            }
        }
        return null;
    }
    
}
