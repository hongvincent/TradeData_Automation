# TradeData_Scraping_Automation


# TradeData_Automation

## 소개
이 레포지토리는 거래 데이터의 웹 크롤링과 데이터 시각화를 위한 프로젝트입니다. 웹 크롤링을 통해 데이터를 자동화하여 수집하고, 그 데이터를 기반으로 다양한 차트를 생성할 수 있는 기능을 제공합니다.

## 레포지토리 구성
- `/py/`: 추가적인 파이썬 스크립트나 모듈을 포함하는 폴더입니다.
- `cts_web_crawler.py`: 웹 크롤링을 담당하는 스크립트입니다. Selenium을 사용하여 웹 페이지를 접근하고, 거래 데이터를 크롤링합니다.
- `msedgedriver.exe`: Selenium 웹 크롤링을 위한 Microsoft Edge 웹 드라이버입니다.
- `requirements.txt`: 이 프로젝트에서 필요한 Python 패키지와 버전 정보를 포함하고 있습니다.
- `tradedata_crawler.py`: 크롤링된 데이터를 시각화하는 스크립트입니다. 사용자는 이 스크립트를 통해 다양한 차트를 생성하고 저장할 수 있습니다.

## 사용 방법
1. 필요한 Python 패키지를 설치합니다: `pip install -r requirements.txt`
2. 데이터 크롤링을 수행합니다: `python cts_web_crawler.py`
3. 데이터 시각화를 수행합니다: `python tradedata_crawler.py`

