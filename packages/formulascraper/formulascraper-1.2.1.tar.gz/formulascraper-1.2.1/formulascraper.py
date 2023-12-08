"""
Module containing classes for scraping data from Formula websites.
"""
import re
import requests
from bs4 import BeautifulSoup


class Formula1Scraper:
    """
    Class for scraping Formula 1 data from the official website.
    """
    def __init__(self):
        """
        Initialize the class with the base URL for the website.
        """
        self.base_url_f1 = "https://www.formula1.com/en/results.html/"

    def get_drivers_data(self, year):
        """
        Scrape the driver data for a specific year.

        Args:
            year: The year for which to retrieve driver data.

        Returns:
            A list of dictionaries containing driver information for each driver.
        """
        if year < 1950:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1}{year}/drivers.html"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        drivers_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                driver_info = self._extract_driver_info(row)
                drivers_data.append(driver_info)

        return drivers_data

    def get_races_data(self, year):
        """
        Scrape the race data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing race information for each race.
        """
        if year < 1950:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1}{year}/races.html"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        races_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                race_info = self._extract_race_info(row)
                races_data.append(race_info)

        return races_data

    def get_teams_data(self, year):
        """
        Scrape the team data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing team information for each team.
        """
        if year < 1958:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1}{year}/team.html"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        teams_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                team_info = self._extract_team_info(row)
                teams_data.append(team_info)

        return teams_data

    def get_fastest_laps_data(self, year):
        """
        Scrape the fastest laps data for a specific year.

        Args:
            year: The year for which to retrieve fastest laps data.

        Returns:
            A list of dictionaries containing team information of fastests for each grandprix.
        """
        if year < 1950:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1}{year}/fastest-laps.html"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        fastest_laps_data = []
        for table in soup.find_all('table', class_='resultsarchive-table'):
            for row in table.find_all('tr')[1:]:
                fastest_lap_info = self._extract_fastest_lap_info(row)
                fastest_laps_data.append(fastest_lap_info)

        return fastest_laps_data

    def _extract_driver_info(self, row):
        position = re.findall(r'<td class="dark">(.*?)</td>', str(row))[0].strip()
        driver_name_pattern = r'<span class="hide-for-tablet">(.*?)</span>'
        driver_name = re.findall(driver_name_pattern, str(row))[0]
        driver_surname_pattern = r'<span class="hide-for-mobile">(.*?)</span>'
        driver_surname = re.findall(driver_surname_pattern, str(row))[0].strip()
        nat_pattern = r'<td class="dark semi-bold uppercase">(.*?)</td>'
        nationality = re.findall(nat_pattern, str(row))[0].strip()
        car = re.findall(r'.html">(.*?)</a>', str(row))[0].strip()
        points = re.findall(r'<td class="dark bold">(.*?)</td>', str(row))[0].strip()

        driver_info = {
            "position": position,
            "name": f"{driver_name} {driver_surname}",
            "nationality": nationality,
            "car": car,
            "points": points
        }

        return driver_info

    def _extract_race_info(self, row):
        grandprix = re.findall(r'html">\n {24}(.*?)\n {20}</a>', str(row))[0].strip()
        date = re.findall(r'<td class="dark hide-for-mobile">(.*?)</td>', str(row))[0]
        winner_name_pattern = r'<span class="hide-for-tablet">(.*?)</span>'
        winner_name = re.findall(winner_name_pattern, str(row))[0]
        winner_surname_pattern = r'<span class="hide-for-mobile">(.*?)</span>'
        winner_surname = re.findall(winner_surname_pattern, str(row))[0].strip()
        car = re.findall(r'<td class="semi-bold uppercase">(.*?)</td>', str(row))[0].strip()
        laps = re.findall(r'<td class="bold hide-for-mobile">(.*?)</td>', str(row))[0].strip()

        race_info = {
            "grandprix": grandprix,
            "date": date,
            "winner": f"{winner_name} {winner_surname}",
            "car": car,
            "laps": laps
        }

        return race_info

    def _extract_team_info(self, row):
        position = re.findall(r'<td class="dark">(.*?)</td>', str(row))[0].strip()
        team = re.findall(r'.html">(.*?)</a>\n</td>\n', str(row))[0].strip()
        points = re.findall(r'<td class="dark bold">(.*?)</td>', str(row))[0].strip()

        team_info = {
            "position": position,
            "team": team,
            "points": points
        }

        return team_info

    def _extract_fastest_lap_info(self, row):
        grandprix = re.findall(r'<td class="width30 dark">(.*?)</td>', str(row))[0]
        driver_surname = re.findall(r'<span class="hide-for-mobile">(.*?)</span>', str(row))[0]
        team_pattern = r'<td class="width25 semi-bold uppercase">(.*?)</td>'
        team = re.findall(team_pattern, str(row))[0].strip()
        lap_time = re.findall(r'<td class="dark bold">(.*?)</td>', str(row))[0]

        fastest_lap_info = {
            "grandprix": grandprix,
            "driver": f"{driver_surname}",
            "team": team,
            "lap_time": lap_time
        }

        return fastest_lap_info

