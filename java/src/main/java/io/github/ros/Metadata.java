package io.github.ros;

import java.util.List;
import java.util.Date;
import jakarta.validation.constraints.*;
import org.hibernate.validator.constraints.Length;
import org.hibernate.validator.constraints.Range;
import org.hibernate.validator.constraints.UniqueElements;

import de.skuzzle.semantic.Version;

public class Metadata {
    @NotBlank
    public String name;
 
    @NotBlank
    public String author;
 
    public String description;
 
    public String display_name;
 
    @Range(min=1900, max=9999)
    public int year;
 
    public boolean factual;
 
    public int difficulty;

    @NotBlank
    @Length(min=2, max=2)
    public String country_code;

    public Version version;

    @NotBlank
    public String rly_file;

    @UniqueElements
    public List<String> contributors;

    @Size(min=1)
    @UniqueElements
    public List<String> ttb_files;

    @UniqueElements
    public List<String> ssn_files;

    @Size(min=1)
    @UniqueElements
    public List<String> doc_files;

    @UniqueElements
    public List<String> img_files;

    @UniqueElements
    public List<String> graphic_files;

    @NotBlank
    @PastOrPresent
    public Date release_date;


    public Metadata(String name, String author, String description, String display_name, int year, boolean factual, int difficulty,
            String country_code, String version, String rly_file, List<String> contributors, List<String> ttb_files,
            List<String> ssn_files, List<String> doc_files, List<String> img_files, List<String> graphic_files, Date release_date) {
        this.name = name;
        this.author = author;
        this.description = description;
        this.display_name = display_name;
        this.year = year;
        this.factual = factual;
        this.difficulty = difficulty;
        this.country_code = country_code;
        this.version = Version.parseVersion(version);
        this.rly_file = rly_file;
        this.contributors = contributors;
        this.ttb_files = ttb_files;
        this.ssn_files = ssn_files;
        this.doc_files = doc_files;
        this.img_files = img_files;
        this.graphic_files = graphic_files;
        this.release_date = release_date;
    }

    public String toString() {
        return "\nName: " + name + "\nAuthor" + author;
    }
}
