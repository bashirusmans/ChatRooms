from django.test import TestCase, Client
from django.urls import reverse


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
