from unittest import TestCase

from app import app, db
from models import User

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

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_add_user(self):
        with self.client as c:
            resp = c.post('/users/new',
                          data={"first-name": "test_third", "last-name": "test_last",
                                "img": None}, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertIsNotNone(User.query.get(self.user_id + 2))
            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_third', html)

    def test_user_details(self):
        with self.client as c:
            resp = c.get(f"/users/{self.user_id}")

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('button formmethod="get"', html)

    def test_user_edit(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/edit',
                          data={"first-name": "edited_name", "last-name": "last_one",
                                "img": None}, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("edited_name", html)
            self.assertEqual(User.query.get(self.user_id).first_name, "edited_name")

    def test_user_delete(self):
        with self.client as c:
            resp = c.post(f'/users/{self.user_id}/delete', follow_redirects = True)

            html = resp.get_data(as_text = True)

            self.assertEqual(resp.status_code, 200)
            self.assertIsNone(User.query.get(self.user_id))