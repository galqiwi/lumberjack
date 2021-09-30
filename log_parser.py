from dataclasses import dataclass


def read_log(filename):
    with open(filename, 'r') as file:
        return ['[T ' + line for line in file.read().split('[T ')]


@dataclass
class Message:
    source: str
    destination: str
    time: int
    tracker: str

    @staticmethod
    def parse_str(log_line: str) -> "Message":
        out = Message("", "", -1, "")
        time_raw, _, source_raw, _, tracker_and_destination_raw = \
            [entry.strip() for entry in log_line.split(']\t[', 5)]

        # "[T 1598 | 581" -> 1598
        out.time = int(time_raw.split()[1])

        # " Server-kv-1 /T1" -> "Server-kv-1"
        out.source = source_raw.split()[0].strip()

        # "Get-guid-X-7]	 Send packet to Server-kv-1:2..." ->
        # "Get-guid-X-7",	"Send packet to Server-kv-1:2..."
        out.tracker, destination_raw = \
            tracker_and_destination_raw.split(']', 1)

        # "Send packet to Server-kv-1:2..." -> "Server-kv-1"
        out.destination = \
            destination_raw.split(':', 1)[0][len('Send packet to '):].strip()

        return out

    @staticmethod
    def is_str_valid(log_line: str) -> bool:
        return '[Network' in log_line and 'Send packet to' in log_line
