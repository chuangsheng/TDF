import os


class TaskList:
    allTaskList = []

    def init_task_list(self):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            serverPluginName = os.path.splitext(filename)[0]
            serverPlugin = __import__("plugins." + serverPluginName, fromlist=[serverPluginName])
            self.allTaskList.extend(serverPlugin.init_task_list())

    def handle_response(self, taskmodule):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            serverPluginName = os.path.splitext(filename)[0]
            if serverPluginName == taskmodule.plugin_name:
                serverPlugin = __import__("plugins." + serverPluginName, fromlist=[serverPluginName])
                serverPlugin.handle_response(taskmodule)

    def completed_signal(self, plugin_name):
        for filename in os.listdir("plugins"):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            serverPluginName = os.path.splitext(filename)[0]
            if serverPluginName == plugin_name:
                serverPlugin = __import__("plugins." + serverPluginName, fromlist=[serverPluginName])
                serverPlugin.completed_signal(plugin_name)



    def getUnAssignedTaskIndex(self, plugin_name, max_num):
        unAssignedTaskIndexList = []
        for index in range(len(self.allTaskList)):
            taskModule = self.allTaskList[index]
            if self.allTaskList[index].plugin_name == plugin_name and self.allTaskList[index].applicant_id == '':
                unAssignedTaskIndexList.append(index)
                max_num -= 1
                if max_num <= 0:
                    break
        return unAssignedTaskIndexList

    def completedAllTask(self, plugin_name):
        for index in range(len(self.allTaskList)):
            taskModule = self.allTaskList[index]
            if self.allTaskList[index].plugin_name == plugin_name and self.allTaskList[index].end_time == '':
                return False

        return True

    def getUnCompletedTaskIndexByUUID(self, uuid):
        for index in range(len(self.allTaskList)):
            if self.allTaskList[index].uuid == uuid and self.allTaskList[index].end_time == '':
                return index

    def modifyTask(self, index, taskModule):
        self.allTaskList[index] = taskModule
