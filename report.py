from typing import List
import lumberjack
from PIL import Image, ImageDraw, ImageFont
from utils import create_palette

W, H = (1920, 1080)
dH = 50
event_r = 5
line_w = 3


class Report:
    def __init__(self, messages: List[lumberjack.Message]):
        timestamps = {message.time for message in messages}
        timestamps_id = {timestamp: timestamp_id for timestamp_id, timestamp in
                         enumerate(sorted(timestamps))}

        hostnames = {message.source for message in messages} | \
                    {message.destination for message in messages}
        hostnames_id = {hostname: hostname_id for hostname_id, hostname in
                        enumerate(sorted(hostnames))}

        trackers = {message.tracker for message in messages}
        trackers_color = {tracker: color for tracker, color in
                          zip(trackers, create_palette(len(trackers)))}

        out = Image.new("RGBA", (W, H), (255, 255, 255, 255))
        d = ImageDraw.Draw(out)

        def get_line_y(hostname):
            y_id = hostnames_id[hostname]
            return H / 2 - dH * (y_id - (len(hostnames) - 1) / 2)

        def get_timestamp_x(timestamp, shift=False):
            x_id = timestamps_id[timestamp]
            return W * (0.1 + 0.8 * (x_id + shift / 2) / (
                        len(timestamps) - 1 + 0.5))

        for hostname in hostnames:
            d.rectangle([(get_timestamp_x(min(timestamps)),
                          get_line_y(hostname) - line_w / 2), (
                         get_timestamp_x(max(timestamps), True),
                         get_line_y(hostname) + line_w / 2)], fill=(0, 0, 0))
            fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 25)
            text_w, text_h = (d.textsize(hostname, fnt))
            d.text((get_timestamp_x(min(timestamps), False) - text_w,
                    get_line_y(hostname) - text_h / 2), hostname,
                   fill=(0, 0, 0), font=fnt)

        for message in messages:
            d.line([(get_timestamp_x(message.time, False),
                     get_line_y(message.source)),
                    (get_timestamp_x(message.time, True),
                     get_line_y(message.destination))],
                   fill=trackers_color[message.tracker], width=5)

        self.out = out

    def save(self, filename):
        self.out.save(filename)
