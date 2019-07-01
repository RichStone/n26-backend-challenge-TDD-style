"""This module was written in a TDD style as described
in 'Test-Driven-Development by Example' by Kent Beck.

The test classes are to be found inside the module because this code was
part of a challenge on hackerrank.com where multiple files are disallowed.

Task:
    1. Read a log file with HTTP responses
    2. Perform some filtering
    3. Create a new file with the filter results

Conditions:
    - duplicate lines are disallowed
    - a single log file might contain up to 2 * 10^5 lines which
      will add up to roughly 25 MB [ 200.000 * 120 / (1024 * 1024) ]
"""

import unittest
import os


class ResponseFilter:
    """Performs filtering operations on a specific log file according to set parameters."""

    def __init__(self, filename, extension_filter, response_code_filter):
        """Inits Response filter with configurable filename and filter parameters."""
        self._filename = filename
        self._extension_filter = extension_filter
        self._code_filter = response_code_filter

        self._filtered_elements_filename_start = 'gifs_'
        self.filtered_elements_filename = '{0}{1}'.format(self._filtered_elements_filename_start, self._filename)

    @staticmethod
    def _get_last_path_element_from_log(line):
        request_param = line.split('"')[1]
        file_path = request_param.split(' ')[1]
        path_elements = file_path.split('/')
        return path_elements[len(path_elements) - 1]

    def _last_path_element_passes_extension_filter(self, last_path_element):
        if last_path_element.lower().endswith(self._extension_filter):
            return True

    @staticmethod
    def _get_response_code_from_log(line):
        response_elements = line.split(' ')
        return response_elements[len(response_elements) - 2]

    def _response_code_passes_filter(self, response_code):
        return response_code == self._code_filter

    def create_new_file_with_filtered_elements(self):
        """Creates a new file with the filtered elements

        Reads a response log file and creates a new file with elements.

        Filter parameters are set at object initiation.
        """

        with open(self._filename, 'r') as input_file:
            with open(self.filtered_elements_filename, 'w') as output_file:
                for line in input_file:
                    last_path_element = ResponseFilter._get_last_path_element_from_log(line)
                    if self._last_path_element_passes_extension_filter(last_path_element):
                        response_code = ResponseFilter._get_response_code_from_log(line)
                        if self._response_code_passes_filter(response_code):
                            output_file.write(last_path_element + '\n')


class TextFileFilter:
    """Takes a text file and performs filtering operations on it."""

    @staticmethod
    def remove_duplicates(filename):
        """Removes duplicate lines in a single text file.

        Creates a set of lines and overwrites the same file with the lines
        in the set.

        Is not optimized for files without a newline at the end of the file.
        """
        with open(filename, 'r') as file:
            filtered_lines = set(file.readlines())

        with open(filename, 'w') as file:
            for line in filtered_lines:
                file.write(line)


