# WrapperXSelector

**WrapperXSelector** is a tool that simplifies the process of generating web scraping wrappers for Selenium-loaded HTML pages. It provides an interactive user interface for users to select and define the elements they want to scrape on a website, and then generates corresponding Selenium XPath selectors for automation.

## Features

- **User-Friendly Interface:** WrapperXSelector offers a user-friendly interface for selecting and defining elements on a Selenium-loaded HTML page.
- **XPath Generation:** Automatically generates XPath selectors based on user-defined elements for web scraping automation.
- **Dynamic Wrapping:** Supports dynamic websites by allowing users to interact with elements before generating the wrapper.

## How It Works

1. **Setup:** Start by providing the URL of the Selenium-loaded HTML page you want to scrape.
2. **Interactive Selection:** Use the interactive interface to click and select elements on the page that you want to scrape.
3. **XPath Generation:** WrapperXSelector dynamically generates XPath selectors for the selected elements.
4. **Wrapper Output:** Outputs the generated wrapper in JSON format, ready to be used for web scraping automation.

## Usage

```python
from WrapperXSelector import generateWrapper

# Provide the wrapper name, URL, and optional repeated pattern parameter
wrapper_name = "example_wrapper"
url = "https://example.com"
repeated_pattern = "yes"  # Set to "yes" if the pattern repeats, otherwise omit or set to "no"

# Generate the wrapper
wrapper_file = generateWrapper(wrapper_name, url, repeated_pattern)
print(f"Wrapper generated and saved to {wrapper_file}")

pip install WrapperXSelector

**Dependencies:**

- [Selenium](https://pypi.org/project/selenium/)
- [ChromeDriver](https://pypi.org/project/webdriver-manager/)


## License

**MIT License.** See [LICENSE](LICENSE) for details.

## Disclaimer

Intended for educational and legal use only. Users must comply with the terms of service of scraped websites and applicable laws and regulations.