class Formula1AcademyScraper:
    """
    Class for scraping Formula 1 Academy data from the official website.
    """
    def __init__(self):
        """
        Initialize the class with the base URL for the website.
        """
        self.base_url_f1a = "https://www.f1academy.com/Standings/"

    def get_drivers_data(self, year):
        """
        Scrape the driver data for a specific year from the official Formula 1 website.

        Args:
            year: The year for which to retrieve driver data.

        Returns:
            A list of dictionaries containing driver information for each driver.
        """
        if year != 2023:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1a}Driver?seasonId=1"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        drivers_data = []

        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("tr")[1:]:
                driver_info = self._extract_driver_info(row)
                drivers_data.append(driver_info)

        return drivers_data

    def get_races_data(self, year):
        """
        Scrape the race data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing race information for each race.
        """
        if year != 2023:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1a}Driver?seasonId=1"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        races_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("th")[2:]:
                race_info = self._extract_race_info(row, year)
                races_data.append(race_info)

        return races_data

    def get_teams_data(self, year):
        """
        Scrape the team data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing team information for each team.
        """
        if year != 2023:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f1a}Team?seasonId=1"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        teams_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("tr")[1:]:
                team_info = self._extract_team_info(row)
                teams_data.append(team_info)

        return teams_data

    def _extract_driver_info(self, row):
        position = re.findall(r'<div class="pos">(.*?)</div>', str(row))[0].strip()
        driver_name_pattern = r'<span class="visible-desktop-up">(.*?)</span>'
        driver_name = re.findall(driver_name_pattern, str(row))[0].strip()
        points = re.findall(r'<div class="total-points">(.*?)</div>', str(row))[0].strip()

        driver_info = {
            "position": position,
            "name": driver_name, 
            "points": points
        }

        return driver_info

    def _extract_race_info(self, row, year):
        grandprix_pattern = r'<div class="country-name"><span>(.*?)</span></div>'
        grandprix = re.findall(grandprix_pattern, str(row))[0].strip()
        date = re.findall(r'<div class="dates">(.*?)</div>', str(row))[0].strip()

        race_info = {
            "grandprix": grandprix,
            "date": f'{date} {year}'
        }

        return race_info

    def _extract_team_info(self, row):
        position = re.findall(r'<div class="pos">(.*?)</div>', str(row))[0].strip()
        team = re.findall(r'<span class="visible-desktop-up">(.*?)</span>', str(row))[0].strip()
        points = re.findall(r'<div class="total-points">(.*?)</div>', str(row))[0].strip()

        team_info = {
            "position": position,
            "team": team,
            "points": points
        }

        return team_info

