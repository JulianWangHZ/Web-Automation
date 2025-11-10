from config.config import Config


########## URL Path Settings ##########
config = Config()
BASE_URL = config.BASE_URL
###############################



########## Path Settings ##########
ORDER_PAGE_QUERY = "?language=en"
ADDRESS_AND_DATE_PICKER_FRAGMENT = "#address-and-date-picker"
###############################



########## URL Settings ##########
ADDRESS_AND_DATE_PICKER_URL = f"{BASE_URL}{ORDER_PAGE_QUERY}{ORDER_PAGE_QUERY}{ADDRESS_AND_DATE_PICKER_FRAGMENT}"
###############################