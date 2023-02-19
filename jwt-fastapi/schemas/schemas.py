
def post_serializer(post) -> dict:
        return {
            "id": str(post["id"]),
            "title": post["title"],
            "content" : post["content"]
        }


def posts_serializer(posts) -> list:
    return [post_serializer(post) for post in posts]