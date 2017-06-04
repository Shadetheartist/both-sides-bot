from src.poster.standard_poster import StandardPoster

class TestPoster(StandardPoster):

    def submit_post(self, center_sub, left_post, right_post):

        post_info = self.output.build_post(left_post, right_post)

        new_post = None

        try:
            new_post = center_sub.submit(post_info[0], post_info[1])
        except Exception as ex:
            print("Error when submitting post")
            return

        self.add_comments(self.comment_limit, new_post, left_post, right_post)

        return new_post
