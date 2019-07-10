from base import BaseScrapper


class SybScrapper(BaseScrapper):
    url = 'https://www.sezerbozkir.com/'
    # follow = True
    # next_selector = '.nav-previous a'
    as_json = True
    save_as_file = True
    filename = 'sezerbozkir.json'

    def scrap(self, soup):
        for post in soup.select('.type-post'):
            yield {
                'url': post.select_one('.entry-title a').attrs.get('href'),
                'title': post.select_one('.entry-title a').get_text(strip=True),
                'htmlContent': post.select_one('.entry-content').__str__(),
                'date': post.select_one('.entry-meta .date-meta a').get_text(strip=True),
            }
            break


if __name__ == '__main__':
    SybScrapper()
