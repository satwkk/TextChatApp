from dataclasses import dataclass

@dataclass
class Message:
    author: bytes
    content: bytes
    attachment: bytes