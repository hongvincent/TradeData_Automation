# %% [markdown]
# # [관세청 수출입무역통계 사이트](https://tradedata.go.kr/cts/index.do) 크롤러 개발
# - webdriver 버전

# %%
# latest selenium version (October 9, 2023)
# !pip install selenium=="4.14.0"
# !python.exe -m pip install --upgrade pip

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import time

# 반응형 웹 오류 대비해 옵션 설정
options = Options()
options.add_argument("--start-maximized")   # 전체화면으로 실행
options.add_argument("--disable-infobars")  # 정보바 숨김
# disable the banner "Chrome is being controlled by automated test software"
# edgedriver는 해당 실행파일과 같은 경로에 위치해야 함
edge_driver_path = "./msedgedriver.exe"
# 기본 edge 브라우저 경로 설정
options.binary_location = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
driver = webdriver.Edge(options = options)
driver.get('https://tradedata.go.kr/cts/index.do')
hs_codes = [
    "8479501000",
    "8479502000",
    "8479509000",
    "8515211010",
    "8515212010",
    "8515213010",
    "8515219010",
    "8515311010",
    "8515319010",
    "8486309020",
    "8424202010",
    "8479892010", 
	"8479892090", 
	"8428701000", 
	"8427103000", 
	"8428702000", 
	"8428709000", 
	"8508111000", 
	"8508192000"
]

def click_export_import_statistics(driver):
    """
    Clicks on the '수출입통계' -> '수출입통계 실적' dropdown menu in the top navigation bar.

    Args:
        driver: The Selenium WebDriver instance to use.

    Returns:
        None.
    """
    # Click on the '수출입통계' dropdown menu
    dropdown_menu = driver.find_element(by="xpath", value='//*[@id="topMenuArea"]/li[1]')
    dropdown_menu.click()

    # Wait for the dropdown menu to expand
    time.sleep(1)

    # Click on the '수출입통계 실적' link
    link = driver.find_element(by="xpath", value='//*[@id="topMenuArea"]/li[1]/ul/li[2]/a')
    link.click()

    # Wait for the page to load
    time.sleep(1)

def change_statistics_type(driver):
    """
    Changes the statistics type to '품목별+국가별' in the left navigation bar.

    Args:
        driver: The Selenium WebDriver instance to use.

    Returns:
        None.
    """
    # Click on the '품목별+국가별' radio button
    radio_button = driver.find_element(by="xpath", value='//*[@id="titleType"]')
    radio_button.click()

    # Wait for the radio button to be selected
    time.sleep(1)

    # Click on the '조회' button
    button = driver.find_element(by="xpath", value='//*[@id="radioListType"]/li[2]')
    button.click()

    # Wait for the page to load
    time.sleep(1)

def enter_hs_codes(driver, hs_codes):
    """
    Enters the given HS codes into the search input field.

    Args:
        driver: The Selenium WebDriver instance to use.
        hs_codes: A list of HS codes to enter.

    Returns:
        None.
    """
    # Find the search input field and click on it
    search_input = driver.find_element(by="xpath", value='//*[@id="ETS0100019Q_hsSgn"]')
    search_input.click()

    # Wait for the input field to be ready
    time.sleep(0.5)

    # Enter each HS code and press Enter
    for hs_code in hs_codes:
        search_input.send_keys(hs_code)
        time.sleep(0.1)
        search_input.send_keys(Keys.ENTER)
        time.sleep(0.1)

def monthly_search(driver):
    """
    Clicks on the '월별 조회' radio button and selects the most recent month.

    Args:
        driver: The Selenium WebDriver instance to use.

    Returns:
        None.
    """
    # Click on the '월별 조회' radio button
    radio_button = driver.find_element(by="xpath", value='//*[@id="filterCon"]/div[11]/div[1]/div[2]/ul/li[2]')
    radio_button.click()

    # Wait for the radio button to be selected
    time.sleep(0.1)

    # Select the most recent month
    month_option = driver.find_element(by="xpath", value='//*[@id="ETS0100019Q_formYearMonthPc"]/option[1]')
    month_option.click()

    # Wait for the page to load
    time.sleep(1)

    # Click on the '조회' button
    search_button = driver.find_element(by="xpath", value='//*[@id="filterCon"]/div[14]/button[2]')
    search_button.click()

    # Wait for the page to load
    time.sleep(1)

def yearly_search(driver):
    """
    Changes the search type to yearly and clicks the search button.

    Args:
        driver: The Selenium WebDriver instance to use.

    Returns:
        None.
    """
    # Click on the '연도별' radio button
    radio_button = driver.find_element(by="xpath", value='//*[@id="filterCon"]/div[11]/div[1]/div[2]/ul/li[1]')
    radio_button.click()

    # Wait for the radio button to be selected
    time.sleep(1)

    # Click on the '조회' button
    search_button = driver.find_element(by="xpath", value='//*[@id="filterCon"]/div[14]/button[2]')
    search_button.click()

    # Wait for the page to load
    time.sleep(1)

def download_trade_data(driver):
    """
    Downloads the monthly export/import trade data in Excel format.

    Args:
        driver: The Selenium WebDriver instance to use.

    Returns:
        None.
    """
    # Click on the '엑셀 다운로드' button
    download_button = driver.find_element(by="xpath", value='//*[@id="mainarea"]/div/div[1]/div[2]/div[2]/div/div/button')
    download_button.click()

    # Wait for the download button to be ready
    time.sleep(1)

    # Click on the data download button
    download_button = driver.find_element(by="xpath", value='//*[@id="ETS0100019Q_btnXls"]')
    download_button.click()

    # Wait for the download to complete
    time.sleep(10)



