import os
import time
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
# 在获取 work_name 后添加文件名清洗逻辑
import re

def rename_folders(target_dir, headless=False, no_images=True):
    # 配置浏览器选项
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    if no_images:
        options.add_argument("--blink-settings=imagesEnabled=false")

    # 初始化浏览器
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        for folder_name in os.listdir(target_dir):
            folder_path = os.path.join(target_dir, folder_name)
            if not os.path.isdir(folder_path):
                continue

            product_id = folder_name
            url = f"https://www.dlsite.com/maniax/work/=/product_id/{product_id}.html"

            try:
                driver.get(url)

                # 新增弹窗处理逻辑
                try:
                    # 处理语言选择弹窗
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '简体中文')]"))
                    ).click()

                    # 处理年龄验证弹窗
                    WebDriverWait(driver, 3).until(
                        EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), '是，我已满18岁')]"))
                    ).click()

                    time.sleep(1)  # 确保弹窗关闭
                except:
                    pass  # 没有弹窗时继续执行

                # 处理可能的跳转
                current_url = driver.current_url
                if 'translation=' in current_url:
                    driver.get(current_url)

                # 等待元素加载
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "work_name"))
                )

                # 获取作品名称
                work_name = driver.find_element(By.ID, "work_name").text.strip()
                sanitized_name = sanitize_filename(work_name)
                new_name = f"{product_id} {sanitized_name}"
                new_path = os.path.join(target_dir, new_name)

                os.rename(folder_path, new_path)
                print(f"Renamed: {folder_name} -> {new_name}")

            except Exception as e:
                print(f"Error processing {product_id}: {str(e)}")
            time.sleep(1)  # 礼貌等待

    finally:
        driver.quit()

def sanitize_filename(name):
    # 移除特殊字符（保留中文、日文、字母、数字、空格和常用符号）
    name = re.sub(r'[\\/*?:"<>|]', '_', name)
    # 合并连续空格
    return re.sub(r'\s+', ' ', name).strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir", help="目标目录路径")
    parser.add_argument("--headless", action="store_true",
                       help="启用无头模式（默认关闭）")
    parser.add_argument("--no-images", action="store_false",
                       dest="no_images", help="禁用无图模式（默认开启）")

    args = parser.parse_args()

    rename_folders(
        target_dir=args.target_dir,
        headless=args.headless,
        no_images=args.no_images
    )
