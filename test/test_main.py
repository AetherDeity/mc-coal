import fix_dev_path

from main_test import AuthTest, ServerAuthTest
from models import Server, Command


TEST_USER_EMAIL = 'test@example.com'


class MainTest(AuthTest):
    URL = '/'

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response)

    def test_get_auth(self):
        pass

    def test_get_no_auth(self):
        response = self.get()
        self.assertRedirects(response)

    def test_get_inactive_user(self):
        self.log_in_user(email='hacker@example.com', is_active=False)
        response = self.get()
        self.assertRedirects(response)

    def test_get_logout(self):
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response)
        self.assertLoggedIn(response)
        self.log_out_user()
        response = self.get()
        self.assertRedirects(response)

    def test_get_login_again(self):
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response)
        self.assertLoggedIn(response)
        self.log_out_user()
        response = self.get()
        self.assertRedirects(response)
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response)
        self.assertLoggedIn(response)

    def test_get_multi_server(self):
        Server.create()
        self.log_in_user()
        response = self.get()
        self.assertOK(response)


class UserProfileTest(AuthTest):
    URL = '/profile'

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertOK(response)


class UsernameClaimTest(AuthTest):
    URL = '/players/claim'
    ALLOWED = ['POST']

    def __init__(self, *args, **kwargs):
        super(UsernameClaimTest, self).__init__(*args, **kwargs)
        self.params = {'username': 'steve'}

    def test_post_auth(self):
        self.log_in_user()
        response = self.post(params=self.params)
        self.assertRedirects(response)
        self.assertLoggedIn(response)

    def test_post_no_auth(self):
        response = self.post(params=self.params)
        self.assertRedirects(response)

    def test_post_inactive(self):
        self.log_in_user(email='hacker@example.com', is_active=False)
        response = self.post(params=self.params)
        self.assertRedirects(response)

    def test_post_logout(self):
        self.log_in_user()
        response = self.post(params=self.params)
        self.assertRedirects(response)
        self.assertLoggedIn(response)
        self.log_out_user()
        response = self.post(params=self.params)
        self.assertRedirects(response)

    def test_post_login_again(self):
        self.log_in_user()
        response = self.post()
        self.assertRedirects(response)
        self.assertLoggedIn(response)
        self.log_out_user()
        response = self.post()
        self.assertRedirects(response)
        self.log_in_user()
        response = self.post()
        self.assertRedirects(response)
        self.assertLoggedIn(response)

    def test_post(self):
        self.log_in_user()
        response = self.post(params=self.params)
        self.assertRedirects(response)


class HomeTest(ServerAuthTest):
    URL = '/servers/{0}'

    @property
    def url(self):
        return self.URL.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertOK(response)

    def test_get_with_slash(self):
        pass


class ChatsTest(ServerAuthTest):
    URL = '/servers/{0}/chats'

    @property
    def url(self):
        return self.URL.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertOK(response)

    def test_returns_html_content(self):
        self.log_in_user()
        response = self.get()
        self.assertEqual('text/html', response.content_type)

    def test_post(self):
        self.log_in_user()
        response = self.post(params={'chat': 'test'})
        self.assertCreated(response)
        self.assertEqual(1, Command.query().count())


class NakedTest(AuthTest):
    def test_get_inactive_server(self):
        if self.url:
            self.log_in_user()
            self.server.active = False
            self.server.put()
            response = self.get()
            if 'GET' in self.ALLOWED:
                self.assertRedirects(response, to='/')
            else:
                self.assertMethodNotAllowed(response)


class NakedChatsTest(NakedTest):
    URL = '/chats'

    def setUp(self):
        super(NakedChatsTest, self).setUp()
        self.redirect_to = '/servers/{0}/chats'.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response, to=self.redirect_to)

    def test_get_multi_server(self):
        Server.create()
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response, to='/')

    def test_get_auth(self):
        pass

    def test_get_login_again(self):
        pass

    def test_get_logout(self):
        pass


class ChatsInfiniteScrollTest(ServerAuthTest):
    URL = '/servers/{0}/chats'

    @property
    def url(self):
        return self.URL.format(self.server.key.urlsafe())

    def test_returns_status_OK(self):
        self.log_in_user()
        response = self.get(headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertOK(response)

    def test_returns_javascript_content(self):
        self.log_in_user()
        response = self.get(headers={'X-Requested-With': 'XMLHttpRequest'})
        self.assertEqual('text/javascript', response.content_type)

    def test_response_appends_event_rows(self):
        self.log_in_user()
        response = self.get(headers={'X-Requested-With': 'XMLHttpRequest'})
        response.mustcontain("""$('#live_events').append""")


class PlayersTest(ServerAuthTest):
    URL = '/servers/{0}/players'

    @property
    def url(self):
        return self.URL.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertOK(response)


class NakedPlayersTest(NakedTest):
    URL = '/players'

    def setUp(self):
        super(NakedPlayersTest, self).setUp()
        self.redirect_to = '/servers/{0}/players'.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response, to=self.redirect_to)

    def test_get_multi_server(self):
        Server.create()
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response, to='/')

    def test_get_auth(self):
        pass

    def test_get_login_again(self):
        pass

    def test_get_logout(self):
        pass


class PlaySessionsTest(ServerAuthTest):
    URL = '/servers/{0}/sessions'

    @property
    def url(self):
        return self.URL.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertOK(response)


class NakedPlayerSessionsTest(NakedTest):
    URL = '/sessions'

    def setUp(self):
        super(NakedPlayerSessionsTest, self).setUp()
        self.redirect_to = '/servers/{0}/sessions'.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response, to=self.redirect_to)

    def test_get_multi_server(self):
        Server.create()
        self.log_in_user()
        response = self.get()
        self.assertRedirects(response, to='/')

    def test_get_auth(self):
        pass

    def test_get_login_again(self):
        pass

    def test_get_logout(self):
        pass


class ScreenShotUploadTest(ServerAuthTest):
    URL = '/servers/{0}/screenshot_upload'

    @property
    def url(self):
        return self.URL.format(self.server.key.urlsafe())

    def test_get(self):
        self.log_in_user()
        response = self.get()
        self.assertOK(response)
        self.assertIn("http://localhost/_ah/upload/", response.body)

    # def test_post(self):
    #     self.log_in_user()
    #     response = self.get()
    #     body = response.body
    #     i = body.index("http://localhost/")
    #     j = body.index('"', i)
    #     url = body[i:j]
    #     self.post(url, {'file': None})
    #     self.assertRedirects(response, '/')
