from db import DB

class ForumDB(DB):
    def __init__(self):
        super().__init__(DB.FORUM_DB, DB.FORUM_MAIN_TABLE)

    def create_table(self):
        super().execute_script('data/forum.sql')

    def create_user(self, first_name, last_name, email, salt, password_hash, is_admin):
        sql, args = 'INSERT INTO user (first_name, last_name, email, salt, password_hash, is_admin) VALUES (?, ?, ?, ?, ?, ?)', (first_name, last_name, email, salt, password_hash, is_admin)
        super().insert(sql, args)

    def select_user(self, email):
        sql, args = 'SELECT * FROM user WHERE email = ?', (email,)
        user = super().select_one(sql, args)
        return user

    def get_all_users(self):
        sql, args = 'SELECT * FROM user', ()
        users = super().select_all(sql, args)
        return users;

    def create_forum(self, topic, user_email):
        sql, args = 'INSERT INTO forum (topic, user_email) VALUES (?, ?)', (topic, user_email)
        super().insert(sql, args)

    def get_all_forums(self):
        sql, args = 'SELECT * FROM forum', ()
        forums = super().select_all(sql, args)
        return forums

    def create_comment(self, comment, forum_id, user_email):
        sql, args = 'INSERT INTO comment (comment, forum_id, user_email) VALUES (?, ?, ?)', (comment, forum_id, user_email)
        super().insert(sql, args)

    def get_all_comments(self):
        sql, args = 'SELECT * FROM comment', ()
        comments = super().select_all(sql, args)
        return comments
    
    def get_all_comments_by_forum_id(self, forum_id):
        sql, args = 'SELECT * FROM comment WHERE forum_id = ?', (forum_id,)
        comments = super().select_all(sql, args)
        return comments
    
    def delete_forum(self, forum_id):
        comments = self.get_all_comments_by_forum_id(forum_id)
        for comment in comments:
            comment_id = comment['id']
            self.delete_comment(comment_id)

        sql, args = 'DELETE FROM forum WHERE id = ?', (forum_id,)
        super().delete(sql, args)
    
    def delete_comment(self, comment_id):
        sql, args = 'DELETE FROM comment WHERE id = ?', (comment_id,)
        super().delete(sql, args)