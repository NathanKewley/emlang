class TestBase:
    def get_file_contents(self, test_file):
        file = open(test_file, mode='r')
        source = file.read()
        file.close()
        return source