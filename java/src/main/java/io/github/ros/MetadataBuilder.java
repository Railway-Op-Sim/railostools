package io.github.ros;

import java.io.File;
import java.io.IOException;

import com.fasterxml.jackson.core.exc.StreamReadException;
import com.fasterxml.jackson.databind.DatabindException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.dataformat.yaml.YAMLFactory;

public class MetadataBuilder {
    public Metadata metadata;

    public MetadataBuilder(File file) throws StreamReadException, DatabindException, IOException {
        ObjectMapper om = new ObjectMapper(new YAMLFactory());
        metadata = om.readValue(file, Metadata.class);
        System.out.println("Read data: " + metadata.toString());
    }
}