class Formula2Scraper:
    """
    Class for scraping Formula 2 data from the official website.
    """
    def __init__(self):
        """
        Initialize the class with the base URL for the website.
        """
        self.base_url_f2 = "https://www.fiaformula2.com/Standings/"

    def get_drivers_data(self, year):
        """
        Scrape the driver data for a specific year from the official Formula 1 website.

        Args:
            year: The year for which to retrieve driver data.

        Returns:
            A list of dictionaries containing driver information for each driver.
        """
        if year < 2017:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f2}Driver?seasonId={year-1843}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        drivers_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("tr")[1:]:
                driver_info = self._extract_driver_info(row)
                drivers_data.append(driver_info)

        return drivers_data

    def get_races_data(self, year):
        """
        Scrape the race data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing race information for each race.
        """
        if year < 2017:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f2}Driver?seasonId={year-1843}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        races_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("th")[2:]:
                race_info = self._extract_race_info(row, year)
                races_data.append(race_info)

        return races_data

    def get_teams_data(self, year):
        """
        Scrape the team data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing team information for each team.
        """
        if year < 2017:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f2}Team?seasonId={year-1843}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        teams_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("tr")[1:]:
                team_info = self._extract_team_info(row)
                teams_data.append(team_info)

        return teams_data

    def _extract_driver_info(self, row):
        position = re.findall(r'<div class="pos">(.*?)</div>', str(row))[0].strip()
        driver_name_pattern = r'<span class="visible-desktop-up">(.*?)</span>'
        driver_name = re.findall(driver_name_pattern, str(row))[0].strip()
        points = re.findall(r'<div class="total-points">(.*?)</div>', str(row))[0].strip()

        driver_info = {
            "position": position,
            "name": driver_name, 
            "points": points
        }

        return driver_info

    def _extract_race_info(self, row, year):
        grandprix_pattern = r'<div class="country-name"><span>(.*?)</span></div>'
        grandprix = re.findall(grandprix_pattern, str(row))[0].strip()
        date = re.findall(r'<div class="dates">(.*?)</div>', str(row))[0].strip()

        race_info = {
            "grandprix": grandprix,
            "date": f'{date} {year}'
        }

        return race_info

    def _extract_team_info(self, row):
        position = re.findall(r'<div class="pos">(.*?)</div>', str(row))[0].strip()
        team = re.findall(r'<span class="visible-desktop-up">(.*?)</span>', str(row))[0].strip()
        points = re.findall(r'<div class="total-points">(.*?)</div>', str(row))[0].strip()

        team_info = {
            "position": position,
            "team": team,
            "points": points
        }

        return team_info

class Formula3Scraper:
    """
    Class for scraping Formula 3 data from the official website.
    """
    def __init__(self):
        """
        Initialize the class with the base URL for the website.
        """
        self.base_url_f3 = "https://www.fiaformula3.com/Standings/"

    def get_drivers_data(self, year):
        """
        Scrape the driver data for a specific year from the official Formula 1 website.

        Args:
            year: The year for which to retrieve driver data.

        Returns:
            A list of dictionaries containing driver information for each driver.
        """
        if year < 2019:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f3}Driver?seasonId={year-1843}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, features="html.parser")

        drivers_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("tr")[1:]:
                driver_info = self._extract_driver_info(row)
                drivers_data.append(driver_info)

        return drivers_data

    def get_races_data(self, year):
        """
        Scrape the race data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing race information for each race.
        """
        if year < 2019:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f3}Driver?seasonId={year-1843}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        races_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("th")[2:]:
                race_info = self._extract_race_info(row, year)
                races_data.append(race_info)

        return races_data

    def get_teams_data(self, year):
        """
        Scrape the team data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing team information for each team.
        """
        if year < 2019:
            raise ValueError(f"Invalid year: {year}")
        url = f"{self.base_url_f3}Team?seasonId={year-1843}"
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        teams_data = []
        for table in soup.find_all('table', class_='table table-bordered'):
            for row in table.find_all("tr")[1:]:
                team_info = self._extract_team_info(row)
                teams_data.append(team_info)

        return teams_data

    def _extract_driver_info(self, row):
        position = re.findall(r'<div class="pos">(.*?)</div>', str(row))[0].strip()
        driver_name_pattern = r'<span class="visible-desktop-up">(.*?)</span>'
        driver_name = re.findall(driver_name_pattern, str(row))[0].strip()
        points = re.findall(r'<div class="total-points">(.*?)</div>', str(row))[0].strip()

        driver_info = {
            "position": position,
            "name": driver_name, 
            "points": points
        }

        return driver_info

    def _extract_race_info(self, row, year):
        grandprix_pattern = r'<div class="country-name"><span>(.*?)</span></div>'
        grandprix = re.findall(grandprix_pattern, str(row))[0].strip()
        date = re.findall(r'<div class="dates">(.*?)</div>', str(row))[0].strip()

        race_info = {
            "grandprix": grandprix,
            "date": f'{date} {year}'
        }

        return race_info

    def _extract_team_info(self, row):
        position = re.findall(r'<div class="pos">(.*?)</div>', str(row))[0].strip()
        team = re.findall(r'<span class="visible-desktop-up">(.*?)</span>', str(row))[0].strip()
        points = re.findall(r'<div class="total-points">(.*?)</div>', str(row))[0].strip()

        team_info = {
            "position": position,
            "team": team,
            "points": points
        }

        return team_info

