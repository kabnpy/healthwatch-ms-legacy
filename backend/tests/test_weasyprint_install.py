from weasyprint import HTML
import tempfile
import os

def test_weasyprint_installation():
    """Verify that WeasyPrint is installed and can generate a simple PDF."""
    html_content = "<h1>Test</h1><p>This is a test PDF.</p>"
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
        HTML(string=html_content).write_pdf(tmp.name)
        assert os.path.exists(tmp.name)
        assert os.path.getsize(tmp.name) > 0
        os.unlink(tmp.name)

if __name__ == "__main__":
    test_weasyprint_installation()
    print("WeasyPrint installation verified.")
