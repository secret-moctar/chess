class StateManager:
    def __init__(self):
        self._menus = {}
        self.current_state = None

    def register(self, state_id, state_class):
        self._menus[state_id] = state_class

    def get_state(self, state_id):
        if state_id not in self._menus:
            raise KeyError(f"State {state_id} is not registered")

        return self._menus[state_id]

    def change_state(self, state_id):
        if self.current_state:
            self.current_state.exit()
        self.current_state = self.get_state(state_id)()


state_manager = StateManager()
