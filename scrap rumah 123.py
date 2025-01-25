import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import random
import time

header = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
}

# Define paths
path = r'C:\Users\MAbdi\OneDrive\Dokumen\project tp'
path_output = r'C:\Users\MAbdi\OneDrive\Dokumen\project tp'
os.makedirs(path, exist_ok=True)
os.makedirs(path_output, exist_ok=True)

# Set Chrome options to ignore SSL errors
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors=yes")
chrome_options.add_argument("--log-level=3")  # Menyembunyikan log yang tidak perlu
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36")

# Initialize Selenium driver with the options
service = Service(executable_path="C:\Program Files\chromedriver-win64\chromedriver.exe", service_log_path=os.devnull)
driver = webdriver.Chrome(service=service, options=chrome_options)

def wait_random(min_sec=1, max_sec=20):
    """Fungsi untuk menunggu dengan jeda acak agar menyerupai perilaku manusia"""
    time.sleep(random.uniform(min_sec, max_sec))

def get_property_details(url):
    driver.get(url)

    # Interaksi tambahan untuk menghindari deteksi bot oleh Cloudflare
    wait_random(5, 10)  # Tunggu agar halaman termuat

    # Scroll bertahap ke bawah untuk meniru perilaku manusia
    for i in range(3):
        scroll_distance = random.randint(100, 400)  # Jarak scroll acak
        driver.execute_script(f"window.scrollBy(0, {scroll_distance});")
        wait_random(2, 4)

    # Klik pada checkbox verifikasi manusia jika ada
    try:
    # Tunggu hingga checkbox muncul, maksimal waktu tunggu 20 detik
        checkbox = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'cb-c')]//input[@type='checkbox']"))
        )
        wait_random(5, 10)  # Tunggu sebentar setelah checkbox muncul, sebelum klik
        checkbox.click()  # Klik checkbox untuk verifikasi
        print("Checkbox 'Verify you are human' berhasil diklik.")
    except:
        print("Checkbox tidak ditemukan atau tidak bisa diakses.")

    # Klik di area kosong untuk interaksi tambahan
    try:
        body = driver.find_element(By.TAG_NAME, "body")
        body.click()
        print("Klik tambahan di halaman untuk simulasi interaksi.")
    except:
        print("Gagal melakukan klik tambahan di halaman.")

    # Handle reCAPTCHA jika ada
    if "recaptcha" in driver.current_url.lower():
        print("reCAPTCHA encountered. Please complete it manually if possible.")
        WebDriverWait(driver, 120).until(lambda d: "recaptcha" not in d.current_url.lower())

    # Klik tombol "Muat lebih banyak"
    try:
        load_more_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'text-primary text-sm w-full flex justify-center md:justify-start py-2 items-center gap-2 cursor-pointer mt-4') and .//span[text()='Muat lebih banyak']]"))
        )
        load_more_button.click()
        print("Clicked 'Muat lebih banyak'")
    except:
        print("Failed to find or click 'Muat lebih banyak' button")

    # Fungsi untuk mengklik kategori dan menampilkan informasi tambahan
    def expand_section_interior(section_name):
        try:
            section_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'flex items-center justify-between w-full pb-2') and .//div[text()='{section_name}']]"))
            )
            section_button.click()
            print(f"Clicked '{section_name}' section.")
        except Exception as e:
            print(f"Failed to find or click '{section_name}' section.")

    def expand_section_eksterior(section_name):
        try:
            section_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'flex items-center justify-between w-full pb-2') and .//div[text()='{section_name}']]"))
            )
            section_button.click()
            print(f"Clicked '{section_name}' section.")
        except Exception as e:
            print(f"Failed to find or click '{section_name}' section.")

    def expand_section_tentang_properti(section_name):
        try:
            section_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(@class, 'flex items-center justify-between w-full pb-2') and .//div[text()='{section_name}']]"))
            )
            section_button.click()
            print(f"Clicked '{section_name}' section.")
        except Exception as e:
            print(f"Failed to find or click '{section_name}' section.")

    # Klik masing-masing kategori untuk memunculkan rincian informasi
    expand_section_interior("Interior")
    expand_section_eksterior("Exterior")
    expand_section_tentang_properti("Tentang Properti")

    # Parsing informasi tambahan setelah tombol diklik
    page_soup = BeautifulSoup(driver.page_source, 'html.parser')

    details = {}

    # Basic property details that appear on page load
    def extract_basic_info_kt(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Kamar Tidur'
            
    details['Kamar Tidur'] = extract_basic_info_kt("Kamar Tidur")
        
    def extract_basic_info_km(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Kamar Mandi'

    details['Kamar Mandi'] = extract_basic_info_km("Kamar Mandi")

    def extract_basic_info_lt(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'N/A'

    details['Luas Tanah'] = extract_basic_info_lt("Luas Tanah")
        
    def extract_basic_info_lb(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Luas Bangunan'

    details['Luas Bangunan'] = extract_basic_info_lb("Luas Bangunan")

        
    def extract_basic_info_cp(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Carport'
        
    details['Carport'] = extract_basic_info_cp("Carport")

        
    def extract_basic_info_tp(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Tipe Properti'

    details['Tipe Properti'] = extract_basic_info_tp("Tipe Properti")

        
    def extract_basic_info_se(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Sertifikat'

    details['Sertifikat'] = extract_basic_info_se("Sertifikat")


    # Additional details that require clicking the button
    def extract_additional_info_dl(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Daya Listrik'
        
    details['Daya Listrik'] = extract_additional_info_dl("Daya Listrik")

        
    def extract_additional_info_dp(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Dapur'
        
    
    details['Dapur'] = extract_additional_info_dp("Dapur")   
        
    def extract_additional_info_rm(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Ruang Makan'
    
    details['Ruang Makan'] = extract_additional_info_rm("Ruang Makan")

    

    def extract_additional_info_rt(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Ruang Tamu'
    
    details['Ruang Tamu'] = extract_additional_info_rt("Ruang Tamu")

        
    def extract_additional_info_kp(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Perabotan'
        
    details['Kondisi Perabotan'] = extract_additional_info_kp("Kondisi Perabotan")
    
    def extract_additional_info_gr(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Garasi'
        
    details['Garasi'] = extract_additional_info_gr("Garasi")
                
    def extract_additional_info_jl(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Lantai'
        
    details['Jumlah Lantai'] = extract_additional_info_jl("Jumlah Lantai")
        
    def extract_additional_info_td(label):
        try:
            element = page_soup.find("p", string=label).find_next_sibling("p")
            return element.get_text(strip=True)
        except:
            return 'No Tahun'
        
    details['Tahun Dibangun'] = extract_additional_info_td("Tahun Dibangun")


    def extract_additional_info_alamat():
        try:
            # Cari elemen <h1> terlebih dahulu
            element = page_soup.find("h1")
            # Ambil elemen <p> berikutnya setelah <h1>
            address_element = element.find_next_sibling("p")
            return address_element.get_text(strip=True)
        except Exception as e:
            print(f"Gagal mengekstrak alamat: {e}")
            return 'No Alamat'

    # Data Lokasi
    details['Alamat'] = extract_additional_info_alamat()

    def extract_additional_info_harga():
        try:
            harga_span = page_soup.find("span", class_="text-primary font-bold whitespace-pre md:text-2xl md:leading-6 text-lg leading-[16px]")
            harga = harga_span.get_text(strip=True) if harga_span else "N/A"
            return harga
        except Exception as e:
            print(f"Gagal mengekstrak harga: {e}")
            return "No Harga"
        
    details['Alamat'] = extract_additional_info_harga()

    return details

# Define a function to handle scraping for each keyword up to a max count of articles
def scrape_articles(city, category, max_articles):
    all_data = []
    page = 1
    total_articles = 0

    while total_articles < max_articles:
        url = f'https://www.rumah123.com/jual/{city}/{category}/?certificates[]=1&sort=posted-desc&page={page}'
        print(f"Scraping URL: {url}")
        driver.get(url)
        wait_random(2, 5)

        # Scroll dinamis untuk memuat lebih banyak artikel
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            wait_random(3, 5)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # Parsing halaman yang sudah dimuat
        page_soup = BeautifulSoup(driver.page_source, 'html.parser')
        properties = page_soup.find_all('div', class_='ui-organism-intersection__element intersection-card-container')

        # Loop melalui properti yang ditemukan
        for property_card in properties:
            if total_articles >= max_articles:
                break
            link = property_card.find("a", href=True)
            if link:
                property_url = f"https://www.rumah123.com{link['href']}"
                if property_url not in [data.get('URL') for data in all_data]:
                    property_details = get_property_details(property_url)
                    property_details['URL'] = property_url
                    all_data.append(property_details)
                    total_articles += 1
                    print(f"Scraped data for {property_url}")
                else:
                    print(f"Duplicate data detected for {property_url}")

        # Pindah ke halaman berikutnya
        next_page = page_soup.find("a", rel="next")
        if next_page:
            page += 1
        else:
            print("Halaman terakhir tercapai.")
            break

    return all_data

def main():
    while True:
        city = input("Masukkan keyword (misal: 'jakarta', 'bekasi'): ").strip().lower()
        category = input("Masukkan tipe properti (misal: 'rumah', 'apartemen'): ").strip().lower()
        max_articles = int(input("Masukkan jumlah artikel yang ingin diambil: "))

        scraped_data = scrape_articles(city, category, max_articles)

        if scraped_data:
            # Simpan data ke Excel
            df = pd.DataFrame(scraped_data)
            output_path = os.path.join(os.getcwd(), f"scraped_properties_{city}_{category}.xlsx")
            df.to_excel(output_path, index=False)
            print(f"Data saved to {output_path}")
        else:
            print("Tidak ada data yang di-scrape.")

        # Prompt user if they want to continue
        lanjut = input("Ingin mencari data lain? (y/n): ").strip().lower()
        if lanjut != 'y':
            break

    driver.quit()

if __name__ == "__main__":
    main()