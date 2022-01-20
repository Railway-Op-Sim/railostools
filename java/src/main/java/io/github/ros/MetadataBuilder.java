package io.github.ros;

import java.io.File;

import com.moandjiezana.toml.Toml;

public class MetadataBuilder {
    public Metadata metadata;

    public MetadataBuilder(File file) {
        Toml toml = new Toml().read(file);
        metadata = toml.to(Metadata.class);
    }
}