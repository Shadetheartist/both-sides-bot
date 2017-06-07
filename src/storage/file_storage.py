import json
import datetime


class FileStorage(object):

    def __init__(self, compare_list_file_path, post_history_file_path, sub_blacklist_file_path, user_blacklist_file_path):
        self.compare_list_file_path = compare_list_file_path
        self.post_history_file_path = post_history_file_path
        self.sub_blacklist_file_path = sub_blacklist_file_path
        self.user_blacklist_file_path = user_blacklist_file_path

    def get_subs_to_compare(self):
        return self.get_array_from_file(self.compare_list_file_path)

        try:
            return self.get_array_from_file(self.compare_list_file_path)
        except Exception as ex:
            print("Error: No compare list file exists at [{0}]".format(
                self.compare_list_file_path))
            return []

    def add_post_to_history(self, center_post, left_post, right_post):
        key = self.get_key(left_post, right_post, center_post)
        if self.is_in_history(key):
            print("Post set already in history: {0}".format(key))
            return

        json_str = json.dumps({
            'key': self.get_key(left_post, right_post, center_post),
            'left_post_id': left_post.id,
            'right_post_id': right_post.id,
            'center_post_id': center_post.id,
            'date_created': datetime.datetime.now().isoformat(),
            'last_updated': datetime.datetime.now().isoformat()
        })

        print("Adding To History: {0}".format(json_str))

        post_history_file = open(self.post_history_file_path, 'a+')

        print(json_str, file=post_history_file)

    def posts_have_been_compared(self, left_post, right_post):
        return self.get_post_info(left_post, right_post) is not None

    def get_post_history(self):
        blacklist = list()

        with open(self.post_history_file_path) as file:
            content = file.readlines()

            for line in content:
                data = json.loads(line.strip())
                blacklist.append(data)

        return blacklist

    def is_in_history(self, key):
        for json_data in self.get_post_history():
            if key == json_data['key']:
                return True
        return False

    def get_key(self, left_post, right_post, center_post):
        return left_post.id + right_post.id + center_post.id

    def get_post_info(self, left_post, right_post):
        for json_data in self.get_post_history():
            if {left_post.id, right_post.id} == {json_data['left_post_id'], json_data['right_post_id']}:
                return json_data
        return None

    def get_blacklisted_subs(self):
        return self.get_array_from_file(self.sub_blacklist_file_path)

    def is_sub_blacklisted(self, sub_display_name):
        sub_display_name = str.lower(sub_display_name)
        blacklist = self.get_blacklisted_subs()
        return sub_display_name in blacklist

    def get_blacklisted_users(self):
        return self.get_array_from_file(self.user_blacklist_file_path)

    def is_user_blacklisted(self, user_name):
        user_name = str.lower(user_name)
        blacklist = self.get_blacklisted_users()
        lowercase_blacklist = map(str.lower, blacklist)
        return user_name in lowercase_blacklist

    def blacklist_user(self, username):
        blacklist_file = open(self.user_blacklist_file_path, 'a+')
        print(username, file=blacklist_file)

    def get_array_from_file(self, filename):
        blacklist = list()

        with open(filename) as file:
            content = file.readlines()

            for line in content:
                blacklist.append(line.strip())

        return blacklist
