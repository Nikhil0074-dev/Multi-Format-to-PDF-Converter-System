"""
Test suite for Multi-Format PDF Converter.
Run from the project root: python test_all.py
"""
import os
import sys
import json
import traceback

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

PASS = "PASS"
FAIL = "FAIL"
results = []

def run_test(name, fn):
    try:
        fn()
        results.append((PASS, name))
        print(f"  [PASS] {name}")
    except Exception as e:
        results.append((FAIL, name, str(e)))
        print(f"  [FAIL] {name}")
        print(f"         {e}")
        traceback.print_exc()

# ---- Setup temp dirs ----
import tempfile
TMP = tempfile.mkdtemp()
OUT = os.path.join(TMP, 'out')
os.makedirs(OUT, exist_ok=True)


# ---- Sample source files ----
PY_SOURCE = '''\
def greet(name):
    """Return a greeting string."""
    return f"Hello, {name}!"

class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

if __name__ == "__main__":
    calc = Calculator()
    print(greet("World"))
    print(calc.add(2, 3))
    print(calc.multiply(4, 5))
'''

C_SOURCE = '''\
#include <stdio.h>
#include <stdlib.h>

int factorial(int n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

int main() {
    int i;
    for (i = 1; i <= 10; i++) {
        printf("%d! = %d\\n", i, factorial(i));
    }
    return 0;
}
'''

HTML_SOURCE = '''\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Page</title>
</head>
<body>
    <h1>Welcome to the Test Page</h1>
    <h2>About this Project</h2>
    <p>This is a sample HTML file used for testing the converter.</p>
    <h3>Features</h3>
    <ul>
        <li>Batch file conversion</li>
        <li>Drag and drop interface</li>
        <li>Watermark support</li>
    </ul>
    <p>All features are tested automatically.</p>
</body>
</html>
'''

IPYNB_SOURCE = {
    "nbformat": 4,
    "nbformat_minor": 5,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": ["# Test Notebook\n", "\n", "This is a **markdown** cell.\n", "\n", "## Section 1\n", "- Item A\n", "- Item B"]
        },
        {
            "cell_type": "code",
            "execution_count": 1,
            "metadata": {},
            "source": ["x = 42\n", "y = x * 2\n", "print(f'Result: {y}')"],
            "outputs": [
                {
                    "output_type": "stream",
                    "name": "stdout",
                    "text": ["Result: 84\n"]
                }
            ]
        },
        {
            "cell_type": "code",
            "execution_count": 2,
            "metadata": {},
            "source": ["def fibonacci(n):\n", "    a, b = 0, 1\n", "    for _ in range(n):\n", "        print(a, end=' ')\n", "        a, b = b, a + b\n", "\n", "fibonacci(10)"],
            "outputs": [
                {
                    "output_type": "stream",
                    "name": "stdout",
                    "text": ["0 1 1 2 3 5 8 13 21 34 "]
                }
            ]
        }
    ]
}

TXT_SOURCE = '''\
Multi-Format PDF Converter
==========================

This plain text file will be converted to PDF.

Key features:
  - Batch processing
  - Watermark support
  - Multiple formats

The converter handles line numbers automatically.
'''

JS_SOURCE = '''\
// JavaScript sample file
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

const fetchData = async (url) => {
    try {
        const response = await fetch(url);
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Fetch failed:", error);
        return null;
    }
};

module.exports = { debounce, fetchData };
'''


def write_tmp(name, content, mode='w'):
    path = os.path.join(TMP, name)
    with open(path, mode) as f:
        if isinstance(content, dict):
            json.dump(content, f, indent=2)
        else:
            f.write(content)
    return path


# ---- Test: Python converter ----
def test_py_converter():
    from converters.py_converter import PyConverter
    src = write_tmp('sample.py', PY_SOURCE)
    out = os.path.join(OUT, 'sample_py.pdf')
    PyConverter().convert(src, out)
    assert os.path.exists(out), "Output PDF not created"
    assert os.path.getsize(out) > 1000, f"PDF too small: {os.path.getsize(out)} bytes"


