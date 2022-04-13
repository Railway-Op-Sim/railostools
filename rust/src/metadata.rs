use toml::Value;
use chrono::NaiveDate;
use semver::Version;
use rust_iso3166::from_alpha2;
use serde::Serialize;
use std::{fs::read_to_string, panic, fs::File, io::Write, fmt::Result};


#[derive(Serialize)]
pub struct Metadata {
    rly_file: String,
    ttb_files: Vec<String>,
    doc_files: Vec<String>,
    ssn_files: Vec<String>,
    img_files: Vec<String>,
    graphic_files: Vec<String>,
    release_date: String,
    version: String,
    minimum_required: String,
    country_code: String,
    factual: bool,
    description: String,
    display_name: String,
    name: String,
    author: String,
    contributors: Vec<String>,
    year: i64
}

impl Metadata {
    pub fn write(&self, mut out_file: File) {
        let toml_data;
        match toml::to_string(self) {
            Ok(t) => toml_data = t,
            Err(e) => panic!("Failed to serialize metadata object with error '{}'", e)
        }

        match write!(out_file, "{}", toml_data) {
            Ok(_n) => (),
            Err(e) => panic!("Failed to write output TOML file with error '{}'", e)
        }
    }
}

fn load_toml_file(file_name: &String) -> Value {
    let mut str_read;

    match read_to_string(file_name) {
        Ok(s) => str_read = s,
        Err(e) => panic!("Failed to read file {} with '{}'", file_name, e)
    }

    match str_read.parse::<Value>() {
        Ok(p) => p,
        Err(e) => panic!("Failed to parse file '{}' with error '{}'", file_name, e)
    }
}

fn val_to_str_vec(label: &String, val_vec: &Vec<Value>) -> Vec<String> {
    let mut out_vec = Vec::<String>::new();

    for value in val_vec {
        match value.as_str() {
            Some(n) => out_vec.push(n.to_string()),
            None => panic!("Failed to parse '{}' in key '{}", value, label)
        }
    }
    out_vec
}

fn retrieve_optionals(file_content: &Value, label: &str, else_str: &str) -> String {
    let val_str;

    match file_content.get(label) {
        Some(n) => val_str = n.as_str(),
        None => val_str = Some(else_str)
    }

    match val_str {
        Some(n) => return n.to_string(),
        None => return else_str.to_string()
    }
}

fn retrieve_country_code(file_content: &Value) -> String {
    let country_code: String;
    match file_content["country_code"].as_str() {
        Some(n) => country_code = n.to_string(),
        None => panic!("Expected value for key 'country_code'")
    }

    if country_code != "FN" {
        match from_alpha2(&country_code) {
            Some(_cc) => country_code,
            None => panic!("Invalid country code '{}'", country_code)
        }
    }
    else {
        country_code
    }
}

pub fn load_metadata_file(file_name: &String) -> Metadata {
    let file_content = load_toml_file(file_name);
    let name: String;
    let rly_file: String;
    let ttb_files: Vec<Value>;
    let ssn_files: Vec<Value>;
    let img_files: Vec<Value>;
    let doc_files: Vec<Value>;
    let graphic_files: Vec<Value>;
    let country_code: String = retrieve_country_code(&file_content);
    let is_factual: bool;
    let description: String;
    let display_name: String;
    let author: String;
    let contributors: Vec<Value>;
    let version_str: String;
    let year: i64;
    let req_ver_str: String;
    let release_date_str: String;

    match file_content["name"].as_str() {
        Some(n) => name = n.to_string(),
        None => panic!("Expected value for key 'name'")
    }

    match file_content["rly_file"].as_str() {
        Some(n) => rly_file = n.to_string(),
        None => panic!("Expected value for key 'rly_file'")
    }

    match file_content["author"].as_str() {
        Some(n) => author = n.to_string(),
        None => panic!("Expected value for key 'author'")
    }

    match file_content["factual"].as_bool() {
        Some(n) => is_factual = n,
        None => panic!("Expected value for key 'factual'")
    }

    description = retrieve_optionals(&file_content, "description", "");

    display_name = retrieve_optionals(&file_content, "display_name", "");

    match file_content["version"].as_str() {
        Some(n) => version_str = n.to_string(),
        None => panic!("Expected value for key 'version'")
    }

    // Only use parser for validation as cannot serialize a semver
    let v_str = &version_str[..];
    match Version::parse(v_str) {
        Ok(v) => (),
        Err(e) => panic!("Failed to parse '{}' as semantic versioning with error '{}'", version_str, e)
    }

    req_ver_str = retrieve_optionals(&file_content, "minimum_required", "0.1.0");

    // Only use parser for validation as cannot serialize a semver
    let rv_str = &req_ver_str[..];
    match Version::parse(rv_str) {
        Ok(_v) => (),
        Err(e) => panic!("Failed to parse '{}' as minimum required program version with error '{}'", version_str, e)
    }

    match file_content["ttb_files"].as_array() {
        Some(n) => ttb_files = n.to_vec(),
        None => panic!("Expected value for key 'ttb_files'")
    }

    match file_content["doc_files"].as_array() {
        Some(n) => doc_files = n.to_vec(),
        None => panic!("Expected value for key 'doc_files'")
    }

    match file_content["img_files"].as_array() {
        Some(n) => img_files = n.to_vec(),
        None => panic!("Expected value for key 'img_files'")
    }

    match file_content["contributors"].as_array() {
        Some(n) => contributors = n.to_vec(),
        None => contributors = vec![]
    }

    match file_content["ssn_files"].as_array() {
        Some(n) => ssn_files = n.to_vec(),
        None => ssn_files = vec![]
    }

    match file_content["graphic_files"].as_array() {
        Some(n) => graphic_files = n.to_vec(),
        None => graphic_files = vec![]
    }

    match file_content["year"].as_integer() {
        Some(n) => year = n,
        None => year = -1
    }

    match file_content["release_date"].as_str() {
        Some(n) => release_date_str = n.to_string(),
        None => panic!("Expected value for key 'release_date'")
    }

    // Only use parser for validation as cannot serialize a datetime
    match NaiveDate::parse_from_str(&release_date_str, "%Y-%m-%d") {
        Ok(r) => (),
        Err(e) => panic!("Failed to parse release date '{}' with error '{}'", release_date_str, e)
    }

    Metadata {
        rly_file,
        ttb_files: val_to_str_vec(&"ttb_files".to_string(), &ttb_files),
        doc_files: val_to_str_vec(&"doc_files".to_string(), &doc_files),
        ssn_files: val_to_str_vec(&"ssn_files".to_string(), &ssn_files),
        graphic_files: val_to_str_vec(&"graphic_files".to_string(), &graphic_files),
        img_files: val_to_str_vec(&"img_files".to_string(), &img_files),
        release_date: release_date_str,
        version: version_str,
        minimum_required: req_ver_str,
        country_code,
        factual: is_factual,
        description,
        display_name,
        name,
        year,
        author,
        contributors: val_to_str_vec(&"contributors".to_string(), &contributors),
    }
}

