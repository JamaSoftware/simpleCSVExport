
# Jama Software
Jama Software is the definitive system of record and action for product development. The company’s modern requirements and test management solution helps enterprises accelerate development time, mitigate risk, slash complexity and verify regulatory compliance. More than 600 product-centric organizations, including NASA, Boeing and Caterpillar use Jama to modernize their process for bringing complex products to market. The venture-backed company is headquartered in Portland, Oregon. For more information, visit [jamasoftware.com](http://jamasoftware.com).

Please visit [dev.jamasoftware.com](http://dev.jamasoftware.com) for additional resources and join the discussion in our community [community.jamasoftware.com](http://community.jamasoftware.com).

## Simple CSV Exporter
```verifier.py``` is a script which exports all project information, items for each item type, project relationships, and project comments to csv files for a given Jama instance using the Jama REST API.  

Please note that this script is distrubuted as-is as an example and will likely require modification to work for your specific use-case.  This example omits error checking. Jama Support will not assist with the use or modification of the script.

### Before you begin
- Install Python 2.7 or higher and the requests library.  [Python](https://www.python.org/) and [Requests](http://docs.python-requests.org/en/latest/)

### Setup
1. As always, set up a test environment and project to test the script.

2. Fill out the CONFIG section of the script.  The necessary fields are:
  - ```username```
  - ```password```
  - ```base_url```
