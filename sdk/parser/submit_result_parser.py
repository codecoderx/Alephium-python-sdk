from sdk import util


class SubmitResultParser:
    def __init__(self, msg_buffer):
        self.fromGroup_size = 4
        self.toGroup_size = 4
        self.result_size = 1

        self.start_offset = 0
        self.end_offset = 0

        self.buffer = msg_buffer

    def parse(self):
        result = {}
        self.end_offset = self.start_offset + self.fromGroup_size
        result["fromGroup"] = util.parse_be_uint32(self.buffer[self.start_offset, self.end_offset])

        self.start_offset += self.fromGroup_size
        self.end_offset = self.start_offset + self.toGroup_size
        result["toGroup"] = util.parse_be_uint32(self.buffer[self.start_offset, self.end_offset])

        self.start_offset += self.toGroup_size
        self.end_offset = self.start_offset + self.result_size

        result["result"] = util.parse_be_uint8(self.buffer[self.start_offset, self.end_offset])

        return result
