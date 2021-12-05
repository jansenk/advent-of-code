class InputReader:

    @staticmethod
    def file_reader(filename):
        return InputReader(open('advent/input_files/' + filename, 'r'))

    @staticmethod
    def string_reader(string):
        return InputReader(string.splitlines())

    def __init__(self, lines_iter):
        self.lines_iter = lines_iter
    
    def lines(self):
        for line in self.lines_iter:
            l = line.strip()
            if not l:
                continue
            yield l
    
    def comma_separated(self):
        for line in self.lines():
            yield line.split(',')

    def comma_separated_ints(self):
        for split_line in self.comma_separated():
            yield [int(i) for i in split_line]

    def ints(self):
        for line in self.lines():
            yield int(line)

    def lines_discard_header(self):
        for line in self.lines():
            if line.startswith('//'):
                continue
            yield line

    def close(self):
        try:
            self.lines_iter.close()
        except AttributeError:
            pass
