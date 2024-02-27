from sdk.parser import util


class JobParser:
    def __init__(self, msg_buffer):
        self.fromGroup_size = 4
        self.toGroup_size = 4
        self.headerBlobLength_size = 4
        self.txsBlobLength_size = 4
        self.targetLength_size = 4

        self.start_offset = 0
        self.end_offset = 0

        self.buffer = msg_buffer

    def parse(self):
        job = {}

        self.end_offset = self.start_offset + self.fromGroup_size
        job["fromGroup"] = util.parse_be_uint32(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += self.fromGroup_size
        self.end_offset = self.start_offset + self.toGroup_size
        job["toGroup"] = util.parse_be_uint32(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += self.toGroup_size
        self.end_offset = self.start_offset + self.headerBlobLength_size
        job["headerBlobLength"] = util.parse_be_uint32(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += self.headerBlobLength_size
        self.end_offset = self.start_offset + job["headerBlobLength"]
        job["headerBlob"] = util.parse_be_bytes(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += job["headerBlobLength"]
        self.end_offset = self.start_offset + self.txsBlobLength_size
        job["txsBlobLength"] = util.parse_be_uint32(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += self.txsBlobLength_size
        self.end_offset = self.start_offset + job["txsBlobLength"]
        job["txsBlob"] = util.parse_be_bytes(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += job["txsBlobLength"]
        self.end_offset = self.start_offset + self.targetLength_size
        job["targetLength"] = util.parse_be_uint32(self.buffer[self.start_offset: self.end_offset])

        self.start_offset += self.targetLength_size
        self.end_offset = self.start_offset + job["targetLength"]
        job["targetBlob"] = util.parse_be_bytes(self.buffer[self.start_offset: self.end_offset])

        job["dataLength"] = self.end_offset

        return job
