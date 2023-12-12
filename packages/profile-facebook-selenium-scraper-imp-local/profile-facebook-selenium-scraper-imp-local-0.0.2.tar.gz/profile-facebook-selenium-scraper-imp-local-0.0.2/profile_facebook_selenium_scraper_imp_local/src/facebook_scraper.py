"""
FacebookScraper Class:

This class defines a Facebook scraper to gather
information about friends on Facebook.
It uses Selenium for web scraping and provides methods for logging in,
extracting data about friends."""
from dotenv import load_dotenv
load_dotenv()
import time  # noqa: E402
import json  # noqa: E402
# import os
from datetime import datetime  # noqa: E402
from language_local import lang_code  # noqa: E402
from selenium import webdriver  # noqa: E402
from selenium.webdriver.common.by import By  # noqa: E402
from selenium.webdriver.support.ui import WebDriverWait  # noqa: E402
from selenium.webdriver.support import expected_conditions as EC  # noqa: E402
from selenium.common.exceptions import NoSuchElementException  # noqa: E402
# from external_user_local.external_user import ExternalUser
from profile_local.comprehensive_profile import ComprehensiveProfilesLocal  # noqa:E402
from logger_local.Logger import Logger  # noqa: E402
from logger_local.LoggerComponentEnum import LoggerComponentEnum  # noqa: E402


LANG_CODE_HE = lang_code.LangCode.HEBREW.value
QUEUE_LOCAL_PYTHON_COMPONENT_ID = 245
QUEUE_LOCAL_PYTHON_COMPONENT_NAME = "\
    profile_facebook_selenium_scraper_imp_local/\
    src/facebook_scraper"
DEVELOPER_EMAIL = 'neomi.b@circ.zone'
DEFAULT_STARS = 0
DEFAULT_LAST_DIALOG_WORKFLOW_STATE_ID = 0
SYSTEM_ID = 1


