from lambdatest_sdk_utils import is_smartui_enabled,fetch_dom_serializer,post_snapshot
from lambdatest_sdk_utils import get_pkg_name,setup_logger,get_logger


def smartui_snapshot(driver, name,**kwargs):
    # setting up logger
    setup_logger()
    logger = get_logger()
    
    try:
        if not name:
            raise Exception('The `snapshotName` argument is required.')
        if is_smartui_enabled() is False: 
            raise Exception("SmartUI server is not running.")
        
        resp = fetch_dom_serializer()
        driver.execute_script(resp['data']['dom'])

        # Serialize and capture the DOM
        dom = driver.execute_script("return {'dom':SmartUIDOM.serialize()}")

        # Post the dom to smartui endpoint
        post_snapshot(dom,name,get_pkg_name())

        logger.info(f'Snapshot captured {name}')
    except Exception as e:
        logger.error(f'Could not take snapshot "{name}" Error {e}')