#[cfg(test)]
mod tests {
    use crate::metadata::{Metadata, load_metadata_file};

    use std::{path::Path};
    use tempfile::tempfile;

    use super::retrieve_country_code;

    fn read_test_toml(file_name: &str) -> String {
        let mut main_dir;
        match Path::new(file!()).parent() {
            Some(p) => main_dir = p,
            None => panic!("Failed to retrieve test TOML file")
        }
        match Path::new(main_dir).parent() {
            Some(p) => main_dir = p,
            None => panic!("Failed to retrieve test TOML file")
        }
        let toml_file = main_dir.join("test_data").join(file_name);

        match toml_file.to_str() {
            Some(s) => s.to_string(),
            None => panic!("Could not retrieve file path string")
        }
    }

    #[test]
    fn test_toml_file_parse() {
        let parsed = load_metadata_file(&String::from(read_test_toml("Antwerpen_Centraal.toml")));
        assert!(parsed.factual == true);
        assert!(parsed.name == "Simulation of Antwerp south");
        assert!(parsed.display_name == "Antwerpen Centraal");
        assert!(parsed.contributors == vec!["Albert Ball"]);
        assert!(parsed.country_code == "BE");
        assert!(parsed.rly_file == "Antwerpen_Centraal.rly");
        assert!(parsed.year == 2021);
        assert!(parsed.author == "Krizar");
        assert!(parsed.minimum_required == "0.1.0");
        assert!(parsed.version == "1.0.0");
        assert!(parsed.release_date == "2021-10-09");
        assert!(parsed.graphic_files == vec!["Antwerp.jpg"]);
        assert!(parsed.ttb_files == vec!["Antwerpen_Centraal_2021.ttb"]);
        assert!(parsed.doc_files == vec!["README.md"]);
        assert!(parsed.ssn_files == vec!["Antwerpen_Centraal_2021.ssn"]);
        assert!(parsed.img_files == vec!["Antwerp_Centraal_2021.bmp"]);
        assert!(parsed.description == "Simulation covering the lines from Antwerpen Centraal to St. Katelijne-Waver/Lier")
    }

    #[test]
    fn test_write_toml() {
        let out_dat = Metadata {
            rly_file: "test.rly".to_string(),
            ttb_files: vec!["test.ttb".to_string()],
            ssn_files: vec![],
            doc_files: vec!["README.md".to_string()],
            img_files: vec!["test.png".to_string()],
            graphic_files: vec![],
            version: "1.0.0".to_string(),
            minimum_required: "0.1.0".to_string(),
            release_date: "2022-04-02".to_string(),
            factual: false,
            country_code: "FN".to_string(),
            contributors: vec![],
            year: 2022,
            name: "Test Route".to_string(),
            description: "".to_string(),
            display_name: "".to_string(),
            author: "Joe Bloggs".to_string()
        };
        let file;

        match tempfile() {
            Ok(t) => file = t,
            Err(e) => panic!("Could not create temporary file: '{}'", e)
        }

        out_dat.write(file);
    }

    #[test]
    #[should_panic(expected="Invalid country code 'YO'")]
    fn test_invalid_country_code() {
        use super::load_toml_file;
        let file_content = load_toml_file(&read_test_toml("invalid_country_code.toml"));
        retrieve_country_code(&file_content);
    }

    #[test]
    fn test_fiction_country_code() {
        use super::load_toml_file;
        let file_content = load_toml_file(&read_test_toml("fictional_country_code.toml"));
        retrieve_country_code(&file_content);
    }
}
