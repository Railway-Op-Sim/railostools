package net.danielgill.railostools.railway;

import static org.junit.jupiter.api.Assertions.assertNotNull;

import java.io.File;
import java.io.FileNotFoundException;
import java.net.URISyntaxException;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class RailwayTest {

    @Test
    @DisplayName("Testing Railway Parsing")
    public void testRailway() throws URISyntaxException, FileNotFoundException {
        Railway r = ParseRailway.parseRailway(new File(this.getClass().getClassLoader().getResource("Antwerpen_Centraal.rly").toURI()));
        assertNotNull(r);
    }
}
