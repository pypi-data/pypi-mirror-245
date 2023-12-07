use pyo3::prelude::*;

const CONFIDENCE_THRESHOLD: f64 = 0.85;

// Higher-fidelity detection with a confidence interval. If we don't get a
// reasonably-confident answer from `whatlang`, we will fall through to `whichlang`,
// which always gives an answer, but which isn't always correct.
#[inline(always)]
fn _attempt_whatlang_detection(input: &str) -> Option<&'static str> {
    let info = whatlang::detect(input)?;

    match info.confidence() >= CONFIDENCE_THRESHOLD {
        true => Some(info.lang().code()),
        false => None,
    }
}

// First attempt detection with `whatlang`, then fall through to `whichlang`.
#[inline(always)]
fn _detect_language(input: &str) -> Option<(&str, Language)> {
    let detected = match _attempt_whatlang_detection(input)
        .unwrap_or_else(|| whichlang::detect_language(input).three_letter_code())
    {
        // Map 'Chinese Mandarin' to 'Chinese'
        "cmn" => "zho",
        code => code,
    };

    isolang::Language::from_639_3(detected).map(|language| {
        (
            input,
            Language {
                code: language.to_639_1().unwrap(),
                name: language.to_name(),
            },
        )
    })
}

#[pyclass]
#[derive(Debug, PartialEq)]
struct Language {
    #[pyo3(get)]
    code: &'static str,

    #[pyo3(get)]
    name: &'static str,
}

#[pymethods]
impl Language {
    fn __repr__(&self) -> String {
        format!("Language(code='{}', name='{}')", self.code, self.name)
    }

    fn __str__(&self) -> String {
        self.code.into()
    }
}

/// detect_language(input)
/// --
///
/// This function computes the two-letter ISO 639-1 language code for a given
/// input string. It is possible that the true language of the given input is
/// not the detected language in cases where the language is less common.
#[pyfunction]
fn detect_language(input: &str) -> PyResult<Option<Language>> {
    match _detect_language(input) {
        Some((_, language)) => Ok(Some(language)),
        None => Ok(None),
    }
}

/// bulk_detect_language(input_list)
/// --
///
/// This function computes the two-letter ISO 639-1 language code for a given
/// list of strings, and returns a tuple of (input_string, language). It is
/// possible that the true language of the given input is not the detected
/// language in cases where the language is less common.
#[pyfunction]
fn bulk_detect_language(input_list: Vec<&str>) -> PyResult<Vec<Option<(&str, Language)>>> {
    Ok(input_list.into_iter().map(_detect_language).collect())
}

/// A Python module implemented in Rust.
#[pymodule]
fn fishbowl(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(detect_language, m)?)?;
    m.add_function(wrap_pyfunction!(bulk_detect_language, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::{bulk_detect_language, detect_language, Language};

    #[test]
    fn test_detect_language() {
        assert!(matches!(
            detect_language("Hello there, General Kenobi"),
            Ok(Some(Language {
                code: "en",
                name: "English"
            }))
        ));
        assert!(matches!(
            detect_language("Voulez vous coucher avec moi?"),
            Ok(Some(Language {
                code: "fr",
                name: "French"
            }))
        ));
        assert!(matches!(
            detect_language("Estudiaba en Santa Barbara"),
            Ok(Some(Language {
                code: "es",
                name: "Spanish"
            }))
        ));
    }

    #[test]
    fn test_chinese_mapping() {
        assert!(matches!(
            detect_language("你好，今天怎么样？"),
            Ok(Some(Language {
                code: "zh",
                name: "Chinese",
            }))
        ));
    }

    #[test]
    fn test_bulk_detect_language() {
        let expected = vec![
            Some((
                "Hello there, General Kenobi",
                Language {
                    code: "en",
                    name: "English",
                },
            )),
            Some((
                "Voulez vous coucher avec moi?",
                Language {
                    code: "fr",
                    name: "French",
                },
            )),
            Some((
                "Estudiaba en Santa Barbara",
                Language {
                    code: "es",
                    name: "Spanish",
                },
            )),
        ];
        let output = bulk_detect_language(vec![
            "Hello there, General Kenobi",
            "Voulez vous coucher avec moi?",
            "Estudiaba en Santa Barbara",
        ])
        .unwrap();

        assert_eq!(output, expected);
    }
}