# ---- Test: C converter ----
def test_c_converter():
    from converters.c_converter import CConverter
    src = write_tmp('main.c', C_SOURCE)
    out = os.path.join(OUT, 'sample_c.pdf')
    CConverter().convert(src, out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000


# ---- Test: HTML converter ----
def test_html_converter():
    from converters.html_converter import HtmlConverter
    src = write_tmp('page.html', HTML_SOURCE)
    out = os.path.join(OUT, 'sample_html.pdf')
    HtmlConverter().convert(src, out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000


# ---- Test: Jupyter Notebook converter ----
def test_ipynb_converter():
    from converters.ipynb_converter import IpynbConverter
    src = write_tmp('notebook.ipynb', IPYNB_SOURCE)
    out = os.path.join(OUT, 'sample_ipynb.pdf')
    IpynbConverter().convert(src, out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000


# ---- Test: Text/generic converter ----
def test_text_converter():
    from converters.text_converter import TextConverter
    src = write_tmp('readme.txt', TXT_SOURCE)
    out = os.path.join(OUT, 'sample_txt.pdf')
    TextConverter().convert(src, out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000


# ---- Test: JS via text converter ----
def test_js_converter():
    from converters.text_converter import TextConverter
    src = write_tmp('app.js', JS_SOURCE)
    out = os.path.join(OUT, 'sample_js.pdf')
    TextConverter().convert(src, out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000


# ---- Test: Watermark - center ----
def test_watermark_center():
    from converters.py_converter import PyConverter
    from services.watermark import WatermarkService
    src = write_tmp('wm_test.py', PY_SOURCE)
    out = os.path.join(OUT, 'wm_center.pdf')
    PyConverter().convert(src, out)
    size_before = os.path.getsize(out)
    WatermarkService().apply_watermark(out, text='CONFIDENTIAL', position='center', opacity=0.3, font_size=48)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000, "Watermarked file is too small"


# ---- Test: Watermark - top position ----
def test_watermark_top():
    from converters.c_converter import CConverter
    from services.watermark import WatermarkService
    src = write_tmp('wm_top.c', C_SOURCE)
    out = os.path.join(OUT, 'wm_top.pdf')
    CConverter().convert(src, out)
    WatermarkService().apply_watermark(out, text='DRAFT', position='top', opacity=0.5, font_size=36)
    assert os.path.exists(out)


# ---- Test: Watermark - bottom position ----
def test_watermark_bottom():
    from converters.html_converter import HtmlConverter
    from services.watermark import WatermarkService
    src = write_tmp('wm_bottom.html', HTML_SOURCE)
    out = os.path.join(OUT, 'wm_bottom.pdf')
    HtmlConverter().convert(src, out)
    WatermarkService().apply_watermark(out, text='SUBMITTED', position='bottom', opacity=0.25, font_size=32)
    assert os.path.exists(out)


# ---- Test: Batch processor ----
def test_batch_processor():
    from services.batch_processor import BatchProcessor
    bp = BatchProcessor(OUT, TMP)

    pairs = [
        (write_tmp('b_test.py', PY_SOURCE), os.path.join(OUT, 'batch_py.pdf')),
        (write_tmp('b_test.c', C_SOURCE), os.path.join(OUT, 'batch_c.pdf')),
        (write_tmp('b_test.html', HTML_SOURCE), os.path.join(OUT, 'batch_html.pdf')),
    ]
    results_batch = bp.convert_batch(pairs)
    successes = [r for r in results_batch if r['status'] == 'success']
    errors = [r for r in results_batch if r['status'] == 'error']
    assert len(successes) == 3, f"Expected 3 successes, got {len(successes)}. Errors: {errors}"
    for r in successes:
        assert os.path.exists(r['output']), f"Output missing: {r['output']}"


# ---- Test: Batch processor - single file ----
def test_batch_single():
    from services.batch_processor import BatchProcessor
    bp = BatchProcessor(OUT, TMP)
    src = write_tmp('single.ipynb', IPYNB_SOURCE)
    out = os.path.join(OUT, 'single_nb.pdf')
    bp.convert_file(src, out)
    assert os.path.exists(out)
    assert os.path.getsize(out) > 1000


# ---- Test: Unsupported extension ----
def test_unsupported_extension():
    from services.batch_processor import BatchProcessor
    bp = BatchProcessor(OUT, TMP)
    src = write_tmp('file.xyz', 'some content')
    out = os.path.join(OUT, 'file_xyz.pdf')
    try:
        bp.convert_file(src, out)
        raise AssertionError("Should have raised ValueError for unsupported extension")
    except ValueError:
        pass  # Expected


# ---- Test: File handler utility ----
def test_file_handler():
    from utils.file_handler import FileHandler
    fh = FileHandler(TMP)
    fname = 'test_util.py'
    write_tmp(fname, PY_SOURCE)
    info = fh.get_file_info(fname)
    assert info is not None
    assert info['extension'] == 'py'
    assert info['size'] > 0


# ---- Run all tests ----
def main():
    print("\nMulti-Format PDF Converter - Test Suite")
    print("=" * 45)
    print(f"Temp dir: {TMP}\n")

    run_test("Python (.py) to PDF", test_py_converter)
    run_test("C (.c) to PDF", test_c_converter)
    run_test("HTML (.html) to PDF", test_html_converter)
    run_test("Jupyter Notebook (.ipynb) to PDF", test_ipynb_converter)
    run_test("Plain text (.txt) to PDF", test_text_converter)
    run_test("JavaScript (.js) to PDF", test_js_converter)
    run_test("Watermark - center diagonal", test_watermark_center)
    run_test("Watermark - top position", test_watermark_top)
    run_test("Watermark - bottom position", test_watermark_bottom)
    run_test("Batch processor - multiple files", test_batch_processor)
    run_test("Batch processor - single file", test_batch_single)
    run_test("Unsupported extension raises error", test_unsupported_extension)
    run_test("File handler utility", test_file_handler)

    print("\n" + "=" * 45)
    passed = sum(1 for r in results if r[0] == PASS)
    failed = sum(1 for r in results if r[0] == FAIL)
    print(f"Results: {passed} passed, {failed} failed out of {len(results)} tests")

    if failed:
        print("\nFailed tests:")
        for r in results:
            if r[0] == FAIL:
                print(f"  - {r[1]}: {r[2]}")
        sys.exit(1)
    else:
        print("\nAll tests passed. Output PDFs saved to:")
        print(f"  {OUT}")
        sys.exit(0)


if __name__ == '__main__':
    main()
