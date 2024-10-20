from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from .models import Auction, Category, Bid
from django.urls import reverse
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


class AuctionTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            email='raketa@seznam.cz',
            password='Admin123456'
        )

        # Create a test category
        self.category = Category.objects.create(name="Cars")

    def test_create_auction(self):
        # Create a new auction
        auction = Auction.objects.create(
            title="Test Auction",
            description="This is a test auction.",
            user=self.user,
            category=self.category,
            minimum_amount=100.00,
            current_price=0.00,
            starting_price=100.00,
            buy_now_price=200.00,
            end_date=timezone.now() + timezone.timedelta(days=5)
        )

        # Check if the auction was created successfully
        self.assertEqual(auction.title, "Test Auction")
        self.assertEqual(auction.description, "This is a test auction.")
        self.assertEqual(auction.user.email, "raketa@seznam.cz")
        self.assertEqual(auction.category.name, "Cars")
        self.assertEqual(auction.minimum_amount, 100.00)
        self.assertEqual(auction.starting_price, 100.00)
        self.assertEqual(auction.buy_now_price, 200.00)
        self.assertFalse(auction.is_closed)


class BidTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(email='raketa@seznam.cz', password='Admin123456')

        # Create a category
        self.category = Category.objects.create(name='Cars')

        # Create an auction
        self.auction = Auction.objects.create(
            user=self.user,
            title='Test Auction',
            description='Test description',
            starting_price=100,
            minimum_amount=50,
            category=self.category,
            end_date=timezone.now() + timezone.timedelta(days=2)
        )

    def test_place_bid(self):
        # Log in the user
        self.client.login(email='raketa@seznam.cz', password='Admin123456')

        # Place a bid
        response = self.client.post(reverse('place_bid', args=[self.auction.pk]), {'amount': 150})

        # Check that the bid was placed successfully
        self.assertEqual(response.status_code, 302)  # Redirects after a successful bid
        self.assertTrue(Bid.objects.filter(auction=self.auction, user=self.user).exists())


class WatchlistTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = get_user_model().objects.create_user(email='raketa191@seznam.cz', password='Admin123456')

        # Create an auction
        self.category = Category.objects.create(name='Cars')
        self.auction = Auction.objects.create(
            user=self.user,
            title='Test Auction',
            description='Test description',
            starting_price=100,
            minimum_amount=50,
            category=self.category,
            end_date=timezone.now() + timezone.timedelta(days=2)
        )

    def test_add_to_watchlist(self):
        # Log in the user
        self.client.login(email='raketa191@seznam.cz', password='Admin123456')

        # Add the auction to the watchlist
        response = self.client.post(reverse('add_to_watchlist', args=[self.auction.pk]))

        # Check that the auction was added to the user's watchlist
        self.assertEqual(response.status_code, 302)  # Redirects after adding to watchlist
        self.assertTrue(self.auction in self.user.watchlist.all())


class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        options = webdriver.FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        cls.selenium = webdriver.Firefox(options=options)
        cls.selenium.implicitly_wait(10)
        User = get_user_model()
        cls.admin_user = User.objects.create_superuser(
            username='admin',
            password='password12345',
            email='admin@example.com'
        )

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_create_auction(self):
        # Step 1: Log in as admin
        self.selenium.get(f'{self.live_server_url}/accounts/login/')

        username_input = self.selenium.find_element(By.NAME, "username")
        password_input = self.selenium.find_element(By.NAME, "password")

        username_input.send_keys('admin@example.com')
        password_input.send_keys('password12345')
        time.sleep(2)

        submit_input = self.selenium.find_element(By.NAME, "submit")
        submit_input.click()
        time.sleep(2)

        # Step 2: Navigate to 'Create Auction' page
        self.selenium.get(f'{self.live_server_url}/auction/new/')
        time.sleep(2)

        # Step 3: Fill out auction form fields
        title_input = self.selenium.find_element(By.NAME, "title")
        description_input = self.selenium.find_element(By.NAME, "description")
        starting_price_input = self.selenium.find_element(By.NAME, "starting_price")
        minimum_price_input = self.selenium.find_element(By.NAME, "minimum_amount")
        buy_now_price_input = self.selenium.find_element(By.NAME, "buy_now_price")
        end_date_input = self.selenium.find_element(By.NAME, "end_date")

        title_input.send_keys("Test Auction")
        description_input.send_keys("This is a test description.")
        starting_price_input.send_keys("1000")
        minimum_price_input.send_keys("4000")
        buy_now_price_input.send_keys("10000")
        end_date_input.send_keys("2024-12-31 12:00:00")

        time.sleep(2)

        # Step 4: Submit the form
        submit_button = self.selenium.find_element(By.XPATH, '//button[@type="submit"]')
        submit_button.click()
        time.sleep(2)

        # Step 5: Assert auction was created
        self.assertIn("Title", self.selenium.page_source)
