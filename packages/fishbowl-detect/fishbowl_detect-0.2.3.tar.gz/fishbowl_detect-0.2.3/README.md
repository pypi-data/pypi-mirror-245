# Fishbowl

This library wraps two Rust-based language detection libraries, [`whatlang`](https://github.com/greyblake/whatlang-rs)
and [`whichlang`](https://github.com/quickwit-oss/whichlang), to provide fast
language detection in Python. The former has a larger set of languages upon
which is will do detection, but is also less confident about its detections.
We use a strategy of first attempting to detect across that broader set, but
if we receive a result the library is not confident about, we fall through
to the latter, which always returns a result, but against a smaller set of
languages. We are using [PyO3](https://pyo3.rs/) to wrap this Rust code.

## Usage

```python
from fishbowl import bulk_detect_language, detect_language

assert detect_language('Well hello there, General Kenobi').name == 'English'
assert detect_language('¿Hola, como estás hoy?').code == 'es'

bulk_input = [
    'Well hello there, General Kenobi',
    '¿Hola, como estás hoy?',
    'Ich bin ein Berliner',
]
bulk_output = bulk_detect_language(bulk_input)

assert [bo.code for _, bo in bulk_output] == ['en', 'es', 'de']
assert [input_str for input_str, _ in bulk_output] == bulk_input
```
