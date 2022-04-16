package net.danielgill.railostools.railway;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.Set;

import net.danielgill.railostools.railway.element.Element;
import net.danielgill.railostools.railway.element.ElementType;
import net.danielgill.railostools.railway.element.NamedElement;

public class Railway {
    private ArrayList<Element> elements;

    public Railway() {
        elements = new ArrayList<>();
    }

    public void addElement(Element element) {
        elements.add(element);
    }

    public Set<String> getNamedLocations() {
        Set<String> namedLocations = new HashSet<String>();
        for (Element element : elements) {
            if (element.getType() == ElementType.NAMED) {
                NamedElement namedElement = (NamedElement) element;
                namedLocations.add(namedElement.getName());
            }
        }
        return namedLocations;
    }

}
