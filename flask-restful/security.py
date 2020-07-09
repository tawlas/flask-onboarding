from werkzeug.security import safe_str_cmp
from post import Post


posts = [Post(1, "bob", "asdf"), Post(1, "watt", "asdf")]

title_mapping = {p.title: p for p in posts}
postid_mapping = {p.id: p for p in posts}


def authenticate(title, description):
    post = title_mapping.get(title, None)
    if post and safe_str_cmp(post.description, description):
        return post


def identity(payload):
    post_id = payload["identity"]
    return postid_mapping.get(post_id, None)
