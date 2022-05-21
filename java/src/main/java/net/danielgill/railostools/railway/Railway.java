package net.danielgill.railostools.railway;

import java.util.ArrayList;
import java.util.List;

import net.danielgill.railostools.railway.element.Element;
import net.danielgill.ros.timetable.location.Location;

public class Railway {
    protected String programVersion = null;
    protected Location homeLocation = null;
    protected int activeElementCount = -1;

    private List<Element> elements;
    private List<String> namedLocations;

    public Railway() {  
        elements = new ArrayList<>();
        namedLocations = new ArrayList<>();
    }

    public void addElement(Element e) {
        elements.add(e);
        if(e.getName() != null) {
            namedLocations.add(e.getName());
        }
    }

    public List<String> getNamedLocations() {
        return this.namedLocations;
    }

}
