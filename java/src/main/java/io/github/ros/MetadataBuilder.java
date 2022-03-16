package io.github.ros;

import java.io.File;
import java.util.Map;
import java.util.Set;
import java.util.Iterator;
import jakarta.validation.ConstraintViolation;
import jakarta.validation.ValidatorFactory;
import jakarta.validation.Validator;
import jakarta.validation.Validation;

import com.moandjiezana.toml.Toml;

public class MetadataBuilder {
    public Metadata metadata;

    private static Validator validator;
    private static ValidatorFactory factory;

    public class MetadataValidationError extends Exception {  
        public MetadataValidationError(String errorMessage) {  
            super(errorMessage);  
        }  
    }  

    public MetadataBuilder(File file) throws MetadataValidationError {
        factory = Validation.buildDefaultValidatorFactory();
        validator = factory.getValidator();
        Map<String, Object> map = new Toml().read(file).toMap();
        metadata = new Metadata(map);

        Set<ConstraintViolation<Metadata>> constraintViolations = validator.validate(metadata);

        if(!constraintViolations.isEmpty()) {
            StringBuilder stringBuilder = new StringBuilder("Metadata is invalid: ");
            for (Iterator<ConstraintViolation<Metadata>> it = constraintViolations.iterator(); it.hasNext();) {
                ConstraintViolation<Metadata> violation = it.next();
                stringBuilder.append(violation.getPropertyPath()).append(" - ").append(violation.getMessage());
                if (it.hasNext()) {
                    stringBuilder.append("\n");
                }
            }
            throw new MetadataValidationError(stringBuilder.toString());
        }
    }
}