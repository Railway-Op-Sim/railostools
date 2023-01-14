package net.danielgill.railostools.metadata;

import java.io.File;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

public class MetadataTest {

    @Test
    @DisplayName("Testing TOML Parsing")
    public void tomlParse() {

        MetadataBuilder mb = assertDoesNotThrow(() -> new MetadataBuilder(new File(this.getClass().getClassLoader().getResource("Antwerpen_Centraal.toml").toURI())));

        assertEquals("Simulation of Antwerp south", mb.metadata.name);
        assertEquals("Krizar", mb.metadata.author);
        assertEquals(Boolean.TRUE, mb.metadata.factual);
        assertEquals("Albert Ball", mb.metadata.contributors.get(0));
        assertEquals(3, mb.metadata.difficulty);
    }
}
