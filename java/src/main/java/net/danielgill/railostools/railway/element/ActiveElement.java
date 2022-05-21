package net.danielgill.railostools.railway.element;

import java.util.List;

import net.danielgill.ros.timetable.location.Location;

public class ActiveElement extends Element {
    private int lengthMain;
    private int lengthSide;
    private int speedMain;
    private int speedSide;
    private String activeName;

    private ActiveElement(int speedTag, Location location, int lengthMain, int lengthSide, int speedMain, int speedSide, String name, String activeName) {
        super(ElementType.ACTIVE, speedTag, location, name);
        this.lengthMain = lengthMain;
        this.lengthSide = lengthSide;
        this.speedMain = speedMain;
        this.speedSide = speedSide;
        this.activeName = activeName;
    }

    public static ActiveElement parse(List<String> lines) {
        ActiveElement e = new ActiveElement(
            Integer.parseInt(lines.get(1)), 
            new Location(lines.get(2) + "-" + lines.get(3)), 
            Integer.parseInt(lines.get(4)), 
            lines.get(5) != "-1" ? Integer.parseInt(lines.get(5)) : null, 
            Integer.parseInt(lines.get(6)), 
            lines.get(7) != "-1" ? Integer.parseInt(lines.get(7)) : null, 
            lines.get(8), 
            lines.get(9)
        );
        return e;
    }
    
    public int getLengthMain() {
        return this.lengthMain;
    }

    public int getLengthSide() {
        return this.lengthSide;
    }

    public int getSpeedMain() {
        return this.speedMain;
    }

    public int getSpeedSide() {
        return this.speedSide;
    }

    public String getActiveName() {
        return this.activeName;
    }
}
