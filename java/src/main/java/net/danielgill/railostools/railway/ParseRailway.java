package net.danielgill.railostools.railway;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;

public class ParseRailway {
    public static Railway parseRailway(File file) throws FileNotFoundException {
        Railway r = new Railway();

        Scanner scanner = new Scanner(file);
        String line;
        line = scanner.nextLine(); // version
        line = scanner.nextLine(); // home horizontal offset
        line = scanner.nextLine(); // home vertical offset
        line = scanner.nextLine(); // number of active elements
        line = scanner.nextLine(); // identifier

        return r;
    }
}
