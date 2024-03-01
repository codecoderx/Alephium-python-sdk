import socket
import struct
import queue
import threading
import time

from dataclasses import dataclass
from sdk.message.node_message import parse_node_message, JOB_MESSAGE_TYPE, SUBMIT_RESULT_MESSAGE_TYPE


HOST = "192.168.66.130"
PORT = 3899
BUFFER_SIZE = 1024
HEADER_SIZE = 4

GROUP_SIZE = 4

@dataclass
class MinerJob:
    jobId: int
    timestamp: int
    fromGroup: int
    toGroup: int
    headerBlob: str
    txsBlob: str
    targetBlob: str
    target: int
    chainIndex: int

    @staticmethod
    def from_jobs_message(job_id, jobs_message):
        if len(jobs_message) == 0:
            raise Exception("Job Not Found")

        max_target = 0
        for job_message in jobs_message:
            target = int(job_message["targetBlob"], 16)
            if max_target <= target:
                max_target = target

        jobs = [job_message for job_message in jobs_message if int(job_message["targetBlob"], 16) == max_target]
        job = jobs[0]

        return MinerJob(
            jobId=job_id,
            timestamp=time.time_ns(),
            fromGroup=job["fromGroup"],
            toGroup=job["toGroup"],
            headerBlob=job["headerBlob"],
            txsBlob=job["txsBlob"],
            targetBlob=job["targetBlob"],
            target=max_target,
            chainIndex=job["fromGroup"] * GROUP_SIZE + job["toGroup"]
        )


class Server:
    def __init__(self):
        self.ss = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.message_queue = queue.Queue(100)
        # only save latest job message
        self.job_message_queue = queue.Queue(1)
        self.submit_result_message_queue = queue.Queue(10)
        self.job_counter = 1
        self.cached_miner_job = {}

    def connect(self):
        self.ss.connect((HOST, PORT))

    def receive(self):
        start_offset = 0
        buffer = []
        while True:
            _buffer = self.ss.recv(BUFFER_SIZE)
            _buffer_len = len(_buffer)

            # save buffer to cache buffer
            end_offset = start_offset + _buffer_len
            buffer[start_offset:end_offset] = _buffer
            start_offset += _buffer_len
            if len(buffer) >= HEADER_SIZE:
                # read complete message length
                msg_len = struct.unpack(">I", bytes(buffer[0:HEADER_SIZE]))[0]
                if (len(buffer) - HEADER_SIZE) >= msg_len:
                    msg_buffer = buffer[HEADER_SIZE: HEADER_SIZE + msg_len]
                    # put message buffer to queue concurrency
                    self.message_queue.put_nowait(msg_buffer)
                    # clear cached buffer and cache remaining buffer
                    remain_buffer = buffer[HEADER_SIZE + msg_len:]
                    buffer = []
                    buffer[0: len(remain_buffer)] = remain_buffer

                    # reset start offset
                    start_offset = len(remain_buffer)

    def dispatch(self):
        while True:
            try:
                msg_buffer = self.message_queue.get_nowait()
            except queue.Empty:
                time.sleep(1)
                continue

            data = parse_node_message(msg_buffer)
            if data["type"] == JOB_MESSAGE_TYPE:
                self.job_message_queue.put(data["payload"])
            elif data[type] == SUBMIT_RESULT_MESSAGE_TYPE:
                pass
            else:
                raise Exception("Invalid message type")

    def handle_job_message(self):
        while True:
            try:
                job_message = self.job_message_queue.get_nowait()
            except queue.Empty:
                time.sleep(1)
                continue
            miner_job = MinerJob.from_jobs_message(self.job_counter, job_message)
            print(miner_job)
            self.cached_miner_job[self.job_counter] = miner_job
            self.job_counter += 1

    def start(self):
        self.connect()
        receive_task = threading.Thread(target=self.receive)
        dispatch_task = threading.Thread(target=self.dispatch)
        handle_job_message_task = threading.Thread(target=self.handle_job_message)

        receive_task.start()
        dispatch_task.start()
        handle_job_message_task.start()

        receive_task.join()
        dispatch_task.join()
        handle_job_message_task.join()

    def stop(self):
        self.ss.close()


if __name__ == "__main__":
    server = Server()
    server.start()


