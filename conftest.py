import os
from datetime import datetime
import traceback

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from pytest_bdd import given, when, then

from config.config import Config
from config.devices import BaseDevice, IPhone17ProMax, IPhone17, IPadPro, Pixel9Pro



def pytest_configure(config):
    config.addinivalue_line("markers", "bdd: BDD tests")
    config.addinivalue_line("filterwarnings", "ignore::pytest.PytestUnknownMarkWarning")
    
    env = config.getoption("--env")
    if env:
        os.environ['ENV'] = env


def pytest_addoption(parser):
    config = Config()
    parser.addoption("--headless", action="store_true", default=False,
                    help="Run tests in headless mode")
    parser.addoption("--env", action="store", default=config.ENV,
                    help=f"Environment: {', '.join(['dev', 'staging', 'prod'])}")
    parser.addoption("--browser", action="store", default=config.BROWSER,
                    help=f"Browser: {', '.join(['chrome', 'safari', 'firefox'])}")
    parser.addoption("--device", action="store", default=config.DEVICE_TYPE,
                    help="Device type: desktop, iphone17promax, iphone17, ipadpro, pixel9pro")


def get_device_class(device_type: str) -> BaseDevice:
    devices = {
        "desktop": BaseDevice,
        "iphone17promax": IPhone17ProMax,
        "iphone17": IPhone17,
        "ipadpro": IPadPro,
        "pixel9pro": Pixel9Pro
    }
    device_class = devices.get(device_type.lower())
    if not device_class:
        raise ValueError(f"Unsupported device type: {device_type}")
    return device_class()


@pytest.fixture(scope="session")
def device(request):
    device_type = request.config.getoption("--device")
    return get_device_class(device_type)


def create_browser_options(browser_type: str, headless: bool, device: BaseDevice):
    if browser_type == 'chrome':
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument(f"--window-size={device.width},{device.height}")
        options.add_argument(f"--user-agent={device.user_agent}")
        options.add_argument("--disable-protocol-handler-prompt")
        options.add_argument("--disable-external-protocol-handler")
        return options
    elif browser_type == 'safari':
        return SafariOptions()
    elif browser_type == 'firefox':
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--width={device.width}")
        options.add_argument(f"--height={device.height}")
        options.add_argument(f"--user-agent={device.user_agent}")
        
        firefox_bin = os.getenv('FIREFOX_BIN')
        if firefox_bin:
            options.binary_location = firefox_bin
        return options
    raise ValueError(f"Unsupported browser type: {browser_type}")


@pytest.fixture(scope="function")
def browser(request, device):
    browser_type = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    
    options = create_browser_options(browser_type, headless, device)
    
    if browser_type == 'chrome':
        service = Service()
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_type == 'safari':
        driver = webdriver.Safari(options=options)
    elif browser_type == 'firefox':
        service = FirefoxService()
        driver = webdriver.Firefox(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser type: {browser_type}")
    
    driver.implicitly_wait(0)
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def test_config():
    return Config()


@pytest.fixture(scope="session")
def base_url(test_config):
    return test_config.BASE_URL


def get_test_info(item):
    test_file = os.path.basename(item.module.__file__)
    feature_file = None
    scenario_name = None
    
    if test_file.startswith('test_'):
        feature_name = ''.join(c for c in test_file[5:-8] if not c.isdigit())
        if feature_name:
            feature_file = f"{feature_name}.feature"
    
    if hasattr(item, 'function'):
        scenario_name = item.function.__name__
        if scenario_name.startswith('test_'):
            scenario_name = scenario_name[5:]
    
    return {
        "test_file": test_file,
        "feature_file": feature_file or "unknown",
        "scenario_name": scenario_name or item.name,
        "env": item.config.getoption("--env"),
        "browser": item.config.getoption("--browser"),
        "device": item.config.getoption("--device")
    }


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    
    if report.when == 'call':
        start_time = getattr(report, 'start_time', datetime.now())
        duration = (datetime.now() - start_time).total_seconds()
        
        test_info = get_test_info(item)
        screenshot_path = None
        
        if report.failed and hasattr(item, 'browser'):
            scenario_name = test_info['scenario_name']
            clean_name = ''.join(c if c.isalnum() else '_' for c in scenario_name)
            config = Config()
            screenshot_path = f"{config.SCREENSHOT_PATH}/{clean_name}.png"
            item.browser.save_screenshot(screenshot_path)

        tags = []
        if test_info['test_file'].startswith('test_'):
            test_name = test_info['test_file'][5:-8]
            main_feature = ''.join(c for c in test_name if not c.isdigit())
            if main_feature:
                tags.append(main_feature)

def pytest_bdd_before_step(request, feature, scenario, step, step_func):
    if not hasattr(request.node, 'feature_printed'):
        feature_file = os.path.basename(feature.filename)
        print(f"\n\033[36m{'─' * 70}\033[0m")
        print(f"\033[36mFeature:\033[0m \033[97m{feature_file}\033[0m")
        print(f"\033[36mScenario:\033[0m \033[97m{scenario.name}\033[0m")
        
        if hasattr(scenario, 'tags'):
            tags = [tag for tag in scenario.tags if isinstance(tag, str)]
            if tags:
                print(f"\033[35mTags:\033[0m \033[97m{', '.join(tags)}\033[0m")
        
        print(f"\033[36m{'─' * 70}\033[0m")
        setattr(request.node, 'feature_printed', True)
    
    # GIVEN(Blue) / WHEN(Yellow) / THEN(Green) / AND(Purple)
    color_map = {
        'given': '\033[34m',
        'when': '\033[33m',
        'then': '\033[32m',
        'and': '\033[35m',
    }
    style_type = (step.type or '').lower()
    color = color_map.get(style_type, '\033[37m') 
    print(f"{color}{step.type.upper()}\033[0m \033[97m{step.name}\033[0m")


def pytest_bdd_step_error(request, feature, scenario, step, step_func, exception):
    """When a step fails, display detailed error information"""
    print(f"\n\033[31m{'!' * 70}\033[0m")
    print(f"\033[31m❌ Step execution failed\033[0m")
    print(f"\033[31mStep:\033[0m \033[97m{step.type.upper()} {step.name}\033[0m")
    print(f"\033[31mError type:\033[0m \033[97m{type(exception).__name__}\033[0m")
    print(f"\033[31mError message:\033[0m \033[97m{str(exception)}\033[0m")
    print(f"\033[31m\nFull error:\033[0m")
    traceback.print_exc()

