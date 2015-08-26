# -*- coding: utf-8 -*-


from __future__ import unicode_literals, print_function

from pelican import signals
from pelican.generators import Generator
from pelican.writers import Writer

import os
import logging
import json
import requests

logger = logging.getLogger(__name__)

class XkcdJsonGenerator(Generator):

    def __init__(self, *args, **kwargs):
        super(XkcdJsonGenerator, self).__init__(*args, **kwargs)

        self.path_article = self.settings.get('ARTICLE_JSON_SAVE_AS')
        self.path_index = self.settings.get('ARTICLE_JSON_INDEX_SAVE_AS')
        self.json_category = self.settings.get('ARTICLE_JSON_CATEGORY_SLUG')
        self.path_last = self.settings.get('ARTICLE_JSON_LAST_SAVE_AS')

    def generate_output(self, writer):
        articles = self.context['articles']
        index_template = self.get_template('xkcd_json_index')
        index_path = os.path.join(self.output_path, self.path_index)
        last_path = os.path.join(self.output_path, self.path_last)

        article_template = self.get_template('xkcd_json')
        for article in articles:
            if article.category.slug == self.json_category:
                article_path = os.path.join(self.output_path, self.path_article.format(slug=article.slug) )
                writer.write_file(article_path, article_template, self.context, article=article)

        category_articles = [article for article in articles if article.category.slug == self.json_category]

        writer.write_file(last_path, article_template, self.context, article=category_articles[0])
        writer.write_file(index_path, index_template, self.context, article=category_articles)

class SpecialPagesGenerator(Generator):

    def __init__(self, *args, **kwargs):
        super(SpecialPagesGenerator, self).__init__(*args, **kwargs)

        self.path_nums = self.settings.get('NUMS_SAVE_AS')
        self.path_imgs = self.settings.get('IMGS_SAVE_AS')
        self.category = self.settings.get('ARTICLE_JSON_CATEGORY_SLUG')
        self.MAX_NUM = int(requests.get("http://xkcd.com/info.0.json").json()["num"])
        logging.info("latest xkcd is {}".format(self.MAX_NUM))


    def generate_output(self, writer):
        all_articles = self.context['articles']
        nums_template = self.get_template('xkcd_nums')
        imgs_template = self.get_template('xkcd_imgs')

        articles = [article for article in all_articles if article.category.slug == self.category]

        nums_path = os.path.join(self.output_path, self.path_nums)
        imgs_path = os.path.join(self.output_path, self.path_imgs)

        articles.sort(key=(lambda x: int(x.sourcenum)), reverse=(True))

        nums = []
        snum = {}
        
        for article in articles:
            snum[int(article.sourcenum)] = article
        
        nums = [(num, snum.get(num, False)) for num in xrange(1, self.MAX_NUM + 1) if num != 404]


        writer.write_file(nums_path, nums_template, self.context, nums=nums)
        writer.write_file(imgs_path, imgs_template, self.context, articles=articles)

class XkcdRandomGenerator(Generator):

    def __init__(self, *args, **kwargs):
        super(XkcdRandomGenerator, self).__init__(*args, **kwargs)

        self.category = self.settings.get('ARTICLE_JSON_CATEGORY_SLUG')
        self.path_random = self.settings.get('RANDOM_SAVE_AS')


    def generate_output(self, writer):
        all_articles = self.context['articles']
        random_template = self.get_template('xkcd_random')

        articles = [article for article in all_articles if article.category.slug == self.category]

        random_path = os.path.join(self.output_path, self.path_random)

        articles.sort(key=(lambda x: int(x.sourcenum)), reverse=(True))

        writer.write_file(random_path, random_template, self.context, articles=articles)

def get_generators(generators):
    return XkcdJsonGenerator

def get_special(generators):
    return SpecialPagesGenerator

def get_random(generators):
    return XkcdRandomGenerator


def register():
    signals.get_generators.connect(get_generators)
    signals.get_generators.connect(get_special)
    signals.get_generators.connect(get_random)

