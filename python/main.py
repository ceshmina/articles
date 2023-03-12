import glob
from google.cloud import firestore
import sys
from typing import NamedTuple


class Article(NamedTuple):
    year: int
    month: int
    title: str
    content: str


def read_article(path: str) -> Article:
    paths = path.split('/')
    assert len(paths) == 5

    year = int(paths[2])
    month = int(paths[3])
    title = paths[4]
    with open(path, 'r') as f:
        content = f.read()
    
    return Article(year=year, month=month, title=title, content=content)


def upload(article: Article) -> None:
    fs_client = firestore.Client()
    # TODO


def main() -> None:
    print()
    cnt = 0
    for path in glob.glob('../articles/**/*.md', recursive=True):
        try:
            article = read_article(path)
        except:
            sys.stderr.write(f'ファイルパスが不正なため、以下ファイルのアップロードをスキップします: {path}\n')
            continue
        
        upload(article)
        cnt += 1
    
    print(f'{cnt}件のファイルをアップロードしました')


if __name__ == '__main__':
    main()
