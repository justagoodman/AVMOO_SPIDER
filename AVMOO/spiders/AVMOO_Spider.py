import scrapy
from ..items import AV_Item, Star_Item, Genre_Item
import psycopg2
import logging


class AVMOO_Spider(scrapy.Spider):
    name = "avmoo"

    connection = psycopg2.connect(
        database="Scrapy",
        user="postgres",
        password="964719978",
        host="127.0.0.1",
        port="5432")
    cursor = connection.cursor()

    start_urls = [
        "https://avmask.com/cn",
        # "https://avmask.com/cn/released",
        # "https://avmask.com/cn/popular",
        # "https://avmask.com/cn/actresses",
        "https://avmask.com/cn/genre",
    ]

    def parse(self, response):
        if response.url == "https://avmask.com/cn/actresses":
            yield scrapy.Request(response.url, self.parse_stars)
        elif response.url == "https://avmask.com/cn/genre":
            yield scrapy.Request(response.url, self.parse_genres)
        else:
            yield scrapy.Request(response.url, self.parse_avs)

    '''
    生成女星item   
    @param response {response}
    @param selector {'div.star-box' selector}
    '''
    @classmethod
    def generate_star_item(cls, response, selector):
        star_item = Star_Item()
        star_item['origin_url'] = response.url
        star_item['cover_url'] = cls.extract_css_single(selector, 'img::attr(src)')
        star_item['name'] = cls.extract_css_single(selector, 'div.photo-info > span::text')
        info_p_tags = selector.css('p')[:-1]

        for p_tag in info_p_tags:
            p_tag_text = cls.extract_css_single(p_tag, 'p::text')
            if p_tag_text.find("生日: ") != -1:
                star_item['birthday'] = p_tag_text.replace("生日: ", "")
            elif p_tag_text.find("年龄: ") != -1:
                star_item['age'] = p_tag_text.replace("年龄: ", "")
            elif p_tag_text.find("身高: ") != -1:
                star_item['height'] = p_tag_text.replace("身高: ", "")
            elif p_tag_text.find("罩杯: ") != -1:
                star_item['cup'] = p_tag_text.replace("罩杯: ", "")
            elif p_tag_text.find("胸围: ") != -1:
                star_item['bust'] = p_tag_text.replace("胸围: ", "")
            elif p_tag_text.find("腰围: ") != -1:
                star_item['waist'] = p_tag_text.replace("腰围: ", "")
            elif p_tag_text.find("臀围: ") != -1:
                star_item['hipline'] = p_tag_text.replace("臀围: ", "")
            elif p_tag_text.find("出生地: ") != -1:
                star_item['birth_place'] = p_tag_text.replace("出生地: ", "")
            elif p_tag_text.find("爱好: ") != -1:
                star_item['hobby'] = p_tag_text.replace("爱好: ", "")

        return star_item

    '''
    解析女星集合页面， 将解析到的每个女星地址传递给parse_avs，进一步生成女星Item，和该女星的所有影片
    '''
    def parse_stars(self, response):
        if not self._is_real_page(response):
            yield scrapy.Request(response.url, self.parse_stars)
        stars = response.css('#waterfall a.avatar-box')
        for star in stars:
            star_url = self.extract_css_single(star, 'a::attr(href)')
            if not self._check_star_exist(star_url):
                yield scrapy.Request(star_url, self.parse_avs)
            else:
                logging.info("+++++++++++ skip one duplicated star record ++++++++++++")

        next_page_url = self._find_next_page_url(response)
        if next_page_url is not None:
            yield response.follow(next_page_url, self.parse_stars)

    '''
    解析类别页面，为每一个分类生成Genre Item
    将每个类别的地址传递给parse_avs，进一步解析类别中的所有影片
    '''
    def parse_genres(self, response):
        if not self._is_real_page(response):
            yield scrapy.Request(response.url, self.parse_genres)
        h4_tags = response.css('div.container-fluid h4')
        # row_genres = response.css('div.container-fluid h4 + div.row')
        for h4_tag in h4_tags:
            group_name = self.extract_css_single(h4_tag, 'h4::text')
            row = h4_tag.css('h4 + div.row')
            for genre in row.css('a'):
                genre_item = Genre_Item()
                genre_item['genre_group'] = group_name
                genre_item['origin_url'] = self.extract_css_single(genre, 'a::attr(href)')
                genre_item['title'] = self.extract_css_single(genre, 'a::text')
                yield genre_item
                yield scrapy.Request(genre_item['origin_url'], self.parse_avs)

    '''
    解析av集合页面， 需要分析是否有女星信息，如果有，生成一个女星Item；
    将解析到的av详情地址传递给parse_detail
    '''
    def parse_avs(self, response):
        if not self._is_real_page(response):
            yield scrapy.Request(response.url, self.parse_avs)
        star = response.css('#waterfall div.avatar-box')
        if len(star) != 0:
            av_details = response.css('#waterfall a.movie-box')
            for av_detail in av_details:
                av_detail_url = av_detail.css('a::attr(href)').get()
                if not self._check_av_exist(av_detail_url):
                    yield scrapy.Request(av_detail_url, self.parse_detail)
                else:
                    logging.info("+++++++++++ skip one duplicated av record ++++++++++++")
            star_item = self.generate_star_item(response, star[0])
            yield star_item

        # av_details = response.css('#waterfall a.movie-box')
        # for av_detail in av_details:
        #     av_detail_url = av_detail.css('a::attr(href)').get()
        #     if not self._check_av_exist(av_detail_url):
        #         yield scrapy.Request(av_detail_url, self.parse_detail)
        #     else:
        #         logging.info("+++++++++++ skip one duplicated av record ++++++++++++")
        #
        # next_page_url = self._find_next_page_url(response)
        # if next_page_url is not None:
        #     yield response.follow(next_page_url, self.parse_avs)

        else:

            av_details = response.css('#waterfall a.movie-box')
            for av_detail in av_details:
                av_detail_url = av_detail.css('a::attr(href)').get()
                if not self._check_av_exist(av_detail_url):
                    yield scrapy.Request(av_detail_url, self.parse_detail)
                else:
                    logging.info("+++++++++++ skip one duplicated av record ++++++++++++")

            next_page_url = self._find_next_page_url(response)
            if next_page_url is not None:
                yield response.follow(next_page_url, self.parse_avs)

    '''
    解析av详情页面，处理parse_av中解析到的所有av
    生成AV Item
    对AV Item 中的genres 、 stars 、 studio 、 label 、 series 的url再次调用parse_avs
    尽可能的覆盖所有av，防止遗漏
    '''
    def parse_detail(self, response):
        def get_p_json_obj(p_selector):
            a_tags = p_selector.css('a')
            if len(a_tags) == 1:
                json = {
                    "name": self.extract_css_single(a_tags[0], 'a::text'),
                    "url": self.extract_css_single(a_tags[0], 'a::attr(href)')
                }
                return json
            elif len(a_tags) > 1:
                json_arr = []
                for a_tag in a_tags:
                    json = {
                        "name": self.extract_css_single(a_tag, 'a::text'),
                        "url": self.extract_css_single(a_tag, 'a::attr(href)')
                    }
                    json_arr.append(json)
                return json_arr
            else:
                return {}
        if not self._is_real_page(response):
            yield scrapy.Request(response.url, self.parse_detail)
        av_item = AV_Item()
        container = response.css('div.container')
        av_item['origin_url'] = response.url
        av_item['cover_url'] = self.extract_css_single(container, 'img::attr(src)')
        av_item['title'] = self.extract_css_single(container, 'h3::text')
        movie_info = container.css('div.row.movie > div.col-md-3.info')
        all_p_tags = movie_info.css('p')
        for p_tag in all_p_tags:
            if len(p_tag.css('p::attr(class)')) == 0:
                p_tag_text = self.extract_css_single(p_tag, 'p span.header::text').replace(" ", "")
                if p_tag_text.find("识别码:") != -1:
                    av_item['AV_CODE'] = self.extract_css_single(p_tag, 'p span:last-child::text')
                elif p_tag_text.find("发行时间:") != -1:
                    av_item['publish_date'] = self.extract_css_single(p_tag, 'p::text').replace(" ", "")
                elif p_tag_text.find("长度:") != -1:
                    av_item['video_length'] = self.extract_css_single(p_tag, 'p::text').replace(" ", "")
                elif p_tag_text.find("导演:") != -1:
                    av_item['director'] = get_p_json_obj(p_tag)
                    # yield scrapy.Request(av_item['director']['url'], self.parse_avs)
            else:
                p_tag_text = self.extract_css_single(p_tag, 'p::text')
                if p_tag_text.find("制作商:") != -1:
                    av_item['studio'] = get_p_json_obj(p_tag.css('p + p'))
                    # yield scrapy.Request(av_item['studio']['url'], self.parse_avs)
                elif p_tag_text.find("发行商:") != -1:
                    av_item['label'] = get_p_json_obj(p_tag.css('p + p'))
                    # yield scrapy.Request(av_item['label']['url'], self.parse_avs)
                elif p_tag_text.find("系列:") != -1:
                    av_item['series'] = get_p_json_obj(p_tag.css('p + p'))
                    # yield scrapy.Request(av_item['series']['url'], self.parse_avs)
                elif p_tag_text.find("类别:") != -1:
                    av_item['genres'] = get_p_json_obj(p_tag.css('p + p'))

        engaged_stars = response.css('#avatar-waterfall')
        if len(engaged_stars) == 1:
            arr = []
            for star in engaged_stars.css('a'):
                obj = {
                    "name": star.css('span::text').get(),
                    "url": star.css('a::attr(href)').get()
                }
                # yield scrapy.Request(obj['url'], self.parse_avs)
                arr.append(obj)
            av_item['stars'] = arr

        sample_images = response.css('#sample-waterfall')
        if len(sample_images) == 1:
            arr = []
            for img in sample_images.css('a'):
                fake_url = self.extract_css_single(img, 'img::attr(src)')
                temp_url_args = fake_url.split("-")
                real_url = temp_url_args[0]+"jp"+"-"+temp_url_args[1]
                arr.append(real_url)
            av_item['sample_imgs'] = arr

        yield av_item

    '''
    提取单个属性
    @param selector {css selector}
    @param pattern  {css selector pattern -> '#map div.box'}
    @return ""              -> if no element found
    @return items[0].get()  -> if found, return the first element 
    '''
    @classmethod
    def extract_css_single(cls, selector, patten):
        items = selector.css(patten)
        if len(items) == 0:
            return ""
        else:
            return items[0].get()

    '''
    找到下一页的链接
    @param response {response}
    @return '/movie/afs54fd'  ->  if has next page 
    @return None              ->  if no next page
    '''
    def _find_next_page_url(self, response):
        page_a_tags = response.css('ul.pagination li a')
        for a_tag in page_a_tags:
            if self.extract_css_single(a_tag, 'a::attr(name)') == "nextpage":
                next_page_url = self.extract_css_single(a_tag, 'a::attr(href)')
                return next_page_url

        return None

    '''
    数据库中查询是否存在av对应的origin_url
    @param url  {str}  ->  av url  eg:  "https://avmask.com/cn/movie/0d1bc15588833349"
    @return True       ->  av exists
    @return False      ->  av not exists 
    '''
    def _check_av_exist(self, url):
        origin_url = str(url)
        sql = '''
        SELECT origin_url FROM public."AVMOO_AV" where origin_url = '{}';
        '''.format(
            origin_url
        )
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        return len(results) != 0

    '''
    数据库中查询是否存在star对应的origin_url
    @param url  {str}  ->  av url  eg:  "https://avmask.com/cn/movie/0d1bc15588833349"
    @return True       ->  av exists
    @return False      ->  av not exists 
    '''
    def _check_star_exist(self, url):
        origin_url = str(url)
        sql = '''
        SELECT origin_url FROM public."AVMOO_STAR" where origin_url = '{}';
        '''.format(
            origin_url
        )
        self.cursor.execute(sql)
        results = self.cursor.fetchall()

        return len(results) != 0

    def _is_real_page(self, response):
        logo = response.css('.logo')
        return len(logo) != 0


