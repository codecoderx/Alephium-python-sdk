from sdk.parser import util
from sdk.parser.job_parser import JobParser

JOB_MESSAGE_TYPE = 0
SUBMIT_RESULT_MESSAGE_TYPE = 1


def parse_message(msg_buffer):
    type_buffer = msg_buffer[0:1]
    msg_type = util.parse_be_uint8(type_buffer)
    if msg_type == JOB_MESSAGE_TYPE:
        return {"type": msg_type, "payload": parse_jobs(msg_buffer[1:])}
    elif msg_type == SUBMIT_RESULT_MESSAGE_TYPE:
        pass
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
