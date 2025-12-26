# VS Code Pets Integration Tests

Comprehensive test suite for Fork Monkey sprite generation and video processing.

## Test Files

- **test_assemble_gifs.py**: Tests for GIF assembly (experiment1)
- **test_generate_forkmonkey.py**: Tests for sprite generation (experiment1)
- **test_test_gemini.py**: Tests for Gemini API testing script
- **test_video_processing.py**: Tests for video-to-gif conversion (experiment2)
- **test_json_validation.py**: Tests for JSON data validation

## Running Tests

```bash
# Run all tests
pytest vscode-pets-integration/tests/ -v

# Run specific test file
pytest vscode-pets-integration/tests/test_assemble_gifs.py -v

# Run with coverage
pytest vscode-pets-integration/tests/ --cov=vscode-pets-integration -v
```