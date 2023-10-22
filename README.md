# TradeData_Scraping_Automation

## README.md

### TradeData_Automation-main

이 레포지토리는 웹 크롤링을 통해 거래 데이터를 자동화하여 수집하고, 해당 데이터를 바탕으로 차트를 생성하는 코드를 포함하고 있습니다.

### 주요 파일 및 내용:

1. **cts_web_crawler.ipynb**:
   - 웹 크롤링을 위한 Selenium 드라이버 초기화 및 설정.
   - 특정 웹사이트로 이동하여 거래 데이터 크롤링.
   - 웹 페이지 내의 알림 및 선택지에 따른 데이터 다운로드 로직 포함.
   - 월별 및 연도별 조회 선택 기능.

2. **tradedata_crawler.ipynb**:
   - 크롤링한 데이터를 기반으로 다양한 차트 생성 GUI 애플리케이션.
   - CSV 파일 업로드 및 파이 차트, 막대 차트 등의 생성 기능.
   - 생성된 차트를 PNG 형식으로 저장하는 기능.

3. **msedgedriver.exe**:
   - Selenium 웹 크롤링을 위한 웹 드라이버.

4. **scrapped_tradedata.csv**:
   - 크롤링된 거래 데이터가 저장된 CSV 파일.

5. **외교부_국가표준코드_20230324.csv**:
   - 외교부에서 제공하는 국가 표준 코드가 포함된 CSV 파일.

### 사용 방법:

1. 필요한 Python 라이브러리 및 모듈을 설치합니다.
2. 웹 크롤링을 수행하기 위해 `cts_web_crawler.ipynb` 노트북을 실행합니다.
3. 크롤링된 데이터를 바탕으로 차트를 생성하려면 `tradedata_crawler.ipynb` 노트북을 실행합니다.