class FacebookScraper:
    """
    Class for scraping Facebook friends' information."""

    def __init__(self) -> None:
        """
        Initializes the FacebookScraper class."""
        self.name = 'name'
        # self.username = 'username'
        self.gender = 1
        self.job_title = 'job_title'
        self.address = 'address'

        self.logger = Logger(
            object={
                'component_id': QUEUE_LOCAL_PYTHON_COMPONENT_ID,
                'component_name': QUEUE_LOCAL_PYTHON_COMPONENT_NAME,
                'component_category':
                LoggerComponentEnum.ComponentCategory.Code.value,
                'developer_email': DEVELOPER_EMAIL
            }
        )
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 10)

    def extract_and_cast_to_int(self, input_string: str) -> int:
        """
        Extracts and casts the first integer from the given input string."""
        number = [int(s) for s in input_string.split() if s.isdigit()]
        return number[0] if number else None

    def login(self, facebook_user_identifier: str,
              facebook_password: str) -> None:
        """
        Login to the account by given username and facebook_password."""
        try:
            self.logger.start("Logging into Facebook", object={
                "facebook_user_identifier": facebook_user_identifier
            })
            self.driver.get('https://www.facebook.com/')
            time.sleep(5)
            facebook_user_identifier_input = self.driver.find_element(
                By.ID, 'email')
            facebook_password_input = self.driver.find_element(By.ID, 'pass')

            facebook_user_identifier_input.send_keys(facebook_user_identifier)
            facebook_password_input.send_keys(facebook_password)
            facebook_password_input.submit()

            self.wait.until(EC.url_contains('facebook.com'))
            time.sleep(10)
            self.logger.end("Login successful")
        except NoSuchElementException:
            self.logger.error("Login failed")

    def get_num_friends(self) -> int:
        """
        Gets the number of friends from the Facebook friends list."""
        try:
            self.logger.start("Getting the number of friends")
            self.driver.get('https://www.facebook.com/friends/list')
            time.sleep(5)
            num_friends_css_selector = 'div.xu06os2:nth-child(3) > \
                div:nth-child(1) >div:nth-child(1) > div:nth-child(1) >\
                      div:nth-child(1) > div:nth-child(1) >\
                    h2:nth-child(1) > span:nth-child(1) > span:nth-child(1)'
            num_of_friends = self.driver.find_element(
                By.CSS_SELECTOR, num_friends_css_selector).text
            num_of_friends = self.extract_and_cast_to_int(num_of_friends)
            self.logger.end("Successfully retrieved the number of friends")
            return num_of_friends
        except NoSuchElementException:
            self.logger.error("Error getting the number of friends")
            return None

    def click_friend(self, j: int) -> None:
        """
        Clicks on the friend with the specified index."""
        try:
            self.logger.start(f"Clicking on friend with index {j}")
            friend_css_selector = f'.x135pmgq > div:nth-child({j}) >\
                  a:nth-child(1) >div:nth-child(1) > div:nth-child(2) >\
                      div:nth-child(1) > div:nth-child(1)> div:nth-child(1) >\
                          div:nth-child(1) > span:nth-child(1) >\
                              span:nth-child(1)\
                        > span:nth-child(1)'
            friend = self.driver.find_element(By.CSS_SELECTOR,
                                              friend_css_selector)
            friend.click()
            time.sleep(5)
            self.logger.end(f"Clicked on friend with index {j}")
        except NoSuchElementException:
            self.logger.error(f"Error clicking on friend with index {j}")

    def get_friend_name(self) -> str:
        """
        Gets the name of the current friend."""
        try:
            self.logger.start("Getting friend's name")
            friend_name_css_selector = '.x14qwyeo > h1:nth-child(1)'
            friend_name = self.driver.find_element(By.CSS_SELECTOR,
                                                   friend_name_css_selector
                                                   ).text
            self.logger.end(f"Successfully \
                            retrieved friend's name: {friend_name}")
            return friend_name
        except NoSuchElementException:
            self.logger.error("Error getting friend's name")
            return ""

    def click_about_friend(self) -> None:
        """
        Clicks on the 'About' section of the current friend's profile."""
        try:
            self.logger.start("Clicking on the 'About' \
                              section of the current friend's profile")
            about_friend_css_selector = '.x879a55 > div:nth-child(1) >\
                  div:nth-child(1) >div:nth-child(1) > div:nth-child(1) >\
                      div:nth-child(1) > div:nth-child(1) >a:nth-child(3) >\
                          div:nth-child(1) > span:nth-child(1)'
            about_friend = self.driver.find_element(By.CSS_SELECTOR,
                                                    about_friend_css_selector)
            about_friend.click()
            time.sleep(5)
            self.logger.end("Clicked on the 'About' section successfully")
        except NoSuchElementException:
            self.logger.error("Error clicking on the 'About' section")

    def get_job_title(self) -> str:
        """
        Gets the work place information of the current friend."""
        try:
            self.logger.start(
                "Getting work place information of the current friend")
            try:
                job_title_css_selector = '.xqmdsaz > div:nth-child(1) >\
                      div:nth-child(1) >div:nth-child(2) > div:nth-child(1) >\
                          div:nth-child(1) > div:nth-child(2) >\
                            div:nth-child(1) > span:nth-child(1) > \
                                a:nth-child(1) > span:nth-child(1) >\
                                    span:nth-child(1)'
                job_title = self.driver.find_element(
                    By.CSS_SELECTOR, job_title_css_selector).text
                self.logger.end(
                    "Successfully retrieved work place information")
                return job_title
            except NoSuchElementException:
                return None
        except NoSuchElementException:
            self.logger.error("Error getting work place information")

    def get_went_to(self) -> str:
        """
        Gets the 'Went to' information of the current friend.
        """
        try:
            try:
                self.logger.start(
                    "Getting 'Went to' information of the current friend")
                went_to_css_selector = 'div.x1hq5gj4:nth-child(3) >\
                      div:nth-child(1) >div:nth-child(1) > div:nth-child(2) >\
                          div:nth-child(1) > span:nth-child(1)'
                went_to = self.driver.find_element(
                    By.CSS_SELECTOR, went_to_css_selector).text
                self.logger.end("Successfully retrieved 'Went to' information")
                return went_to
            except NoSuchElementException:
                return None
        except NoSuchElementException:
            self.logger.error("Error getting 'Went to' information")

    def get_address(self) -> str:
        """
        Gets the residential location information of the current friend."""
        try:
            self.logger.start(
                "Getting residential location \
                    information of the current friend")
            address_css_selector = 'div.x1hq5gj4:nth-child(4) >\
                  div:nth-child(1) >div:nth-child(1) >\
                      div:nth-child(2) > div:nth-child(1) >\
                          span:nth-child(1) >a:nth-child(1) >\
                              span:nth-child(1) > span:nth-child(1)'
            address = self.driver.find_element(
                By.CSS_SELECTOR, address_css_selector).text
            self.logger.end(
                "Successfully retrieved residential location information")
            return address
        except NoSuchElementException:
            self.logger.error("Error getting residential location information")
            return None

    def click_about_basic_info_friend(self) -> None:
        """
        Clicks on the 'About' section and then the 'Basic Info' subsection
        of the current friend's profile."""
        try:
            self.logger.start(
                "Clicking on 'Basic Info' subsection\
                      of the current friend's profile")
            self.click_about_friend()

            basic_info_css_selector = 'div.x1e56ztr:nth-child(5)'
            basic_info = self.driver.find_element(
                By.CSS_SELECTOR, basic_info_css_selector)
            basic_info.click()
            time.sleep(5)
            self.logger.end("Clicked on 'Basic Info' subsection successfully")
        except NoSuchElementException:
            self.logger.error("Error clicking on 'Basic Info' subsection")

    def get_gender_type(self) -> str:
        """
        Gets the gender information of the current friend."""
        self.click_about_basic_info_friend()
        try:
            self.logger.start(
                "Getting gender information of the current friend")
            gender_css_selector = '.xqmdsaz > div:nth-child(3) >\
                  div:nth-child(1) >div:nth-child(2) > div:nth-child(1) >\
                      div:nth-child(1) > div:nth-child(2) >div:nth-child(1) >\
                          div:nth-child(1) > div:nth-child(1) >\
                              div:nth-child(1) >div:nth-child(1) >\
                                  span:nth-child(1)'
            gender = self.driver.find_element(By.CSS_SELECTOR,
                                              gender_css_selector).text
            self.logger.end("Successfully retrieved gender information")
            if gender == 'Female':
                gender = 1
                return gender
            if gender == 'Male':
                gender = 2
                return gender
        except NoSuchElementException:
            self.logger.error("Error getting gender information")
            return None

    def convert_to_date(self, date_string: str) -> datetime:
        """
        Converts a date string to a datetime object."""
        default_date_format = "%B %d %Y"
        try:
            self.logger.start("Converting date string to datetime object",
                              object={
                                       "date_string": date_string})
            date_object = datetime.strptime(date_string, default_date_format)
            self.logger.end("Conversion successful")
            return date_object
        except NoSuchElementException:
            self.logger.error("Error converting date string")
            return None

    def get_birth_date(self) -> datetime:
        """
        Gets the birth date of the current friend."""
        self.click_about_basic_info_friend()
        try:
            self.logger.start("Getting birth date of the current friend")
            birth_date_css_selector = 'div.xat24cr:nth-child(3) >\
                  div:nth-child(1) >div:nth-child(1) > div:nth-child(2) >\
                      div:nth-child(1) > div:nth-child(1) >div:nth-child(1) >\
                       div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
            birth_date = self.driver.find_element(By.CSS_SELECTOR,
                                                  birth_date_css_selector).text
            birth_year_css_selector = 'div.xat24cr:nth-child(3) >\
                  div:nth-child(1) >div:nth-child(1) > div:nth-child(2) >\
                    div:nth-child(2) > div:nth-child(1) >div:nth-child(1) >\
                       div:nth-child(1) > div:nth-child(1) > span:nth-child(1)'
            self.logger.end("Successfully retrieved birth date")
            birth_year = self.driver.find_element(By.CSS_SELECTOR,
                                                  birth_year_css_selector).text
            birth_date = birth_date + " " + birth_year
            return self.convert_to_date(birth_date)
        except NoSuchElementException:
            self.logger.error("Error getting birth date")
            return None

    def scrape_friends(self) -> None:
        """
        Scrapes information about the friends
        and inserts it into the database."""
        try:
            self.logger.start("Scraping information about friends")
            num_of_friends = self.get_num_friends()

            frind_css_selector_index = 4

            for _ in range(num_of_friends):
                self.click_friend(frind_css_selector_index)
                self.name = self.get_friend_name()

                self.click_about_friend()
                self.job_title = self.get_job_title()
                # went_to = self.get_went_to()
                self.address = self.get_address()
                self.gender = self.get_gender_type()
                # birth_date = self.get_birth_date()

                frind_css_selector_index += 1

                self.insert_to_database()

            self.logger.end("Scraping completed")
        except NoSuchElementException:
            self.logger.error("Error during scraping")
        finally:
            time.sleep(10)
            self.driver.quit()

    def generate_compatible_json(self, profile_entry: dict):
        """
        generate_compatible_json."""
        profile = {
            'number': profile_entry.get('number', None),
            'profile_name': profile_entry.get('name', None),
            'name': profile_entry.get('name', None),
            'name_approved': True,
            'lang_code': profile_entry.get('language', LANG_CODE_HE),
            # 'user_id': logger.user_context.get_real_user_id(),
            'person_id': profile_entry.get('person_id', None),
            'is_main': profile_entry.get('is_main', 0),
            'profile_type_id': profile_entry.get('profile_type_id', 1),
            'is_approved': profile_entry.get('is_approved', 0),
            # 'preferred_lang_code': profile_entry.get('language',
            # LangCode.ENGLISH.value),
            # 'is_main': profile_entry.get('is_main', None),
            'preferred_lang_code': profile_entry.get('language', None),
            'is_rip': profile_entry.get('rip', 0),
            "main_phone_id": profile_entry.get('main_phone_id', 1),
            "gender_id": profile_entry.get('gender_id', 1),
            "stars": profile_entry.get('stars', 0),
            'experience_years_min': profile_entry.get(
                'experience_years_min', None),
            'last_dialog_workflow_state_id': profile_entry.get(
                'last_dialog_workflow_state_id', 0),
            'visibility_id': profile_entry.get('visibility_id', 0),
        }
        location = {
            'coordinate': {
                'latitude': profile_entry.get('latitude', 0),
                'longitude': profile_entry.get('longitude', 0),
            },
            'address_local_language': profile_entry.get('language', None),
            'address_english': profile_entry.get('street', None),
            'postal_code': profile_entry.get('zip', None),
            'plus_code': profile_entry.get('plus_code', None),
            'neighborhood': profile_entry.get('neighborhood', None),
            'county': profile_entry.get('county', None),
            'region': profile_entry.get('region', None),
            'state': profile_entry.get('state', 'Israel'),
            'country': profile_entry.get('country', None)
        }

        entry = {
            "location": location,
            "profile": profile,
        }

        return json.dumps(entry)

    def insert_to_database(self) -> None:
        """insert."""
        self.logger.start()
        profile_json = {
                'name': self.name,
                'gender_id': self.gender,
                'lang_code': LANG_CODE_HE,
                'visibility_id': True,
                'is_approved': False,
                'stars': DEFAULT_STARS,
                'last_dialog_workflow_state_id':
                DEFAULT_LAST_DIALOG_WORKFLOW_STATE_ID,
                'job_title': self.job_title,
                'address_english': self.address
        }

        profile_str = self.generate_compatible_json(profile_json)
        ComprehensiveProfilesLocal.insert(profile_str, LANG_CODE_HE)
        # access_token = os.getenv("FACEBOOK_GRAPH_IMPORT_API_ACCESS_TOKEN")
        # ExternalUser.insert_or_update_external_user_access_token(
        #     self.username, profile_id, SYSTEM_ID, access_token)
        self.logger.end()


if __name__ == "__main__":
    fb_scraper = FacebookScraper()

    FACEBOOK_USER_IDENTIFIER = "neomi.b@circ.zone"
    FACEBOOK_PASSWORD = "Neo1Bas2Circ3!"

    try:
        fb_scraper.login(FACEBOOK_USER_IDENTIFIER, FACEBOOK_PASSWORD)
        fb_scraper.scrape_friends()
    except NoSuchElementException as e:
        fb_scraper.logger.error(f"An unexpected error occurred: {str(e)}")
