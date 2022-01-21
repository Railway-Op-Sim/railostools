package io.github.ros;

import java.io.File;
import java.util.Map;

import com.moandjiezana.toml.Toml;

public class MetadataBuilder {
    public Metadata metadata;

    public MetadataBuilder(File file) {
        Map<String, Object> map = new Toml().read(file).toMap();
        metadata = new Metadata(map);
    }
}