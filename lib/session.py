from .thread_analyzer import ThreadAnalyzer


class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__new__(cls)
        return cls._instances[cls]


class Session(Singleton):
    def __init__(self):
        if not hasattr(self, "initialized"):
            self.data = {}
            self.thread_ids = []
            self.initialized = True

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

    def add_thread_id(self, thread_id):
        if thread_id not in self.thread_ids:
            self.thread_ids.append(thread_id)

    def get_thread_ids(self):
        return self.thread_ids

    def clear(self):
        self.data.clear()
        self.thread_ids.clear()

    def cost(self):
        total_cost = 0.0
        for thread_id in self.thread_ids:
            analyzer = ThreadAnalyzer(thread_id)
            analyzer.analyze_thread()
            analysis = analyzer.analysis_results.get(thread_id)
            if analysis:
                total_cost += analysis["total_thread_cost"]
        return total_cost

    def tokens(self):
        total_tokens = 0
        for thread_id in self.thread_ids:
            analyzer = ThreadAnalyzer(thread_id)
            analyzer.analyze_thread()
            analysis = analyzer.analysis_results.get(thread_id)
            if analysis:
                total_tokens += analysis["total_token_usage"]
        return total_tokens

    def store_message(self, thread_id, message):
        thread_key = f"thread_{thread_id}"
        thread_object = self.get(thread_key, {"messages": []})
        thread_object["messages"].append(message)
        self.set(thread_key, thread_object)

    def get_last_message(self, thread_id, default=None):
        thread_key = f"thread_{thread_id}"
        thread_object = self.get(thread_key, {"messages": []})
        return thread_object["messages"][-1] if thread_object["messages"] else default
