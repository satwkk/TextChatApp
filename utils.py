from message import Message

def check_exit(message: Message) -> bool:
    ''' Checks if the message sent by user is an exit message '''
    return message.content.decode('utf-8').lower() == 'exit'
