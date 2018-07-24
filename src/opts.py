# coding=utf-8


def protected_func(find_func, *args, **kwargs):
    try:
        return find_func(*args, **kwargs)
    except Exception as e:
        return None


def get_element_text(element, unicode2str=True):
    value = protected_func(element.get_attribute, 'value')
    return value.encode('utf-8') if value and unicode2str else value


def set_element_text(element, text):
    protected_func(element.clear())
    text = text.decode('utf-8')
    return protected_func(element.send_keys, text)


def click_element_by_text(*args, **kwargs):
    element = find_element_by_text(*args, **kwargs)
    if element:
        element.click()
    return element is not None


def input_element_by_text(content, *args, **kwargs):
    element = find_element_by_text(*args, **kwargs)
    if element:
        set_element_text(element, content)
    return element is not None


def find_element_by_text(subject, text, fuzzy=False, by_text=True, by_value=True, by_placeholder=True,
                         by_name=True, by_link_text=True):
    """
    根据文本信息查找元素
    :param subject: 查找主题\n
    :param text:  目标文本\n
    :param fuzzy:  是否支持模糊查询\n
    :param by_text:  是否通过text()查询\n
    :param by_value:  是否通过@value查询\n
    :param by_placeholder:  是否通过@placeholder查询\n
    :param by_name:  是否通过@name\n
    :param by_link_text:  是否通过link_text查询\n
    :return: 目标元素
    """
    element = None
    if by_text:
        xpath = '//*[contains(text(), "%s")]' if fuzzy else '//*[text()="%s"]'
        element = protected_func(subject.find_element_by_xpath, xpath % text)
    if not element and by_value:
        xpath = '//*[contains(@value, "%s")]' if fuzzy else '//*[@value="%s"]'
        element = protected_func(subject.find_element_by_xpath, xpath % text)
    if not element and by_placeholder:
        xpath = '//*[contains(@placeholder, "%s")]' if fuzzy else '//*[@placeholder="%s"]'
        element = protected_func(subject.find_element_by_xpath, xpath % text)
    if not element and by_name:
        xpath = '//*[contains(@name, "%s")]' if fuzzy else '//*[@name="%s"]'
        element = protected_func(subject.find_element_by_xpath, xpath % text)
    if not element and by_link_text:
        element = protected_func(subject.find_element_by_link_text, text)
    return element


def find_elements_by_text(subject, text, fuzzy=False, by_text=True, by_value=True, by_placeholder=True,
                          by_name=True, by_link_text=True):
    """
    根据文本信息查找元素列表
    :param subject: 查找主题\n
    :param text:  目标文本\n
    :param fuzzy:  是否支持模糊查询\n
    :param by_text:  是否通过text()查询\n
    :param by_value:  是否通过@value查询\n
    :param by_link_text:  是否通过link_text查询\n
    :return: 目标元素
    """
    elements = None
    if by_text:
        xpath = '//*[contains(text(), "%s")]' if fuzzy else '//*[text()="%s"]'
        elements = protected_func(subject.find_elements_by_xpath, xpath % text)
    if not elements and by_value:
        xpath = '//*[contains(@value, "%s")]' if fuzzy else '//*[@value="%s"]'
        elements = protected_func(subject.find_elements_by_xpath, xpath % text)
    if not elements and by_placeholder:
        xpath = '//*[contains(@placeholder, "%s")]' if fuzzy else '//*[@placeholder="%s"]'
        elements = protected_func(subject.find_elements_by_xpath, xpath % text)
    if not elements and by_name:
        xpath = '//*[contains(@name, "%s")]' if fuzzy else '//*[@name="%s"]'
        elements = protected_func(subject.find_elements_by_xpath, xpath % text)
    if not elements and by_link_text:
        elements = protected_func(subject.find_elements_by_link_text, text)
    return elements
