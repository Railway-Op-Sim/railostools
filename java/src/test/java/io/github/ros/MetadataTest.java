package io.github.ros;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.File;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class MetadataTest {

    @Test
    @DisplayName("Testing TOML Parsing")
    public void tomlParse() {
        MetadataBuilder mb = new MetadataBuilder(new File("src/test/java/io/github/ros/data/Antwerpen_Centraal.toml"));
        assertEquals("Simulation of Antwerp south", mb.metadata.name);
        assertEquals("Krizar", mb.metadata.author);
        assertEquals(Boolean.TRUE, mb.metadata.factual);
        assertEquals("Albert Ball", mb.metadata.contributors.get(0));
        assertEquals(3, mb.metadata.difficulty);
    }
}
