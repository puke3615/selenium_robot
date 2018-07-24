class Robot:
    def __init__(self, *actions):
        self.actions = actions

    def setup(self, browser):
        for action in self.actions:
            action(browser)
        print('Done.')
