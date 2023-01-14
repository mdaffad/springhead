from statefun import Context, Message

from springhead.models import Process


def custom_process_logger(context: Context, message: Message, process: Process) -> None:
    incoming_message = message.as_type(process.source_type_value)
    print(incoming_message)
    request = incoming_message
    process.send(target_id=process.target_id, value=request, context=context)
