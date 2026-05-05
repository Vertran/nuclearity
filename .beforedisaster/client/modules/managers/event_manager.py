from modules.instancer import manager

import modules.instancer as instancer
assert instancer.log is not None
log = instancer.log

class EventManager:
    @manager
    def __init__(self):
        self._subscribers = {}

    def subscribe(self, event_type, callback):
        if event_type not in self._subscribers:
            self._subscribers[event_type] = set()
        self._subscribers[event_type].add(callback)

        log.info(f'Module subscribed {callback} to {event_type}')

    def unsubscribe(self, event_type, callback):
        if event_type in self._subscribers:
            self._subscribers[event_type].discard(callback)

            log.info(f'Module unsubscribed {callback} from {event_type}')


    def emit(self, event_type, **data):
        try:
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    callback(data)
        except Exception as e:
            log.error('Exception occured: ', str(e.with_traceback))


#===> EVENTS LIST
#
#
#
#
#
#
#
#
#
#