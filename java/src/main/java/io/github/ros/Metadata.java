package io.github.ros;

import java.util.List;

public class Metadata {
    public String name;
    public String author;
    public String description;
    public String display_name;
    public int year;
    public boolean factual;
    public int difficulty;
    public String country_code;
    public String version;
    public String rly_file;
    public List<String> contributors;
    public List<String> ttb_files;
    public List<String> ssn_files;
    public List<String> doc_files;

    public Metadata(String name, String author, String description, String display_name, int year, boolean factual, int difficulty
            String country_code, String version, String rly_file, List<String> contributors, List<String> ttb_files,
            List<String> ssn_files, List<String> doc_files) {
        this.name = name;
        this.author = author;
        this.description = description;
        this.display_name = display_name;
        this.year = year;
        this.factual = factual;
        this.difficulty = difficulty;
        this.country_code = country_code;
        this.version = version;
        this.rly_file = rly_file;
        this.contributors = contributors;
        this.ttb_files = ttb_files;
        this.ssn_files = ssn_files;
        this.doc_files = doc_files;
    }

    public String toString() {
        return "\nName: " + name + "\nAuthor" + author;
    }
}