class TestResponseFilter(unittest.TestCase):

    FILENAME = 'sample_test_input_file.txt'

    def setUp(self):
        with open(self.FILENAME, 'w') as file:
            file.write(
                """unicomp6.unicomp.net - - [01/Jul/1995:00:00:06 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985
                burger.letters.com - - [01/Jul/1995:00:00:11 -0400] "GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 0
                burger.letters.com - - [01/Jul/1995:00:00:12 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 304 0
                burger.letters.com - - [01/Jul/1995:00:00:12 -0400] "GET /shuttle/countdown/video/livevideo.GIF HTTP/1.0" 200 0
                burger.letters.com - - [01/Jul/1995:00:00:12 -0400] "GET /shuttle/countdown/video/livevideo.GIF HTTP/1.0" 200 0
                d104.aa.net - - [01/Jul/1995:00:00:13 -0400] "GET /shuttle/countdown/ HTTP/1.0" 200 3985
                unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 200 40310
                unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 200 786
                unicomp6.unicomp.net - - [01/Jul/1995:00:00:14 -0400] "GET /images/KSC-logosmall.gif HTTP/1.0" 200 1204
                d104.aa.net - - [01/Jul/1995:00:00:15 -0400] "GET /shuttle/countdown/count.gif HTTP/1.0" 200 40310
                d104.aa.net - - [01/Jul/1995:00:00:15 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 200 786
                d104.aa.net - - [01/Jul/1995:00:00:15 -0400] "GET /images/NASA-logosmall.gif HTTP/1.0" 200 786
                d104.aa.net - - [01/Jul/1995:00:00:15 -0400] "GET /images/smogo.gif HTTP/1.0" 200 0"""
                )
        self.res_filter = ResponseFilter(filename=self.FILENAME, extension_filter='.gif', response_code_filter='200')

    def tearDown(self):
        os.remove(self.FILENAME)

    def test_filename_has_txt_extension(self):
        self.assertTrue(self.res_filter._filename.endswith('.txt'))

    def test_get_last_path_element_from_log(self):
        response_log_line = 'burger.letters.com - - [01/Jul/1995:00:00:11 -0400] "GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 0'
        filename = ResponseFilter._get_last_path_element_from_log(response_log_line)
        self.assertEqual('liftoff.html', filename)

    def test_get_response_code(self):
        response_log_line = 'burger.letters.com - - [01/Jul/1995:00:00:11 -0400] "GET /shuttle/countdown/liftoff.html HTTP/1.0" 304 0'
        response_code = ResponseFilter._get_response_code_from_log(response_log_line)
        self.assertEqual('304', response_code)

    def test_response_code_passes_filter(self):
        response_code = '200'
        self.assertTrue(self.res_filter._response_code_passes_filter(response_code))

    def test_response_code_not_passing_filter(self):
        response_code = '304'
        self.assertFalse(self.res_filter._response_code_passes_filter(response_code))

    def test_last_path_element_matches_filter(self):
        last_path_element = 'funny_picture.gif'
        self.assertTrue(self.res_filter._last_path_element_passes_extension_filter(last_path_element))

    def test_last_path_element_with_upper_case_extension_matches_filter(self):
        last_path_element = 'funny_picture.GIF'
        self.assertTrue(self.res_filter._last_path_element_passes_extension_filter(last_path_element))

    def test_last_path_element_not_matching_filter(self):
        last_path_element = '/funny/directory/'
        self.assertFalse(self.res_filter._last_path_element_passes_extension_filter(last_path_element))

    def test_created_file_starts_with_gifs(self):
        self.assertEqual('gifs_', self.res_filter._filtered_elements_filename_start)
        self.assertEqual('gifs_{}'.format(self.res_filter._filename), self.res_filter.filtered_elements_filename)

    def test_7_filenames_written_from_sample(self):
        self.res_filter.create_new_file_with_filtered_elements()
        filtered_elements = self.res_filter.filtered_elements_filename
        with open(filtered_elements, 'r') as file:
            lines_amount = sum(1 for line in file)

        self.assertEqual(9, lines_amount)


class TestTextFileFilter(unittest.TestCase):

    def test_file_filter_removes_duplicates(self):
        test_file = 'test_file.txt'
        with open(test_file, 'w') as file:
            file.write(
"""livevideo.GIF
livevideo.GIF
count.gif
NASA-logosmall.gif
KSC-logosmall.gif
count.gif
count.GIF
NASA-logosmall.gif
NASA-logosmall.gif
sahara.gif
"""
            )

        TextFileFilter.remove_duplicates(test_file)

        with open(test_file, 'r') as file:
            final_text = list(file.read())
            expected_result = list(
"""livevideo.GIF
KSC-logosmall.gif
count.gif
count.GIF
NASA-logosmall.gif
sahara.gif
"""
            )
            final_text.sort()
            expected_result.sort()
            self.assertEqual(expected_result, final_text)

            os.remove(test_file)


if __name__ == '__main__':
    filename = input()
    unittest.main()

    rf = ResponseFilter(filename, extension_filter='.gif', response_code_filter='200')
    rf.create_new_file_with_filtered_elements()

    TextFileFilter.remove_duplicates(rf.filtered_elements_filename)
