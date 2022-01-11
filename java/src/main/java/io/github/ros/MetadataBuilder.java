package main.java.io.github.ros;

import java.io.File;

public class MetadataBuilder {
    public Metadata metadata;

    public MetadataBuilder(File file) {
        ObjectMapper om = new ObjectMapper(new YAMLFactory());
        metadata = om.readValue(file, Metadata.class);
        System.out.println("Read data: " + metadata.toString());
    }
}