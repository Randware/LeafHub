def parse_params(part: str) -> dict:
    parameters = {}

    for piece in part.split(" "):
        if "/?" in piece:
            piece = piece.replace("/?", "")
            amp_split = piece.split("&")

            for param_set in amp_split:
                eq_split = param_set.split("=")

                if len(eq_split) == 2:
                    parameters[eq_split[0]] = eq_split[1]

    return parameters


class Request:
    def __init__(self, raw_request: str):
        self.raw = raw_request

        parts = raw_request.split("\r\n\r\n", 1)
        header_part = parts[0]

        self.body = parts[1] if len(parts) > 1 else ""

        header_lines = header_part.split("\r\n")
        request_line = header_lines[0]
        parts_line = request_line.split()

        if len(parts_line) >= 3:
            self.method = parts_line[0].upper()
            full_path = parts_line[1]
        else:
            self.method = ""
            full_path = ""

        if "?" in full_path:
            self.path, qs = full_path.split("?", 1)
            self.params = parse_params("/?" + qs)
        else:
            self.path = full_path
            self.params = {}

        self.headers = {}

        for line in header_lines[1:]:
            if ":" in line:
                key, value = line.split(":", 1)
                self.headers[key.strip()] = value.strip()
