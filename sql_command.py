import mysql.connector
import requests
import psycopg2
import os

_config = {
    "postgres":{
        "url": os.environ['DATABASE_URL']
    }
}

class Database():

    def _conn(func):
        def wrapper(self, *args, **kwargs):
            self.cur = self.conn.cursor()
            result = func(self, *args, **kwargs)
            self.cur.close()
            return result
        return wrapper

    def __init__(self, database_url = _config['postgres']['url']):
        self.default_subs = open('official_channels.txt').read().split('\n')
        try:
            self.conn = psycopg2.connect(database_url, sslmode='require')
        except:
            print('Error in creating connection/cursor')

    @_conn
    def add_user(self, user_id):
        # add user to Subscribers
        query = """
        INSERT INTO Subscribers (user_id, subs) VALUES (%i, '%s');
        """ %(user_id, 1)
        try:
            self.cur.execute(query)
            print(self.cur.rowcount, "User added")
            # add default list of subscription to Subscription
            for link in self.default_subs:
                print(link)
                query_channel = """
                INSERT INTO Subscription (user_id, channel) VALUES (%i, '%s');
                """ % (user_id, link)
                 

                self.cur.execute(query_channel)
                print(self.cur.rowcount, "Subs added")
            self.conn.commit()

        except Exception as e:
            print(e)
            # User already exist in table so pass
            pass

    @_conn
    def del_user(self, user_id):
        # del user from Subscribers
        query_user_del = """
        DELETE FROM Subscribers WHERE user_id=%i
        """ %(user_id)
        # del  all subscriptions from Subscriptions
        query_subs_del = """
        DELETE FROM Subscription WHERE user_id=%i;
        """ %(user_id)
        try:
            self.cur.execute(query_user_del)
            self.cur.execute(query_subs_del)
            self.conn.commit()
        except Exception as e:
            print(e)
            # User not exist in table so pass
            pass

    @_conn
    def del_subscription(self, user_id, channel):
        if 'https://t.me/' not in channel:
            return None


        query = """
        DELETE FROM Subscription WHERE user_id = %i AND channel = '%s'
        """ %(user_id, channel)

        try:
            self.cur.execute(query)
            self.conn.commit()
            return 1
        except:
            return None

    @_conn
    def get_subscriptions(self, user_id):

        query = """
        SELECT user_id, channel FROM Subscription WHERE user_id = %i
        """ % (user_id)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        # extract
        subscriptions = {}
        for row in rows:
            subscriptions[row[0]] = []
        for row in rows:
            subscriptions[row[0]].append(row[1])
        return subscriptions

    @_conn
    def get_links(self):

        query = """
        SELECT * FROM Subscription
        """
        self.cur.execute(query)
        rows = self.cur.fetchall()
        # extract
        links = []
        for row in rows:
            links.append(row[1])
        links = list(set(links))

        subscribers = { key: [] for key in links }
        for row in rows:
            subscribers[row[1]].append(row[0])
        return subscribers

    @_conn
    def get_users(self):

        query = """
        SELECT * FROM Subscribers; 
        """%()
        self.cur.execute(query)
        rec = self.cur.fetchall()
        #extract
        subscribers = {}
        for row in rec:
            subscribers[row[0]] = row[1]
        return subscribers

    @_conn
    def get_subscriptions(self, user_id):

        query = """
        SELECT user_id, channel FROM Subscription WHERE user_id = %i
        """ %(user_id)
        self.cur.execute(query)
        rows = self.cur.fetchall()
        # extract
        subscriptions = {}
        for row in rows:
            subscriptions[row[0]] = []
        for row in rows:
            subscriptions[row[0]].append(row[1])
        return subscriptions

    @_conn
    def add_subscription(self, user_id, channel):
        if 'https://t.me/' in channel:
            test = requests.get(channel)
            if test.status_code != 200:
                return None
        else:
            return None

        # select user subscription & check existing channel link

        query_subs_get = """
        SELECT user_id, channel FROM Subscription WHERE user_id = %i
        """ % (user_id)

        # add channel
        query_add_chan = """
        INSERT INTO Subscription ( user_id, channel) VALUES (%i, '%s');
        """ % (user_id, channel)
        try:
            self.cur.execute(query_subs_get)
            rows = self.cur.fetchall()
            # extract
            subscriptions = {}
            for row in rows:
                subscriptions[row[0]] = []
            for row in rows:
                subscriptions[row[0]].append(row[1])
            if channel in subscriptions[user_id]:
                return None
            

            self.cur.execute(query_add_chan)
            self.conn.commit()
            return 1
        except:
            return None

    @_conn
    def edit_user(self, user_id, value):
        try:

            query = """UPDATE Subscribers
            SET subs = %i WHERE user_id = %i;
            """%(value, user_id)
            self.cur.execute(query)
            self.conn.commit()
            return 1
        except Exception as e:
            print('In edit_user: ', e)

    def close(self):
            self.conn.close()

if __name__ == '__main__':
    db=Database()
    db.add_user(1)
    db.add_user(2)
    result = db.get_users()
    print(result)
    result = db.get_subscriptions(1)
    print(result)
    db.add_subscription(1,"https://t.me/ink")
    result = db.get_subscriptions(1)
    print(result)
    db.del_user(1)
    db.del_user(2)
    result = db.get_users()
    print(result)
    result = db.get_subscriptions(1)
    print(result)
    db.close()