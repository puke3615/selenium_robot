from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from exceptions import *
from opts import *
import time


def _parse_timeout(timeout):
    before = None
    after = None
    if isinstance(timeout, int):
        after = timeout
    elif isinstance(timeout, tuple) or isinstance(timeout, list):
        size = len(timeout)
        if size == 1:
            after = max(timeout[0], 0)
        elif size == 2:
            before = max(timeout[0], 0)
            after = max(timeout[1], 0)
    return before, after


class Action:

    def __init__(self, timeout):
        self.before, self.after = _parse_timeout(timeout)

    def __call__(self, browser, **kwargs):
        self.browser = browser

        if self.before:
            time.sleep(self.before)
        self.call(browser, **kwargs)
        if self.after:
            time.sleep(self.after)

    def call(self, browser, **kwargs):
        pass


class LambdaAction(Action):

    def __init__(self, func, timeout=None):
        Action.__init__(self, timeout)
        self.func = func

    def call(self, browser, **kwargs):
        self.func(browser, **kwargs)


class Open(Action):

    def __init__(self, url, timeout=2):
        Action.__init__(self, timeout)
        self.url = url

    def call(self, browser, **kwargs):
        browser.get(self.url)


class FindText(Action):

    def __init__(self, text, timeout=None, choose_func=None, find_func=None):
        Action.__init__(self, timeout)
        self.text = text
        if choose_func and not callable(choose_func):
            raise Exception('The argument %s is not callable' % choose_func)
        self.choose_func = choose_func
        if find_func and not callable(find_func):
            raise Exception('The argument %s is not callable' % find_func)
        self.find_func = find_func

    def call(self, browser, **kwargs):
        if self.find_func:
            elements = self.find_func(lambda: self.perform_find(browser, **kwargs), browser, **kwargs)
        else:
            elements = self.perform_find(browser, **kwargs)
        element = self.choose_element(elements)
        if element:
            self.handle_element(element)
        else:
            raise Exception("Can't find element with %s" % self.text)

    def perform_find(self, browser, **kwargs):
        elements = find_elements_by_text(browser, self.text, **kwargs)
        elements = elements or find_elements_by_text(browser, self.text, fuzzy=True, **kwargs)
        return elements

    def choose_element(self, elements):
        if not elements:
            return None
        if isinstance(elements, WebElement):
            return elements
        if self.choose_func:
            element = self.choose_func(elements)
            if element:
                return element
            else:
                raise Exception('The choose function is too strict, no element is choose.')
        elif len(elements) > 1:
            elements_text = ','.join(['"%s"' % element.text.encode('utf-8') for element in elements])
            raise Exception(
                'Too many elements (%s) found with text contains "%s".' % (elements_text, self.text))
        else:
            return elements[0]

    def handle_element(self, element):
        pass


class Click(FindText):

    def __init__(self, text, timeout=1, choose_func=None, find_func=None):
        FindText.__init__(self, text, timeout, choose_func, find_func)

    def handle_element(self, element):
        element.click()


class Input(FindText):

    def __init__(self, text, content, timeout=1, choose_func=None, find_func=None):
        FindText.__init__(self, text, timeout, choose_func, find_func)
        self.content = content

    def handle_element(self, element):
        set_element_text(element, self.content)


class SwitchWindowByHandle(Action):

    def __init__(self, window_handle, timeout=1):
        Action.__init__(self, timeout)
        self.window_handle = window_handle

    def call(self, browser, **kwargs):
        browser.switch_to.widnow(self.window_handle)


class SwitchWindowByIndex(Action):

    def __init__(self, index, timeout=1):
        Action.__init__(self, timeout)
        if index < 0:
            raise Exception("The index shouldn't be negative.")
        self.index = index

    def call(self, browser, **kwargs):
        handles = browser.window_handles
        if self.index >= len(handles):
            raise Exception('The index is %d, but only exists %d window handles in current browser.'
                            % (self.index, len(handles)))
        browser.switch_to.window(handles[self.index])
