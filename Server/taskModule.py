import uuid


class TaskModule:
    def __init__(self, plugin_name, cmd_string):
        self.plugin_name = plugin_name
        self.cmd_string = cmd_string
        self.uuid = str(uuid.uuid1())
        self.applicant_id = ""
        self.start_time = ""
        self.end_time = ""
        self.result = ""
