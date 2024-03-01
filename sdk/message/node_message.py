from sdk import util
from sdk.parser.job_parser import JobParser
from sdk.parser.submit_result_parser import SubmitResultParser

JOB_MESSAGE_TYPE = 0
SUBMIT_RESULT_MESSAGE_TYPE = 1
SUBMIT_BLOCK_MESSAGE_TYPE = 0


def parse_node_message(msg_buffer):
    type_buffer = msg_buffer[0:1]
    msg_type = util.parse_be_uint8(type_buffer)
    if msg_type == JOB_MESSAGE_TYPE:
        return {"type": msg_type, "payload": parse_jobs(msg_buffer[1:])}
    elif msg_type == SUBMIT_RESULT_MESSAGE_TYPE:
        return {"type": msg_type, "payload": parse_submit_result(msg_buffer[1:])}
    else:
        raise Exception("Invalid message type")


def parse_jobs(jobs_buffer):
    job_len = util.parse_be_uint32(jobs_buffer[0:4])
    jobs = []
    start_offset = 4
    for i in range(job_len):
        job_parser = JobParser(jobs_buffer[start_offset:])
        job = job_parser.parse()
        start_offset += job["dataLength"]
        jobs.append(job)
    return jobs


def parse_submit_result(submit_result_buffer):
    submit_result_parser = SubmitResultParser(submit_result_buffer)
    return submit_result_parser.parse()


def build_submit_message(nonce_buffer, headerBlob_buffer, txsBlob_buffer):
    block = nonce_buffer + headerBlob_buffer + txsBlob_buffer
    block_size = len(block)
    message_size = 4 + 1 + block_size
    msg_header = b''
    msg_header += util.to_be_uint32(message_size)
    msg_header += util.to_be_uint8(SUBMIT_BLOCK_MESSAGE_TYPE)
    msg_header += util.to_be_uint32(block_size)

    return msg_header + block
