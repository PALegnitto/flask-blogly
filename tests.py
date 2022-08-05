from unittest import TestCase

from app import app, db
from models import User, Post

# DEFAULT_IMAGE_URL

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None,
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id
        self.user_img = test_user.image_url

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    """User tests"""

    def test_list_users(self):
        """Test users show up in user list"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_user(self):
        """Test adding a user and displaying on user page"""
        with self.client as c:
            resp = c.post('/users/new',
                          data={"first-name": "test_third", "last-name": "test_last",
                                "img": ""}, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_third', html)

    def test_user_details(self):
        """Test showing user profile page"""
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('button formmethod="get"', html)

    def test_user_edit(self):
        """Test editing and user and showing changes"""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/edit',
                          data={"first-name": "edited_name", "last-name": "last_one",
                                "img": self.user_img}, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("edited_name", html)

    def test_user_delete(self):
        """Test deleting a user and displaying delete message"""
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete',
                          follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("User Deleted", html)

    """Post tests"""

    def test_add_post(self):
        """Test adding a post and displaying title on user page"""
        with self.client as c:
            resp = c.post(f"/users/{self.user_id}/posts/new",
                          data={"post-title": "test", "post-content": "tacos"},
                          follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("test</a></li>", html)

    def test_edit_post(self):
        """Test posts is edited and new content is displayed"""
        with self.client as c:

            # make a post to edit
            c.post(f"/users/{self.user_id}/posts/new",
                   data={"post-title": "test", "post-content": "tacos"})

            user = User.query.get(self.user_id)
            post = user.posts[0]

            # edit the post
            resp = c.post(f"/posts/{post.id}/edit",
                          data={"post-title": "changed",
                                "post-content": "burritos"},
                          follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("burritos", html)

    def test_post_delete(self):
        """Test a post is deleted and message is flashed"""
        with self.client as c:

            c.post(f"/users/{self.user_id}/posts/new",
                   data={"post-title": "test", "post-content": "tacos"})

            user = User.query.get(self.user_id)
            post = user.posts[0]

            resp = c.post(f"/posts/{post.id}/delete",
                          follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Post Deleted", html)
