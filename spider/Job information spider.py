from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver
import time
import pandas as pd
import json

# 从配置文件加载特定公司的配置
def load_config(filepath, company_name):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            config = json.load(file)
            return config.get(company_name)
    except FileNotFoundError:
        print(f"配置文件 {filepath} 未找到。")
        return None
    except json.JSONDecodeError:
        print(f"配置文件 {filepath} 格式错误。")
        return None

# 稳定等待页面元素加载
def get_stable_element(driver, by, value):
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((by, value)))

# 创建职位数据字典
def create_job_data(job, selectors, company):
    job_title = job.find_element(By.XPATH, selectors['job_title']).text.strip()
    job_location = job.find_element(By.XPATH, selectors['job_location']).text.strip()
    job_type = job.find_element(By.XPATH, selectors['job_type']).text.strip()
    job_department = job.find_element(By.XPATH, selectors['job_department']).text.strip()
    job_content = job.find_element(By.XPATH, selectors['job_content']).text.strip()

    return {
        'job_company': company,
        'job_title': job_title,
        'job_location': job_location,
        'job_type': job_type,
        'job_department': job_department,
        'job_content': job_content
    }

# 检测重复数据
def is_job_duplicate(job_data, jobs_data):
    return any(
        job['job_title'] == job_data['job_title'] and
        job['job_location'] == job_data['job_location'] and
        job['job_type'] == job_data['job_type']
        for job in jobs_data
    )

# 检测是否能翻页
def should_stop_paging(driver, next_button_selector):
    next_page_buttons = driver.find_elements(By.XPATH, next_button_selector)
    if not next_page_buttons or 'disabled' in next_page_buttons[0].get_attribute('class'):
        print("Reached the last page, or the next page button is not clickable.")
        return True
    return False

# 爬取对应公司的职位数据
def get_jobs_data(driver, selectors, max_pages, company):
    count = 1
    jobs_data = []
    while True:
        job_elements = driver.find_elements(By.XPATH, selectors['job_selector'])
        for job in job_elements:
            job_data = create_job_data(job, selectors, company)

            if not is_job_duplicate(job_data, jobs_data):
                jobs_data.append(job_data)
                print(f"Added new job: {job_data['job_title']} in {job_data['job_location']}")
            else:
                print(f"Duplicate job found: {job_data['job_title']} in {job_data['job_location']}, skipping...")

        if count >= max_pages or should_stop_paging(driver, selectors['next_button']):
            break

        try:
            next_page_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, selectors['next_button']))
            )
            next_page_button.click()
            count += 1
            time.sleep(5)
        except TimeoutException:
            if should_stop_paging(driver, selectors['next_button']):
                break
            print("Timeout waiting for the next page button, checking page status.")

    return jobs_data


# 主程序
if __name__ == "__main__":
    companies = ['快手']
    max_pages = 13
    total_start_time = time.time()  # 总开始时间

    for company in companies:
        company_start_time = time.time()  # 每个公司开始时间
        config = load_config('config.json', company)
        jobs_data = []  # 初始化职位数据列表
        if config:
            url = config['url']
            selectors = config['selectors']
            driver = webdriver.Chrome()
            driver.get(url)
            time.sleep(2)

            if 'external_button' in config['selectors'] and config['selectors']['external_button']:
                try:
                    external_page_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, config['selectors']['external_button']))
                    )
                    driver.execute_script("arguments[0].click();", external_page_button)
                    print('已触发额外页面按钮')
                except TimeoutException:
                    print("额外页面按钮不可点击或不存在。")

            time.sleep(3)
            jobs_data = get_jobs_data(driver, selectors, max_pages, company)

            # 计算并打印每个公司爬虫的时间
            company_end_time = time.time()
            print(f"{company} 爬虫完成，用时 {company_end_time - company_start_time:.2f} 秒")

            # 保存每个公司的职位数据到单独的文件
            if jobs_data:
                file_name = f"{company}职位信息.xlsx"
                df = pd.DataFrame(jobs_data)
                df.to_excel(file_name, index=False)
                print(f"导出的数据保存到 {file_name}，总计 {len(jobs_data)} 条")
        else:
            print(f"No configuration found for {company}")

        if driver:
            driver.quit()

    # 计算并打印总时间
    total_end_time = time.time()
    print(f"所有爬虫任务完成，总用时 {total_end_time - total_start_time:.2f} 秒")
