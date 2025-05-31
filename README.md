# Static Site Generator
This is a custom-built static site generator. It converts Markdown files into a complete HTML website, manages static assets, and supports configurable deployment paths.

## Features
- Markdown to HTML Conversion: Converts Markdown content into HTML pages.
- Block-level Parsing: Recognizes paragraphs, headings (H1-H6), code blocks, quotes, unordered lists, and ordered lists.
- Inline Markdown: Supports bold, italic, code, images and links.

## Requirements
Python 3.9+

## Usage

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Ksagit/StaticSiteGenerator.git
    cd StaticSiteGenerator
    ```
2.  **Organize your content:**
    *   Put your Markdown content files (e.g., `index.md`, `about.md`) into the `content/` directory. Subdirectories will be mirrored in the output.
    *   Place your static assets (CSS, images, JavaScript, etc.) into the `static/` directory. These will be copied as-is to your output.
    *   Ensure your `template.html` file is in the root of your project.

3.  **Run Tests:**
    ```bash
    ./test.sh
    ```
    This script runs all unit tests to ensure the generator's logic is working correctly.

4.  **Build Your Site (Locally or for Deployment):**
    ```bash
    ./main.sh [optional_basepath]
    ```
    This script performs the full site generation:
    *   It cleans the output directory (`docs/` by default, or `public/` if configured in `main.py`).
    *   Copies all files from `static/` to the output directory.
    *   Converts all Markdown files in `content/` to HTML, placing them in the output directory, maintaining the directory structure.
    *   `[optional_basepath]`: If your site will be hosted in a subdirectory (e.g., `yourdomain.com/blog/`), provide the path like `/blog/`. Otherwise, omit it for root deployments (e.g., `yourdomain.com/`).
