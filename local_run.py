import argparse

from nfe_reader.ba.crawler import Crawler


def crawl_qrcode_url(url):
    crawler = Crawler()
    return crawler.search_by_qrcode(url).to_primitive()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "-u", help="URL do qrcode")

    args = parser.parse_args()

    print(crawl_qrcode_url(args.url) if args.url else None)
