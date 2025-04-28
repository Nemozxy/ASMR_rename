from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# 配置浏览器选项（以Chrome为例）
options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # 无头模式，不显示浏览器界面
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')

# 初始化WebDriver
driver = webdriver.Chrome(options=options)

# 新增配置：禁止加载图片
prefs = {
    "profile.managed_default_content_settings.images": 2,  # 2表示阻止加载
    "profile.default_content_setting_values.images": 2
}
options.add_experimental_option("prefs", prefs)

# 关键词列表
KEYWORDS = ["多语种", "中文", "字幕"]


def check_url(url):
    try:
        driver.get(url)
        # 显式等待，确保元素加载完成
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.q-pt-sm.q-pb-none"))
        )
        text = element.text
        # 检查是否包含任意关键词
        for keyword in KEYWORDS:
            if keyword in text:
                return True, keyword
        return False, None
    except TimeoutException:
        return None, "页面加载超时"
    except NoSuchElementException:
        return None, "未找到指定元素"
    except Exception as e:
        return None, f"发生错误: {str(e)}"


def main(url_file):
    with open(url_file, 'r') as f:
        urls = f.read().splitlines()

    results = []
    for url in urls:
        if not url.strip():
            continue
        print(f"正在检查: {url}")
        result, detail = check_url(url)
        if result is True:
            print(f"√ 包含关键词: {detail}")
            results.append((url, "包含", detail))
        elif result is False:
            print("× 未包含关键词")
            results.append((url, "未包含", ""))
        else:
            print(f"× 检查失败: {detail}")
            results.append((url, "失败", detail))
        time.sleep(1)  # 避免频繁请求

    # 保存结果到文件
    with open("check_results.csv", "w", encoding="gbk") as f:
        f.write("URL,状态,详情\n")
        for row in results:
            f.write(",".join(row) + "\n")
    print("\n检查完成，结果已保存到 check_results.csv")


if __name__ == "__main__":
    # 替换为你的URL列表文件路径
    main("urls.txt")
    driver.quit()