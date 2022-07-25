AUTHOR = 'Matthew R. Carbone'
SITENAME = "Matthew R. Carbone"
SITESUBTITLE = 'Thoughts, archive and personal website'
SITEDESCRIPTION = "Personal website of Matthew R. Carbone"
SITEURL = 'https://x94carbone.github.io'

PATH = 'content'

TIMEZONE = 'US/Eastern'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

# # provided as examples, they make ‘clean’ urls. used by MENU_INTERNAL_PAGES.
# TAGS_URL           = 'tags'
# TAGS_SAVE_AS       = 'tags/index.html'
# AUTHORS_URL        = 'authors'
# AUTHORS_SAVE_AS    = 'authors/index.html'
# CATEGORIES_URL     = 'categories'
# CATEGORIES_SAVE_AS = 'categories/index.html'
# ARCHIVES_URL       = 'archives'
# ARCHIVES_SAVE_AS   = 'archives/index.html'

# # use those if you want pelican standard pages to appear in your menu
# MENU_INTERNAL_PAGES = (
#     ('Tags', TAGS_URL, TAGS_SAVE_AS),
#     ('Authors', AUTHORS_URL, AUTHORS_SAVE_AS),
#     ('Categories', CATEGORIES_URL, CATEGORIES_SAVE_AS),
#     ('Archives', ARCHIVES_URL, ARCHIVES_SAVE_AS),
# )

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

STATIC_PATHS = ['docs']

DIRECT_TEMPLATES = ["index", "archives"]

PAGINATION_PATTERNS = (
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)
