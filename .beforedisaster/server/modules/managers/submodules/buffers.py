import modules.instancer as instancer

log = instancer.log


class Buffer:
    def __init__(self, name):
        self.buffer = []
        self.name = name

    def reset_buffer(self):
        self.buffer.clear()
        log.info(f"Cleared the buffer: {self.name}")

    def add(self, object, pos=None):
        try:
            if pos is None:
                self.buffer.append(object)

            else:
                self.buffer.insert(pos, object)
        except Exception as e:
            log.error(f"An error occured while adding an element to {self.name}:", str(e.with_traceback))

    def remove(self, pos):
        try:
            self.buffer.pop(pos)

        except Exception as e:
            log.error(f"An error occured while removing the element from {self.name}:", str(e.with_traceback))