class FormulaEScraper:
    """
    Class for scraping Formula E data from the official website.
    """
    def __init__(self):
        """
        Initialize the class with the base URL for the website and seasonsId.
        """
        self.base_url_fe = "https://api.formula-e.pulselive.com/formula-e/v1/"
        self.season_ids = {
            2024: "84467676-4d5d-4c97-ae07-0b7520bb95ea",
            2023: "bc4a0209-f233-46c8-afce-842d1c48358f",
            2022: "1335d68f-d1ae-4200-8ca5-c53cd1a7690b",
            2021: "bd46d6ec-6d0e-427a-9f8c-f5a5bcc12d1c",
            2020: "0cdedbd9-d9f9-4283-ac31-828792b6b224",
            2019: "7a56ae01-e0c0-43f3-a354-47300118f7b9",
            2018: "ea980dfa-e65a-4d0a-8523-c1faa7eb6bc0",
            2017: "f59db73b-450e-4840-a5f8-2a216072b837",
            2016: "a5f3e09b-74b8-46eb-8211-7028942b6707",
            2015: "88a88a4b-a48d-4d06-9e52-d609bb7824a3",
        }

    def get_drivers_data(self, year):
        """
        Scrape the driver data for a specific year.

        Args:
            year: The year for which to retrieve driver data.

        Returns:
            A list of dictionaries containing driver information for each driver.
        """
        if year not in self.season_ids:
            raise ValueError(f"Invalid year: {year}")

        url = f"{self.base_url_fe}standings/drivers?championshipId={self.season_ids[year]}"
        response = requests.get(url, timeout=5)
        data = response.json()

        drivers_data = self._extract_driver_data(data)

        return drivers_data

    def get_teams_data(self, year):
        """
        Scrape the team data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing team information for each team.
        """

        if year not in self.season_ids:
            raise ValueError(f"Invalid year: {year}")

        url = f"{self.base_url_fe}standings/teams?championshipId={self.season_ids[year]}"
        response = requests.get(url, timeout=5)
        data = response.json()

        teams_data = [self._extract_team_data(team_data) for team_data in data]

        return teams_data

    def get_races_data(self, year):
        """
        Scrape the race data for a specific year.

        Args:
            year: The year for which to retrieve race data.

        Returns:
            A list of dictionaries containing race information for each race.
        """
        if year not in self.season_ids:
            raise ValueError(f"Invalid year: {year}")

        url = f"{self.base_url_fe}races?championshipId={self.season_ids[year]}"
        response = requests.get(url, timeout=5)
        data = response.json()["races"]

        races_data = [self._extract_race_data(race_data) for race_data in data]

        return races_data

    def _extract_driver_data(self, driver_data):
        extracted_data = []

        for driver in driver_data:
            driver_info = {
                "driverTeamName": driver["driverTeamName"],
                "driverPosition": driver["driverPosition"],
                "driverFirstName": driver["driverFirstName"],
                "driverLastName": driver["driverLastName"],
                "driverCountry": driver["driverCountry"],
                "driverPoints": driver["driverPoints"],
            }

            extracted_data.append(driver_info)

        return extracted_data

    def _extract_team_data(self, team_data):
        teams_data = {
            "teamName": team_data["teamName"],
            "teamPosition": team_data["teamPosition"],
            "teamPoints": team_data["teamPoints"],
        }

        return teams_data

    def _extract_race_data(self, race_data):
        races_data = {
            "raceName": race_data["name"],
            "raceDate": race_data["date"],
        }

        return races_data
