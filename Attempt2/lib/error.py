class Error():
    # Print out the error
    def throw(self, line, where, message):
        print(f"[Line {line}] ERROR {where}: {message}")
