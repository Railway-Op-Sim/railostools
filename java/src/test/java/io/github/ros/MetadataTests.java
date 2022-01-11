package io.github.ros;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.io.File;
import java.io.IOException;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

public class MetadataTests {

    @Test
    @DisplayName("Testing YAML Parsing")
    public void yamlParse() {
        try {
            MetadataBuilder mb = new MetadataBuilder(new File("data/Antwerpen_Centraal.toml"));
            assertEquals("Simulation of Antwerp south", mb.metadata.name);
            assertEquals("Krizar", mb.metadata.author);
            assertEquals(Boolean.TRUE, mb.metadata.factual);
            assertEquals("Albert Ball", mb.metadata.contributors.get(0));
            assertEquals(3, mb.metadata.difficulty);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
