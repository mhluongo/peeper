import argparse, mechanize
from lxml import etree
from urlparse import urljoin

def find_image_urls(url=None, html=None, duplicate=False, alphabetical=False):
  assert url is not None or html is not None
  if html == "": return []
  urls = _find_image_urls(url, html)
  if not duplicate: urls = uniquify(urls)
  if alphabetical: urls.sort()
  return urls

def uniquify(seq):
  seen = set()
  return [x for x in seq if x not in seen and not seen.add(x)]


def _find_image_urls(url, html):
  tree = get_tree(url, html)
  base = get_base(tree, url)
  return [
    urljoin(base, x.attrib['src'])
    for x in tree.xpath('//img')
    if 'src' in x.attrib ]

def get_tree(url, html):
  parser = etree.HTMLParser()
  if html is None:
    response = mechanize.Browser().open(url)
    return etree.parse(source=response, parser=parser, base_url=url)
  else:
    return etree.fromstring(text=html, parser=parser, base_url=url)

def get_base(tree, url):
  for base in tree.xpath('//base'):
    if 'href' in base.attrib:
      return _urljoin(base.attrib['href'], url)
  return url

def _urljoin(href, url=None):
  if url is None: return href
  else: return urljoin(url, href)

def get_arg_parser():
  parser = argparse.ArgumentParser()
  parser.add_argument('-u', '--url', type=str)
  parser.add_argument('-d', '--duplicate', action='store_true')
  parser.add_argument('-a', '--alphabetical', action='store_true')
  parser.add_argument('-x', '--html')
  return parser

if __name__ == '__main__':
  args = get_arg_parser().parse_args()
  print '\n'.join(find_image_urls(**vars(args)))
