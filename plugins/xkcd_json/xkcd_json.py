# -*- coding: utf-8 -*-


from __future__ import unicode_literals, print_function

from pelican import signals
from pelican.generators import Generator
from pelican.writers import Writer

import os
import logging
import json

logger = logging.getLogger(__name__)

class XkcdJsonGenerator(Generator):

    def __init__(self, *args, **kwargs):
        super(XkcdJsonGenerator, self).__init__(*args, **kwargs)

        self.path_article = self.settings.get('ARTICLE_JSON_SAVE_AS')
        self.path_index = self.settings.get('ARTICLE_JSON_INDEX_SAVE_AS')
        self.json_category = self.settings.get('ARTICLE_JSON_CATEGORY_SLUG')
        self.path_last = self.settings.get('ARTICLE_JSON_LAST_SAVE_AS')

    def generate_output(self, writer):
        category_articles = []
        articles = self.context['articles']
        index_template = self.get_template('xkcd_json_index')
        index_path = os.path.join(self.output_path, self.path_index)
        last_path = os.path.join(self.output_path, self.path_last)

        article_template = self.get_template('xkcd_json')
        for article in articles:
            if article.category.slug == self.json_category:
                article_path = os.path.join(self.output_path, self.path_article.format(slug=article.slug) )
                writer.write_file(article_path, article_template, self.context, article=article)
                category_articles.append(article)

        writer.write_file(last_path, article_template, self.context, article=category_articles[0])
        writer.write_file(index_path, index_template, self.context, article=category_articles)




def get_generators(generators):
    return XkcdJsonGenerator


def register():
    signals.get_generators.connect(get_generators)