driver.execute_script("let a = alert('⌛5초 뒤 웹을 자동으로 조작합니다.\\n 원활한 작업을 위해 마우스/키보드 조작을 금해주세요🚫');document.body.setAttribute('data-id', a)")
try:
    # 5초 간 기다리는데, alert이 뜨면 바로 다음으로 넘어감
    WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
    print("✅Alerted")
    alert = driver.switch_to.alert
    time.sleep(5)  # must 

    # 취소 버튼 클릭 시 의도적으로 오류 발생해 다음 절차(finally) 진행
    raise Exception(alert.accept())
    
except TimeoutException:
    print("⚠️오류가 발생해 프로그램을 종료합니다.")
    driver.quit()

except Exception as e:
    print(type(e))


finally:
    click_export_import_statistics(driver)
    change_statistics_type(driver)
    enter_hs_codes(driver, hs_codes)

    # Scroll down to the bottom of the page
    driver.execute_script("window.scrollTo(0, window.scrollY + 1000)")
    time.sleep(0.5)

# %%
def download_visualization_data(driver):
    """
    Downloads the visualization data for export/import statistics in bar chart format.

    Args:
        driver: The Selenium WebDriver instance to use.

    Returns:
        None.
    """
    # Click on the '막대' chart button
    bar_chart = driver.find_element(by="xpath", value='//*[@id="ETS0100019Q_btnChartColumn"]')
    bar_chart.click()

    # # Wait for the chart to load
    # time.sleep(1)
    # driver.switch_to.window(driver.window_handles[0])
    # blank_area.click()

    # Click on the context menu button
    context_menu = driver.find_element(by="xpath", value='/html/body/div[3]/section/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/div[2]/div[3]/button')
    print(context_menu)
    context_menu.click()

    # Wait for the context menu to appear
    time.sleep(0.5)

    # Click on the '이미지 다운로드' button
    download_button = driver.find_element(by="xpath", value='/html/body/div[3]/section/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/div[3]/ul/li[3]')
    download_button.click()

    # Wait for the download to complete
    time.sleep(5)

driver.execute_script("let a = confirm('⌛5초 뒤 월별 데이터 수집을 진행합니다.\\n[취소] 버튼 클릭시 연도별 데이터를 수집합니다.');document.body.setAttribute('data-id', a)")
try:
    # 5초 간 기다리는데, alert이 뜨면 바로 다음으로 넘어감
    WebDriverWait(driver, 5).until(EC.alert_is_present(),
                                   'Timed out waiting for PA creation ' +
                                   'confirmation popup to appear.')
    print("✅Alerted")
    alert = driver.switch_to.alert
    time.sleep(5)  # must 

    # 취소 버튼 클릭 시 의도적으로 오류 발생해 다음 절차(finally) 진행
    raise Exception(alert.accept())
    
except TimeoutException:
    print("⚠️오류가 발생해 프로그램을 종료합니다.")
    driver.quit()

except Exception as e:
    print(type(e))

finally:
    promt_text = driver.find_element(By.TAG_NAME, 'body').get_attribute('data-id') # get the text from the alert
    # 다운로드 이벤트 후 발생하는 윈도우로 인해 다음 작업 진행 위한 페이지 빈 공간 지정
    blank_area = driver.find_element(By.XPATH, value='/html/body/div[3]/section/div[1]/div/div[1]/div[1]/div[1]/div[1]')

    print("🖱️사용자로부터 입력받은 버튼: "+promt_text)

    if promt_text == "true":
        print('🌕월별 조회')
        monthly_search(driver)
        download_trade_data(driver)
        # driver.switch_to.window(driver.window_handles[0])
        # download_visualization_data(driver)

    elif promt_text == "false":
        print('🗓️연도별 조회')
        yearly_search(driver)
        download_trade_data(driver)
        # driver.switch_to.window(driver.window_handles[0])
        # blank_area.click()
        # time.sleep(0.5)
        # download_visualization_data(driver)

    else:
        print("⚠️오류가 발생해 프로그램을 종료합니다.")
        driver.quit()

# %%
# # 이미지 다운로드(하기 로직은 다른 프로그램으로 대체)
# context_menu = driver.find_element(by="xpath", value='/html/body/div[3]/section/div[1]/div/div[1]/div[2]/div[2]/div/button[2]')
# print(context_menu)
# context_menu.click()
# # Wait for the context menu to appear
# time.sleep(0.5)

# # Click on the '이미지 다운로드' button
# download_button = driver.find_element(by="xpath", value='/html/body/div[3]/section/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/div[3]/ul/li[3]')
# download_button.click()
#### 웹상 '파이' 그래프는 효용성 떨어져서 제외 ####
# # '파이' 그래프 선택 (금액) 후 이미지 다운로드
# pie_chart = driver.find_element(by="xpath", value='//*[@id="ETS0100019Q_btnChartPie"]')
# pie_chart.click()
# WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CLASS_NAME, "highcharts-menu"))).click()
# time.sleep(1)
# 파이차트 컨텍스트 메뉴 버튼 조작
# chart_context_menu = driver.find_element(by="xpath", value='/html/body/div[3]/section/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/div[2]/div[2]/button')
# chart_context_menu.click()
# time.sleep(0.5)
# chart_img_download = driver.find_element(by="xpath", value='/html/body/div[3]/section/div[1]/div/div[1]/div[2]/div[4]/div[2]/div/div[3]/div[3]/ul/li[3]')
# chart_img_download.click()

time.sleep(2)
driver.quit()


