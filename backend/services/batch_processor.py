import os
from converters.py_converter import PyConverter
from converters.ipynb_converter import IpynbConverter
from converters.c_converter import CConverter
from converters.html_converter import HtmlConverter
from converters.text_converter import TextConverter


class BatchProcessor:
    def __init__(self, output_folder, temp_folder):
        self.output_folder = output_folder
        self.temp_folder = temp_folder

        self.converters = {
            'py': PyConverter(),
            'ipynb': IpynbConverter(),
            'c': CConverter(),
            'cpp': CConverter(),
            'h': CConverter(),
            'html': HtmlConverter(),
            'htm': HtmlConverter(),
            'txt': TextConverter(),
            'java': TextConverter(),
            'js': TextConverter(),
            'css': TextConverter(),
        }

    def convert_file(self, input_path, output_path):
        ext = input_path.rsplit('.', 1)[-1].lower()
        converter = self.converters.get(ext)

        if converter is None:
            raise ValueError(f"No converter available for file type: .{ext}")

        converter.convert(input_path, output_path)
        return output_path

    def convert_batch(self, file_pairs):
        results = []
        for input_path, output_path in file_pairs:
            try:
                self.convert_file(input_path, output_path)
                results.append({'input': input_path, 'output': output_path, 'status': 'success'})
            except Exception as e:
                results.append({'input': input_path, 'output': None, 'status': 'error', 'error': str(e)})
        return results
