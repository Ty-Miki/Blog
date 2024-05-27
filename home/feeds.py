import markdown
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = "latest blogs"
    link = reverse_lazy("blog:post_list")
    description = "Latest posts from my blog."

    def items(self) -> list:
        return Post.published.all()[:5]
    def item_title(self, item: Post) -> str:
        return item.title
    def item_description(self, item: Post) -> str:
        return truncatewords_html(markdown.markdown(item.body), 30)
    def item_pubdate(self, item:Post) -> str:
        return item.publish