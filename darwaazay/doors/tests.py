from django.test import TestCase, Client
from django.urls import reverse
from django.test import SimpleTestCase
from django.urls import resolve,reverse
from doors.views import *
from doors.models import *
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from doors.forms import *
from django.core.exceptions import ValidationError  # Import ValidationError
from datetime import timedelta  # Import timedelta


# Create your tests here.
"""
The testing strategy for the Django test cases given below is comprehensive and well-organized. It starts by testing fundamental user 
authentication views, covering login, logout, and registration, ensuring proper template rendering and request handling. 
The strategy then progresses to user profile-related views, including updates and profile viewing. 
Core functionalities like accessing the home page, creating and managing rooms, and handling messages are thoroughly tested. 
The approach includes testing room management features such as updating and deleting rooms. 
The final tests focus on broader application features like displaying topics and user activity.
The strategy is enriched with clear print statements for progress visibility, 
and the inclusion of both positive and negative scenarios enhances test suite robustness.
To further strengthen the strategy, consideration of edge cases, user permissions, error handling, and security aspects would be beneficial.
"""


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_page_url = reverse("login")
        self.logout_page_url = reverse("logout")
        self.register_page_url = reverse("register")
        self.update_user_page_url = reverse("update-user")
        self.home_page_url = reverse("home")
        self.room_page_url = reverse("room", args=[1])
        self.user_profile_page_url = reverse("user-profile", args=[1])
        self.create_room_page_url = reverse("create-room")
        self.update_room_page_url = reverse("update-room", args=[1])
        self.delete_message_page_url = reverse("delete-message", args=[1])
        self.delete_room_page_url = reverse("delete-room", args=[1])
        self.topics_page_url = reverse("topics")
        self.activity_page_url = reverse("activity")

    def test_login_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.login_page_url)
        client = self.client
        response = client.get(self.login_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/login_register.html")

    def test_login_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.login_page_url)
        client = self.client
        response = client.post(
            self.login_page_url,
            {"email": "bashirusman3981@gmail.com", "password": "Yoman123"},
        )

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_logout_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.logout_page_url)
        client = self.client
        response = client.get(self.logout_page_url)

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_register_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.register_page_url)
        client = self.client
        response = client.get(self.register_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/login_register.html")

    def test_register_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.register_page_url)
        client = self.client
        response = client.post(
            self.register_page_url,
            {
                "name": "ahmed",
                "username": "ahmed",
                "email": "ahmed@gmail.com",
                "password1": "Yoman123",
                "password2": "Yoman123",
            },
        )

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_update_user_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.update_user_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.get(self.update_user_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/edit-user.html")

    def test_update_user_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.update_user_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.post(
            self.update_user_page_url,
            {
                "name": "ali",
                "username": "aliboyy",
                "email": "alihack@hotmail.cum",
                "bio": "your hack bro",
            },
        )

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_home_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.home_page_url)
        client = self.client
        response = client.get(self.home_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/home.html")

    def test_room_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.room_page_url)
        client = self.client
        response = client.get(self.room_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/room.html")

    def test_room_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.room_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.post(self.room_page_url, {"body": "Mau ni siri"})

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_user_profile_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.user_profile_page_url)
        client = self.client
        response = client.get(self.user_profile_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/profile.html")

    def test_create_room_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.create_room_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.get(self.create_room_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/room_form.html")

    def test_create_room_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.create_room_page_url)
        client = self.client
        response = client.post(
            self.create_room_page_url,
            {"topic": "python", "name": "I hack", "description": "OOfff"},
        )

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_update_room_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.update_room_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.get(self.update_room_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/room_form.html")

    def test_update_room_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.update_room_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.post(
            self.update_room_page_url,
            {
                "topic": "new-topic",
                "name": "new-name",
                "description": "new description",
            },
        )

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/room_form.html")

    def test_delete_room_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.delete_room_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.get(self.delete_room_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/delete.html")

    def test_delete_room_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.delete_room_page_url)
        client = self.client
        response = client.post(self.delete_room_page_url)

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_delete_message_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.delete_message_page_url)
        client = self.client
        self.test_login_page_POST()
        response = client.get(self.delete_message_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/delete.html")

    def test_delete_message_page_POST(self):
        print()
        print("Testing website for a POST Request to", self.delete_message_page_url)
        client = self.client
        response = client.post(self.delete_message_page_url)

        self.assertEquals(response.status_code, 302)
        print(
            "Test case passed with status code",
            response.status_code,
            "which means view has been redirected.",
        )

    def test_topic_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.topics_page_url)
        client = self.client
        response = client.get(self.topics_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/topics.html")

    def test_activity_page_GET(self):
        print()
        print("Testing website for a GET Request to", self.activity_page_url)
        client = self.client
        response = client.get(self.activity_page_url)

        self.assertEquals(response.status_code, 200)
        print(
            "Test case passed with status code:",
            response.status_code,
            "which means view has been rendered.",
        )
        self.assertTemplateUsed(response, "doors/activity.html")






# ------------------------------------testing urls --------------------------------------

class TestUrls(SimpleTestCase):
    
    
    # Test that the login URL resolves to the loginPage view
    def test_login_url_resolves(self):
        """
        Test that the login URL resolves to the loginPage view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `loginPage`.
            
        """
        url = reverse('login')
        resolver = resolve(url)
        self.assertEquals(resolver.func, loginPage)

    # Test that the logout URL resolves to the logoutUser view
    def test_logout_url_resolves(self):
        """
        Test that the logout URL resolves to the logoutUser view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `logoutUser`.
        """
        
        url = reverse('logout')
        resolver = resolve(url)
        self.assertEquals(resolver.func, logoutUser)

    # Test that the register URL resolves to the registerUser view
    def test_register_url_resolves(self):
        """
        Test that the register URL resolves to the registerUser view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `registerUser`.
        """
        url = reverse('register')
        resolver = resolve(url)
        self.assertEquals(resolver.func, registerUser)

    # Test that the update-user URL resolves to the updateUser view
    def test_update_user_url_resolves(self):
        """
        Test that the update-user URL resolves to the updateUser view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `updateUser`.
        """
        url = reverse('update-user')
        resolver = resolve(url)
        self.assertEquals(resolver.func, updateUser)

    # Test that the home URL resolves to the home view
    def test_home_url_resolves(self):
        """
        Test that the home URL resolves to the home view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `home`.
        """
        url = reverse('home')
        resolver = resolve(url)
        self.assertEquals(resolver.func, home)

    # Test that the room URL resolves to the room view
    def test_room_url_resolves(self):
        """
        Test that the room URL resolves to the room view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `room`.
        """
        url = reverse('room', args=['some_pk'])
        resolver = resolve(url)
        self.assertEquals(resolver.func, room)

    # Test that the user-profile URL resolves to the userProfile view
    def test_user_profile_url_resolves(self):
        """
        Test that the user-profile URL resolves to the userProfile view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `userProfile`.
        """
        url = reverse('user-profile', args=['some_pk'])
        resolver = resolve(url)
        self.assertEquals(resolver.func, userProfile)

    # Test that the create-room URL resolves to the createRoom view
    def test_create_room_url_resolves():
        """
        Test that the create-room URL resolves to the createRoom view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `createRoom`.
        """
        url = reverse('create-room')
        resolver = resolve(url)
        assert resolver.func == createRoom

    # Test that the update-room URL resolves to the updateRoom view
    def test_update_room_url_resolves():
        """
        Test that the update-room URL resolves to the updateRoom view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `updateRoom`.
        """
        url = reverse('update-room', args=['some_pk'])
        resolver = resolve(url)
        assert resolver.func == updateRoom


    # Test that the delete-room URL resolves to the deleteRoom view
    def test_delete_room_url_resolves():
        """
        Test that the delete-room URL resolves to the deleteRoom view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `deleteRoom`.
        """
        url = reverse('delete-room', args=['some_pk'])
        resolver = resolve(url)
        assert resolver.func == deleteRoom


    # Test that the delete-message URL resolves to the deleteMessage view
    def test_delete_message_url_resolves():
        """
        Test that the delete-message URL resolves to the deleteMessage view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `deleteMessage`.
        """
        url = reverse('delete-message', args=['some_pk'])
        resolver = resolve(url)
        assert resolver.func == deleteMessage


    # Test that the topics URL resolves to the topicsPage view
    def test_topics_url_resolves():
        """
        Test that the topics URL resolves to the topicsPage view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `topicsPage`.
        """
        url = reverse('topics')
        resolver = resolve(url)
        assert resolver.func == topicsPage


    # Test that the activity URL resolves to the activityPage view
    def test_activity_url_resolves():
        """
        Test that the activity URL resolves to the activityPage view.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the resolved function is `activityPage`.
        """
        url = reverse('activity')
        resolver = resolve(url)
        assert resolver.func == activityPage


# ---------------------------------------------- testing modals ---------------------------------
class TestModels(TestCase):
    class MessageModelTests(TestCase):

        def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.room = Room.objects.create(name='Test Room', host=self.user)

    def test_create_message_with_valid_data():
        """
        Test creating a message with valid data.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the created message attributes match the expected values.
        """
        # Set up the necessary data
        user = User.objects.create_user(username='testuser', password='testpassword')
        room = Room.objects.create(name='Test Room', host=user)

        # Create a message with valid data
        message = Message.objects.create(
            user=user,
            room=room,
            body='This is a test message'
        )

        # Assert that the message attributes match the expected values
        assert message.user == user
        assert message.room == room
        assert message.body == 'This is a test message'


                

    def test_str_method():
        """
        Test the __str__ method of the Message model.

        Parameters:
            None

        Returns:
            None

        Raises:
            AssertionError: If the test fails to assert that the truncated string representation matches the expected value.
        """
        # Set up the necessary data
        user = User.objects.create_user(username='testuser', password='testpassword')
        room = Room.objects.create(name='Test Room', host=user)

        # Create a message with a specific body
        message = Message.objects.create(
            user=user,
            room=room,
            body='Fever signals immune response; often caused by infections or underlying conditions.'
        )

        # Assert that the truncated string representation matches the expected value
        expected_str = 'Fever signals immune response; often caused by inf'
        assert str(message) == expected_str

            
         
        
        
# --------------------testing formss---------------
class TestForms(SimpleTestCase):
    class MyUserCreationFormTest(TestCase):

        def test_valid_form(self):
            # Create a valid form with dummy data
            form_data = {
                'name': 'Test User',
                'username': 'test_user',
                'email': 'test@example.com',
                'password1': 'Password.123',
                'password2': 'Password.123',
            }
            form = MyUserCreationForm(data=form_data)

            # Print form errors for debugging
            if not form.is_valid():
                print(form.errors)

            # Assert that the form is valid
            self.assertTrue(form.is_valid())


        def test_required_fields(self):
            # Test that all required fields are present
            form = MyUserCreationForm(data={})
            self.assertFalse(form.is_valid())
            self.assertIn('name', form.errors)
            self.assertIn('username', form.errors)
            self.assertIn('email', form.errors)
            self.assertIn('password1', form.errors)
            self.assertIn('password2', form.errors)

        def test_password_mismatch(self):
            # Test that the form detects password mismatch
            form_data = {
                'name': 'Test User',
                'username': 'test_user',
                'email': 'test@example.com',
                'password1': 'password123',
                'password2': 'different_password',
            }
            form = MyUserCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('password2', form.errors)

        def test_email_unique_constraint(self):
            # Test that the form enforces the unique constraint on email
            existing_user = get_user_model().objects.create_user(
                name='Existing User',
                username='existing_user',
                email='existing@example.com',
                password='existing_password'
            )

            form_data = {
                'name': 'Test User',
                'username': 'test_user',
                'email': 'existing@example.com',  # This email is already taken
                'password1': 'password123',
                'password2': 'password123',
            }
            form = MyUserCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors) 
            
    # >>>>>>>><<<<<<<<<<<<<<<<<<<<<<
    class RoomFormTest(TestCase):
        
        def setUp(self):
            self.user = User.objects.create_user(username='testuser', password='testpassword')
            self.topic = Topic.objects.create(name='Test Topic')

        def test_create_room_with_valid_data(self):
            room = Room.objects.create(
                name='Test Room',
                host=self.user,
                topic=self.topic,
                description='This is a test room description'
            )
            self.assertEqual(room.name, 'Test Room')
            self.assertEqual(room.host, self.user)
            self.assertEqual(room.topic, self.topic)
            self.assertEqual(room.description, 'This is a test room description')


        def test_remove_host_or_topic(self):
            room = Room.objects.create(name='Test Room', host=self.user, topic=self.topic)
            self.user.delete()
            self.topic.delete()
            room.refresh_from_db()
            self.assertIsNone(room.host)
            self.assertIsNone(room.topic)

        def test_ordering(self):
            room1 = Room.objects.create(name='Room 1', host=self.user, topic=self.topic)
            room2 = Room.objects.create(name='Room 2', host=self.user, topic=self.topic)
            room2.updated = room2.updated - timedelta(days=1)  # Modify update time
            rooms = Room.objects.all()
            self.assertEqual(list(rooms), [room2, room1])  # Ordered by -updated, then -created

        def test_str_method(self):
            room = Room.objects.create(name='Test Room', host=self.user, topic=self.topic)
            self.assertEqual(str(room), 'Test Room')

        def test_form_clean_data(self):
            # Test any custom cleaning logic in the form's clean() method
            pass  # Implement specific tests for cleaning logic
    class UserFormTest(TestCase):

        def test_valid_form(self):
            form_data = {
                'avatar': 'test_avatar.png',
                'name': 'Test User',
                'username': 'test_username',
                'email': 'test@example.com',
                'bio': 'This is a test bio',
            }
            form = UserForm(data=form_data)
            self.assertTrue(form.is_valid())

        def test_blank_data(self):
            form = UserForm(data={})
            self.assertFalse(form.is_valid())
            self.assertEqual(len(form.errors), 4)  # Assuming there are 4 required fields in the form

        def test_invalid_email(self):
            form_data = {
                'avatar': 'test_avatar.png',
                'name': 'Test User',
                'username': 'test_username',
                'email': 'invalid_email',  # Invalid email
                'bio': 'This is a test bio',
            }
            form = UserForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('email', form.errors)

        def test_form_save(self):
            form_data = {
                'avatar': 'test_avatar.png',
                'name': 'Test User',
                'username': 'test_username',
                'email': 'test@example.com',
                'bio': 'This is a test bio',
            }
            form = UserForm(data=form_data)
            self.assertTrue(form.is_valid())

            # Assuming you have overridden the save method in your User model
            user_instance = form.save(commit=False)
            self.assertEqual(user_instance.name, 'Test User')
            self.assertEqual(user_instance.username, 'test_username')
            self.assertEqual(user_instance.email, 'test@example.com')
            self.assertEqual(user_instance.bio, 'This is a test bio')
            # Add more assertions based on your model fields

            # Save the instance to the database
            user_instance.save()

            # Retrieve the instance from the database and assert its values
            saved_user = User.objects.get(pk=user_instance.pk)
            self.assertEqual(saved_user.name, 'Test User')




