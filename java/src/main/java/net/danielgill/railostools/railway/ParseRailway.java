package net.danielgill.railostools.railway;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Scanner;
import java.util.function.Consumer;

import net.danielgill.railostools.railway.element.ActiveElement;
import net.danielgill.ros.timetable.location.Location;

public class ParseRailway {
    public static Railway parseRailway(File file) throws FileNotFoundException {
        Railway r = new Railway();

        Scanner scanner = new Scanner(file);

        Map<String, Consumer<List<String>>> functions = new HashMap<>();
        functions.put("metadata", ((t) -> parseMetadata(r, t)));
        functions.put("active_elements", ((t) -> parseActiveElement(r, t)));
        functions.put("inactive_elements", ((t) -> parseInactiveElement(r, t)));
        functions.put("text", ((t) -> parseText(r, t)));

        String currParse = "metadata";
        List<String> currLines = new ArrayList<>();

        for(int i = 0; i < getLinesInFile(file); i++) {
            String line = scanner.next();
            if(line.contains("**Active elements**")) {
                Consumer<List<String>> c = functions.get(currParse);
                c.accept(currLines);
                currParse = "active_elements";
                currLines = new ArrayList<>();
                continue;
            } else if(line.contains("**Inactive elements**")) {
                Consumer<List<String>> c = functions.get(currParse);
                c.accept(currLines);
                currParse = "inactive_elements";
                currLines = new ArrayList<>();
                continue;
            } else if(line.contains("***")) {
                Consumer<List<String>> c = functions.get(currParse);
                c.accept(currLines);
                currParse = "text";
                currLines = new ArrayList<>();
                continue;
            }
            currLines.add(line);
        }

        scanner.close();
        return r;
    }

    
    private static void parseMetadata(Railway r, List<String> lines) {
        r.programVersion = lines.get(0);
        r.homeLocation = new Location(lines.get(1) + "-" + lines.get(2));
        r.activeElementCount = Integer.parseInt(lines.get(3));
    }

    private static void parseActiveElement(Railway r, List<String> lines) {
        ActiveElement element = ActiveElement.parse(lines);
        r.addElement(element);
    }

    private static void parseInactiveElement(Railway r, List<String> lines) {

    }

    private static void parseText(Railway r, List<String> lines) {

    }

    private static int getLinesInFile(File f) {
        try {
            BufferedReader reader;
            reader = new BufferedReader(new FileReader(f));
            int lines = 0;
            while(reader.readLine() != null) lines++;
            reader.close();
            return lines;
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            System.exit(1);
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
        return -1;
    }
}
