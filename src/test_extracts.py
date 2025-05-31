import unittest
from utils import extract_markdown_images, extract_markdown_links


class TestMarkdownExtraction(unittest.TestCase):

    def test_extract_images_various_scenarios(self):
        text_single_image = "This is text with an ![image alt text](image.png)"
        expected_single_image = [("image alt text", "image.png")]
        self.assertEqual(
            extract_markdown_images(text_single_image),
            expected_single_image,
            "Failed single image extraction",
        )

        text_multiple_images = "![alt1](url1.jpg) and ![alt2](url2.gif) ![alt3](path/to/img.bmp)"
        expected_multiple_images = [
            ("alt1", "url1.jpg"),
            ("alt2", "url2.gif"),
            ("alt3", "path/to/img.bmp"),
        ]
        self.assertEqual(
            extract_markdown_images(text_multiple_images),
            expected_multiple_images,
            "Failed multiple image extraction",
        )

        text_no_images = (
            "This text has no images, but it has [a link](link.html)."
        )
        expected_no_images = []
        self.assertEqual(
            extract_markdown_images(text_no_images),
            expected_no_images,
            "Failed no images scenario",
        )

        text_empty_alt = "An image with no alt text ![](/path/to/image.jpeg)"
        expected_empty_alt = [("", "/path/to/image.jpeg")]
        self.assertEqual(
            extract_markdown_images(text_empty_alt),
            expected_empty_alt,
            "Failed image with empty alt text",
        )

        text_empty_url = "![alt text with empty url]()"
        expected_empty_url = [("alt text with empty url", "")]
        self.assertEqual(
            extract_markdown_images(text_empty_url),
            expected_empty_url,
            "Failed image with empty URL",
        )

        text_empty_string = ""
        expected_empty_string = []
        self.assertEqual(
            extract_markdown_images(text_empty_string),
            expected_empty_string,
            "Failed empty string input for images",
        )

        text_link_only = "This is [a link](notanimage.com), not an image."
        self.assertEqual(
            extract_markdown_images(text_link_only),
            [],
            "Failed: Link extracted as image",
        )

    def test_extract_links_various_scenarios(self):
        text_single_link = (
            "This is text with a [link anchor](http://example.com)."
        )
        expected_single_link = [("link anchor", "http://example.com")]
        self.assertEqual(
            extract_markdown_links(text_single_link),
            expected_single_link,
            "Failed single link extraction",
        )

        text_multiple_links = (
            "[link1](url1.html) and [link2](url2.php) also [another link](another.site)."
        )
        expected_multiple_links = [
            ("link1", "url1.html"),
            ("link2", "url2.php"),
            ("another link", "another.site"),
        ]
        self.assertEqual(
            extract_markdown_links(text_multiple_links),
            expected_multiple_links,
            "Failed multiple link extraction",
        )

        text_no_links = (
            "This text has no links, but it has an ![image](image.png)."
        )
        expected_no_links = []
        self.assertEqual(
            extract_markdown_links(text_no_links),
            expected_no_links,
            "Failed no links scenario",
        )

        text_empty_anchor = "A link with no anchor text [](destination.html)"
        expected_empty_anchor = [("", "destination.html")]
        self.assertEqual(
            extract_markdown_links(text_empty_anchor),
            expected_empty_anchor,
            "Failed link with empty anchor text",
        )

        text_empty_url = "[anchor text with empty url]()"
        expected_empty_url = [("anchor text with empty url", "")]
        self.assertEqual(
            extract_markdown_links(text_empty_url),
            expected_empty_url,
            "Failed link with empty URL",
        )

        text_empty_string = ""
        expected_empty_string = []
        self.assertEqual(
            extract_markdown_links(text_empty_string),
            expected_empty_string,
            "Failed empty string input for links",
        )

        text_image_only = "This is ![an image](image.com), not a link."
        self.assertEqual(
            extract_markdown_links(text_image_only),
            [],
            "Failed: Image extracted as link",
        )

    def test_mixed_content_and_differentiation(self):
        text_mixed1 = (
            "Text with ![an image](img.jpg) and then [a link](page.html)."
        )
        expected_images_mixed1 = [("an image", "img.jpg")]
        expected_links_mixed1 = [("a link", "page.html")]
        self.assertEqual(
            extract_markdown_images(text_mixed1),
            expected_images_mixed1,
            "Failed image extraction from mixed content (1)",
        )
        self.assertEqual(
            extract_markdown_links(text_mixed1),
            expected_links_mixed1,
            "Failed link extraction from mixed content (1)",
        )

        text_mixed2 = "[link1](l1.html) followed by ![img1](i1.png) then [link2](l2.net) and ![img2](i2.gif)."
        expected_images_mixed2 = [("img1", "i1.png"), ("img2", "i2.gif")]
        expected_links_mixed2 = [
            ("link1", "l1.html"),
            ("link2", "l2.net"),
        ]
        self.assertEqual(
            extract_markdown_images(text_mixed2),
            expected_images_mixed2,
            "Failed image extraction from mixed content (2)",
        )
        self.assertEqual(
            extract_markdown_links(text_mixed2),
            expected_links_mixed2,
            "Failed link extraction from mixed content (2)",
        )

        text_malformed_image = "Malformed: ![alt text(url)"
        self.assertEqual(
            extract_markdown_images(text_malformed_image),
            [],
            "Failed malformed image non-extraction",
        )
        text_malformed_link = "Malformed: [link text](url"
        self.assertEqual(
            extract_markdown_links(text_malformed_link),
            [],
            "Failed malformed link non-extraction",
        )

        text_double_exclamation = "Look: !![this is an image](double.png)"
        expected_image_double_exc = [("this is an image", "double.png")]
        self.assertEqual(
            extract_markdown_images(text_double_exclamation),
            expected_image_double_exc,
            "Failed double exclamation image",
        )
        self.assertEqual(
            extract_markdown_links(text_double_exclamation),
            [],
            "Failed double exclamation link (should be none)",
        )

        text_link_with_exclamation = "A link like [!important link](important.html)"
        expected_link_with_exc = [
            ("!important link", "important.html")
        ]
        self.assertEqual(
            extract_markdown_links(text_link_with_exclamation),
            expected_link_with_exc,
            "Failed link with exclamation in anchor",
        )
        self.assertEqual(
            extract_markdown_images(text_link_with_exclamation),
            [],
            "Failed link with exclamation in anchor (should not be image)",
        )


if __name__ == "__main__":
    unittest.main(argv=["first-arg-is-ignored"], exit=False)