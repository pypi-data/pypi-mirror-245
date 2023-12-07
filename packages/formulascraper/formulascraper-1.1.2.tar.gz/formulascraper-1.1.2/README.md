# formulascraper #

**What is this?**

This Python library allows you to extract data from various Formula racing websites effortlessly. Get driver standings, race results, team rankings, and fastest laps for Formula 1, F1 Academy, Formula 2, and Formula 3.

**Categories:**

- Drivers Standings (drivers)
- Race Results (races)
- Teams Standing (teams)
- Fastest Laps Results (fastest_laps)


**Data Availability:**

- Formula 1: All categories since 1950 (Teams Standings since 1958)
- Formula 1 Academy: All categories since 2023 (expect fastest_laps)
- Formula 2: All categories since 2017 (expect fastest_laps)
- Formula 3: All categories since 2019 (expect fastest_laps)

## Quickstart ##

**Install**:

	pip install formulascraper

**Import**:

	from formulascraper import Formula1Scraper, get_drivers_data

----------

**Extract Data:**

 Formula 1 data:

	scraper = Formula1Scraper()
	drivers_data = scraper.get_drivers_data(2021)

 Formula 1 Academy data:

	academy_scraper = Formula1AcademyScraper()
	races_data = academy_scraper.get_races_data(2023)

 Formula 2 data:

	f2_scraper = Formula2Scraper()
	teams_data = f2_scraper.get_teams_data(2012)

 Formula 3 data:

	f3_scraper = Formula3Scraper()
	fastest_laps = f3_scraper.get_fastest_laps_data(2021)

----------

**Documentation:**

Classes and Functions:

- Formula1Scraper: `get_drivers_data`, `get_races_data`, `get_teams_data`, `get_fastest_laps_data`

- Formula1AcademyScraper: `get_drivers_data`, `get_races_data`, `get_teams_data`

- Formula2Scraper: `get_drivers_data`, `get_races_data`, `get_teams_data`

- Formula3Scraper: `get_drivers_data`, `get_races_data`, `get_teams_data`


----------

Author:

ryazhenkofc (GitHub profile: https://github.com/ryazhenkofc)

----------

Additional Resources:

-   Formula 1 Website: [https://www.formula1.com]
-   Formula 1 Academy Website: [https://www.f1academy.com]
-   Formula 2 Website: [https://www.fiaformula2.com]
-   Formula 3 Website: [https://www.fiaformula3.com]

----------
### Version Updates

1.1.2 version update

-small fixes
-added docstrings

1.1.1 version update

-updated tests
-new categories (Formula 1 Academy, Formula 2, Formula 3)
-updated README.md

1.0.1 version update (Release)

-test samples
-Formula 1 scraping


