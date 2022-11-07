from river.cluster import CluStream
from statefun import Context, Message

from springhead.models import Process


def clustream(context: Context, message: Message, process: Process) -> None:
    clustream = context.storage.clustream or None
    if not clustream:
        clustream = clustream = CluStream(
            n_macro_clusters=3, max_micro_clusters=5, time_gap=3, seed=0, halflife=0.4
        )
    pass
