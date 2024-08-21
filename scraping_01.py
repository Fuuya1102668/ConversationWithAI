import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pdfkit
import os
import time

def save_page_as_pdf(url, save_path):
    """
    指定されたURLのページをPDFとして保存する。

    :param url: 保存するページのURL
    :param save_path: PDFファイルの保存先パス
    :return: なし
    """
    try:
        pdfkit.from_url(url, save_path)
        print(f"Saved PDF: {save_path}")
    except Exception as e:
        print(f"Failed to save PDF for {url}: {e}")

def scrape_and_save_pdf(url, visited, save_dir):
    """
    URLをスクレイピングし、そのページをPDFとして保存。リンク先のページも再帰的に処理。

    :param url: スクレイピングするURL
    :param visited: 訪問済みのURLを保持するセット
    :param save_dir: PDFファイルを保存するディレクトリ
    :return: なし
    """
    # URLが訪問済みであればスキップ
    if url in visited:
        return

    try:
        # URLを訪問済みに追加
        visited.add(url)

        # PDFとして保存
        page_name = url.replace('https://', '').replace('http://', '').replace('/', '_') + '.pdf'
        save_path = os.path.join(save_dir, page_name)
        save_page_as_pdf(url, save_path)

        # HTMLを取得
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        # ページ内のすべてのリンクを取得
        links = soup.find_all('a')
        full_links = [urljoin(url, link.get('href')) for link in links if link.get('href')]

        # 各リンク先を再帰的にスクレイピング
        for link in full_links:
            scrape_and_save_pdf(link, visited, save_dir)

        # リクエストの間隔を適度に開ける
        time.sleep(1)

    except requests.exceptions.RequestException as e:
        print(f"Failed to retrieve {url}: {e}")

if __name__ == "__main__":
    # メインサイトのURL
    #main_url = 'https://www.kanazawa-it.ac.jp/index.html'
    main_url = 'http://darkside.info.kanazawa-it.ac.jp/doku.php?id=star'

    # 訪問済みURLを追跡するためのセット
    visited_urls = set()

    # PDFファイルの保存先ディレクトリ
    save_directory = '/home/fuya/AI/ConversationWithAI/rag_source/'

    # ディレクトリが存在しない場合は作成
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # メインサイトのスクレイピングを開始
    scrape_and_save_pdf(main_url, visited_urls, save_directory)

