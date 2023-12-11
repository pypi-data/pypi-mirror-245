import datetime
import io
import json
import os
import tempfile
import time
from urllib.parse import urljoin

import requests
from PIL import Image

API_VERSION = "v18.0"


class Client(requests.Session):
    """
    A client class for making requests to the Facebook API.

    Args:
        token (str): The access token for authenticating the requests.

    Attributes:
        token (str): The access token for authenticating the requests.
        base_url (str): The base URL for the Facebook API.

    Methods:
        request(method, url, *args, **kwargs): Sends a request to the Facebook API.
    """

    def __init__(self, token):
        super().__init__()
        self.token = token
        self.base_url = f"https://graph.facebook.com/{API_VERSION}/"
        self.headers.update({"Authorization": f"Bearer {self.token}"})

        def rate_limit(r, *args, **kwargs):
            try:
                if "x-business-use-case-usage" in r.headers:
                    data = json.loads(r.headers["x-business-use-case-usage"])
                    data_key = list(data.keys())[0]
                    time_to_regain = (
                        int(data[data_key][0]["estimated_time_to_regain_access"]) * 60
                    )
                    if time_to_regain > 0:
                        print(
                            f"Rate limit encountered, sleeping for {time_to_regain} seconds"
                        )
                        time.sleep(time_to_regain)
                    call_count = data[data_key][0]["call_count"]
                    # print(f"Call count: {call_count}")
                    if call_count > 95:
                        print(f"Approaching rate limit, sleeping for 60 seconds")
                        time.sleep(60)
                if "x-app-usage" in r.headers:
                    data = json.loads(r.headers["x-app-usage"])
                    call_count = data["call_count"]
                    # print(f"Call count: {call_count}")
                    if call_count > 95:
                        print(f"Approaching rate limit, sleeping for 60 seconds")
                        time.sleep(60)
                if "x-ad-account-usage" in r.headers:
                    data = json.loads(r.headers["x-ad-account-usage"])
                    print("X-Ad-Account-Usage:")
                    print(data)
                    util_pct = data["acc_id_util_pct"]
                    # print(f'Utilized Percentage: {util_pct}')
                    if util_pct > 95:
                        print(f"Approaching rate limit, sleeping for 60 seconds")
                        time.sleep(60)
            except Exception as e:
                print("Rate limit hook failed")
                print(f"Exception: {type(e).__name__}")
                print(f"Line: {e.__traceback__.tb_lineno}")

        self.hooks["response"].append(rate_limit)

    def request(self, method, url, *args, **kwargs):
        return super().request(method, urljoin(self.base_url, url), *args, **kwargs)


# --------------------
# Section: Accounts
# --------------------


def get_account_details(access_token, account_id):
    """
    Retrieves basic information about a Facebook Ads account.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.

    Returns:
        dict: Basic account information or error details.
    """
    client = Client(access_token)
    fields = ["id", "account_status", "balance", "currency", "spend_cap"]

    response = client.get(f"act_{account_id}", params={"fields": ",".join(fields)})
    data = response.json()

    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": response.json()}


# --------------------
# Section: Pixels
# --------------------


def get_pixel_events(access_token, pixel_id, event_name=None, since=None, until=None):
    """
    Retrieves events data for a specific Facebook Pixel.

    Args:
        access_token (str): The access token for authentication.
        pixel_id (str): The ID of the Facebook Pixel.
        event_name (str, optional): The specific event name to filter (e.g., 'PageView').
        since (str, optional): The start date of the range (YYYY-MM-DD).
        until (str, optional): The end date of the range (YYYY-MM-DD).

    Returns:
        dict: Pixel event data or error information.
    """

    params = {}

    if event_name:
        params["event_name"] = event_name
    if since and until:
        params["time_range"] = {"since": since, "until": until}
    else:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        params["time_range"] = {"since": today, "until": today}

    client = Client(access_token)
    response = client.get(f"{pixel_id}/events", params=params)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Products
# --------------------


def get_catalog_products(access_token, catalog_id, fields=None, limit=100):
    """
    Retrieves a list of products from a specific Facebook product catalog.

    Args:
        access_token (str): The access token for authentication.
        catalog_id (str): The ID of the product catalog.
        fields (list, optional): The list of fields to retrieve for each product. If None, defaults are used.
        limit (int, optional): The number of products to retrieve (default is 100).

    Returns:
        dict: Product catalog data or error information.
    """
    default_fields = [
        "id",
        "name",
        "description",
        "image_url",
        "price",
        "availability",
        "url",
    ]

    if fields is None:
        fields = default_fields

    client = Client(access_token)
    params = {"fields": ",".join(fields), "limit": limit}

    response = client.get(f"{catalog_id}/products", params=params)
    data = response.json()

    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Campaigns
# --------------------


def create_campaign(
    access_token: str, account_id: str, campaign_name: str, status: str
):
    """
    Create a campaign in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.

    Returns:
        dict: A dictionary containing the success status and data of the created campaign.
            If the campaign creation is successful, the dictionary will have the following structure:
                {"success": True, "data": campaign_data}
            If the campaign creation fails, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    campaign_data = {
        "name": campaign_name,  # Name for the campaign
        "objective": "OUTCOME_LEADS",  # Campaign objective
        "status": status,  # Initial status of the campaign
        "special_ad_categories": "NONE",  # Special ad category for the campaign
    }
    client = Client(token=access_token)
    response = client.post(f"act_{account_id}/campaigns", json=campaign_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def resume_campaign(access_token: str, account_id: str, campaign_id: str):
    """
    Resumes a paused campaign in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        campaign_id (str): The ID of the campaign to be resumed.

    Returns:
        dict: A dictionary containing the success status and data of the resumed campaign.
            If the campaign is resumed successfully, the dictionary will have the following structure:
                {"success": True, "data": campaign_data}
            If the campaign fails to resume, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    campaign_data = {"status": "ACTIVE"}
    client = Client(token=access_token)
    response = client.post(f"{campaign_id}", json=campaign_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def pause_campaign(access_token: str, account_id: str, campaign_id: str):
    """
    Pauses an active campaign in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        campaign_id (str): The ID of the campaign to be paused.

    Returns:
        dict: A dictionary containing the success status and data of the paused campaign.
            If the campaign is paused successfully, the dictionary will have the following structure:
                {"success": True, "data": campaign_data}
            If the campaign fails to pause, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    campaign_data = {"status": "PAUSED"}
    client = Client(token=access_token)
    response = client.post(f"{campaign_id}", json=campaign_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def read_campaign(access_token: str, campaign_id: str):
    """
    Retrieves all available information for a specific campaign from Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        campaign_id (str): The ID of the campaign to be read.

    Returns:
        dict: A dictionary containing the campaign data or an error message.
    """

    # Define all the fields to be retrieved
    fields = [
        "id",
        "account_id",
        "ad_strategy_id",
        "budget_rebalance_flag",
        "buying_type",
        "can_use_spend_cap",
        "configured_status",
        "created_time",
        "daily_budget",
        "effective_status",
        "is_skadnetwork_attribution",
        "issues_info",
        "last_budget_toggling_time",
        "lifetime_budget",
        "name",
        "objective",
        "recommendations",
        "source_campaign_id",
        "special_ad_categories",
        "special_ad_category_country",
        "spend_cap",
        "start_time",
        "status",
        "stop_time",
        "topline_id",
        "updated_time",
    ]

    # Make the API request
    client = Client(token=access_token)
    response = client.get(f"{campaign_id}", params={"fields": ",".join(fields)})
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Ad Sets
# --------------------


def create_ad_set(
    access_token: int | str,
    account_id: int | str,
    name: str,
    campaign_id: int | str,
    daily_budget: int | str,
    start_time: datetime.datetime,
    pixel_id: int | str,
    genders: list,
    custom_audience_id: int | str,
    age_min: int | str = 35,
    age_max: int | str = 65,
    status: str = "ACTIVE",
):
    """
    Creates a new ad set in Facebook Ads Manager.

    Parameters:
    - access_token (int|str): The access token for authentication.
    - account_id (int|str): The ID of the Facebook Ads account.
    - campaign_id (int|str): The ID of the campaign where the ad set will be placed.
    - pixel_id (int|str): The ID of the Facebook pixel associated with the ad set.
    - age_min (int): The minimum age for targeting.
    - age_max (int): The maximum age for targeting.
    - genders (list): The list of genders to target. [1] - men, [2] - women, [1,2] - men and women.
    - custom_audience_id (int|str): The ID of the custom audience to exclude.
    - creative_id (int|str): The ID of the creative to use for the ad set.

    Returns:
    - dict: A dictionary containing the success status and the response data.
    """
    ad_set_data = {
        "name": name,  # Name for the ad set
        "campaign_id": f"{campaign_id}",  # ID of the campaign where you want to place the ad set
        "daily_budget": daily_budget,  # Daily budget for the ad set in cents
        "start_time": start_time,  # Start time for the ad set
        "optimization_goal": "OFFSITE_CONVERSIONS",  # Optimization goal for the ad set
        "promoted_object": {
            "pixel_id": f"{pixel_id}",
            "custom_event_type": "LEAD",
        },  # Pixel ID for the ad set
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",  # Bid strategy for the ad set
        "billing_event": "IMPRESSIONS",  # Billing event for the ad set
        "targeting": {
            "geo_locations": {
                "countries": ["US"],
            },
            "age_min": age_min,
            "age_max": age_max,
            "genders": genders,
            "excluded_custom_audiences": [{"id": custom_audience_id}],
        },
        "status": status,  # Initial status of the ad set
    }
    client = Client(token=access_token)
    response = client.post(f"act_{account_id}/adsets", json=ad_set_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def resume_ad_set(access_token: str, account_id: str, ad_set_id: str):
    """
    Resumes a paused ad set in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        ad_set_id (str): The ID of the ad set to be resumed.

    Returns:
        dict: A dictionary containing the success status and data of the resumed ad set.
            If the ad set is resumed successfully, the dictionary will have the following structure:
                {"success": True, "data": ad_set_data}
            If the ad set fails to resume, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    ad_set_data = {"status": "ACTIVE"}
    client = Client(token=access_token)
    response = client.post(f"{ad_set_id}", json=ad_set_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def pause_ad_set(access_token: str, account_id: str, ad_set_id: str):
    """
    Pauses an active ad set in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        ad_set_id (str): The ID of the ad set to be paused.

    Returns:
        dict: A dictionary containing the success status and data of the paused ad set.
            If the ad set is paused successfully, the dictionary will have the following structure:
                {"success": True, "data": ad_set_data}
            If the ad set fails to pause, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    ad_set_data = {"status": "PAUSED"}
    client = Client(token=access_token)
    response = client.post(f"{ad_set_id}", json=ad_set_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def update_ad_set_budget(
    access_token: str, account_id: str, ad_set_id: str, daily_budget: int | str
):
    """
    Updates the daily budget of an ad set in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        ad_set_id (str): The ID of the ad set to be updated.
        daily_budget (int|str): The new daily budget for the ad set.

    Returns:
        dict: A dictionary containing the success status and data of the updated ad set.
            If the ad set is updated successfully, the dictionary will have the following structure:
                {"success": True, "data": ad_set_data}
            If the ad set fails to update, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    ad_set_data = {"daily_budget": daily_budget}
    client = Client(token=access_token)
    response = client.post(f"{ad_set_id}", json=ad_set_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def read_ad_set(access_token: str, ad_set_id: str):
    """
    Retrieves all available information for a specific ad set from Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        ad_set_id (str): The ID of the ad set to be read.

    Returns:
        dict: A dictionary containing the ad set data or an error message.
    """

    # Define all the fields to be retrieved
    fields = [
        "id",
        "account_id",
        "adlabels",
        "adset_schedule",
        "attribution_spec",
        "bid_amount",
        "bid_constraints",
        "bid_info",
        "bid_strategy",
        "billing_event",
        "budget_remaining",
        "campaign",
        "campaign_id",
        "configured_status",
        "created_time",
        "creative_sequence",
        "daily_budget",
        "daily_min_spend_target",
        "daily_spend_cap",
        "destination_type",
        "effective_status",
        "end_time",
        "frequency_control_specs",
        "full_funnel_exploration_mode",
        "is_dynamic_creative",
        "issues_info",
        "lifetime_budget",
        "lifetime_imps",
        "lifetime_min_spend_target",
        "lifetime_spend_cap",
        "name",
        "optimization_goal",
        "optimization_sub_event",
        "pacing_type",
        "promoted_object",
        "recommendations",
        "recurring_budget_semantics",
        "rf_prediction_id",
        "rtb_flag",
        "source_adset",
        "source_adset_id",
        "start_time",
        "status",
        "targeting",
        "time_based_ad_rotation_id_blocks",
        "time_based_ad_rotation_intervals",
        "updated_time",
        "use_new_app_click",
    ]

    # Make the API request
    client = Client(token=access_token)
    response = client.get(f"{ad_set_id}", params={"fields": ",".join(fields)})
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Ads
# --------------------


def create_ad(
    access_token: str, account_id: str, ad_set_id: str, name: str, creative_id: str
):
    """
    Create an ad on Facebook using the provided ad content.

    This method abstracts the details of ad creation, making it easier to create ads
    through the Facebook API. It formats the ad content as required by Facebook and
    sends the appropriate request.

    Args:
        ad_content (dict): A dictionary containing the content and configuration of the ad.

    Returns:
        Response: The response object from the Facebook API indicating the result of the ad creation request.
    """
    ad_params = {
        "name": name,
        "adset_id": ad_set_id,  # Replace with your ad set ID
        "creative": {"creative_id": creative_id},  # Replace with your creative ID
        "status": "PAUSED",  # Set the initial status of the ad
    }
    client = Client(token=access_token)
    response = client.post(f"act_{account_id}/ads", json=ad_params)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def resume_ad(access_token: str, account_id: str, ad_id: str):
    """
    Resumes a paused ad in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        ad_id (str): The ID of the ad to be resumed.

    Returns:
        dict: A dictionary containing the success status and data of the resumed ad.
            If the ad is resumed successfully, the dictionary will have the following structure:
                {"success": True, "data": ad_data}
            If the ad fails to resume, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    ad_data = {"status": "ACTIVE"}
    client = Client(token=access_token)
    response = client.post(f"{ad_id}", json=ad_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def pause_ad(access_token: str, account_id: str, ad_id: str):
    """
    Pauses an active ad in Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        ad_id (str): The ID of the ad to be paused.

    Returns:
        dict: A dictionary containing the success status and data of the paused ad.
            If the ad is paused successfully, the dictionary will have the following structure:
                {"success": True, "data": ad_data}
            If the ad fails to pause, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    ad_data = {"status": "PAUSED"}
    client = Client(token=access_token)
    response = client.post(f"{ad_id}", json=ad_data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def read_ad(access_token: str, ad_id: str):
    """
    Retrieves all available information for a specific ad from Facebook Ads Manager.

    Args:
        access_token (str): The access token for authentication.
        ad_id (str): The ID of the ad to be read.

    Returns:
        dict: A dictionary containing the ad data or an error message.
    """

    # Define all the fields to be retrieved
    fields = [
        "id",
        "account_id",
        "ad_review_feedback",
        "adlabels",
        "adset",
        "adset_id",
        "bid_amount",
        "bid_info",
        "bid_type",
        "campaign",
        "campaign_id",
        "configured_status",
        "conversion_specs",
        "created_time",
        "creative",
        "effective_status",
        "last_updated_by_app_id",
        "name",
        "recommendations",
        "source_ad",
        "source_ad_id",
        "status",
        "tracking_specs",
        "updated_time",
    ]

    # Make the API request
    client = Client(token=access_token)
    response = client.get(f"{ad_id}", params={"fields": ",".join(fields)})
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Audiences
# --------------------


def list_all_custom_audiences(access_token: str, account_id: str | int):
    """
    Retrieves all custom audiences for a given Facebook account.

    Args:
        account_id (int): The ID of the Facebook account.
        access_token (str): The access token for making API requests.

    Returns:
        dict: A dictionary containing the success status and the retrieved custom audiences.
            If the request is successful, the dictionary will have the following structure:
            {
                "success": True,
                "data": [audience1, audience2, ...]
            }
            If the request fails, the dictionary will have the following structure:
            {
                "success": False,
                "data": error_message
            }
    """
    params = {
        "fields": "id,name,subtype,description,external_event_source,pixel_id,rule,rule_aggregation"
    }
    client = Client(token=access_token)
    response = client.get(f"act_{account_id}/customaudiences", params=params)
    audiences = []
    if response.status_code != 200:
        data = response.json()
        return {"success": False, "data": data.get("error")}
    else:
        continue_paging = True
        while continue_paging:
            data = response.json()
            for item in data["data"]:
                audiences.append(item)
            try:
                data["paging"]["next"]
                response = client.get(data["paging"]["next"])
            except KeyError:
                continue_paging = False
        return {"success": True, "data": audiences}


def create_custom_audience(
    access_token: int | str,
    account_id: int | str,
    name: str,
    term: str,
    pixel_id: int | str,
    retention_seconds: int | str,
):
    """
    Creates a custom audience in Facebook Ads Manager based on website visitors who visited any URL containing the specified term.

    Args:
        account_id (int): The ID of the Facebook Ads Manager account.
        access_token (str): The access token for authentication.
        name (str): The name of the custom audience.
        term (str): The term to search for in the URL of website visitors.
        pixel_id (int): The ID of the Facebook pixel associated with the custom audience.
        retention_seconds (int): The number of seconds for which website visitors should be retained in the custom audience.

    Returns:
        dict: A dictionary containing the success status and data of the custom audience creation.
            - If the custom audience is created successfully, the dictionary will have the following structure:
                {"success": True, "data": response_data}
            - If there is an error during custom audience creation, the dictionary will have the following structure:
                {"success": False, "data": error_data}
    """
    data = {
        "name": name,
        "description": f"Website visitors who visited any URL containing the term '{term}'",
        "retention_seconds": retention_seconds,
        "pixel_id": pixel_id,
        "external_event_source": {"id": pixel_id},
        "rule": {
            "inclusions": {
                "operator": "or",
                "rules": [
                    {
                        "event_sources": [
                            {
                                "type": "pixel",
                                "id": pixel_id,
                            }
                        ],
                        "retention_seconds": retention_seconds,
                        "filter": {
                            "operator": "and",
                            "filters": [
                                {
                                    "field": "url",
                                    "operator": "i_contains",
                                    "value": term,
                                }
                            ],
                        },
                    }
                ],
            }
        },
    }
    client = Client(token=access_token)
    response = client.post(f"act_{account_id}/customaudiences", json=data)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Creatives
# --------------------


def upload_image(access_token: int, account_id: str, image_url: str):
    """
    Uploads an image to Facebook API using tempfile.

    Parameters:
    - access_token (int): The access token for authentication.
    - account_id (str): The ID of the Facebook account.
    - image_url (str): The URL of the image to be uploaded.

    Returns:
    - dict: A dictionary containing the success status and the response data.
    """
    response = requests.get(image_url)
    img = Image.open(io.BytesIO(response.content))

    # Use tempfile to create a temporary file
    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
        img.save(temp_file, format="JPEG")
        temp_file_path = temp_file.name

    # Open the temporary file for reading and make the request
    try:
        with open(temp_file_path, "rb") as file:
            files = {"file": ("image.jpg", file)}
            client = Client(token=access_token)
            response = client.post(f"act_{account_id}/adimages", files=files)

        # Read the response
        data = response.json()
        if response.status_code != 200:
            return {"success": False, "data": data.get("error")}
        else:
            return {"success": True, "data": data}
    finally:
        # Remove the temporary file after use
        os.remove(temp_file_path)


def upload_video(token, page_id, video_url, thumbnail_url):
    """
    Uploads a video to a Facebook page using the Facebook Graph API with tempfile.

    Args:
        token (str): The access token for the Facebook API.
        page_id (str): The ID of the Facebook page where the video will be uploaded.
        video_url (str): The URL of the video to be uploaded.
        thumbnail_url (str): The URL of the thumbnail image for the video.

    Returns:
        dict: A dictionary containing the upload status and response data.
    """
    img_data = requests.get(thumbnail_url).content

    # Use a temporary file for the thumbnail
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_thumb:
        temp_thumb_path = temp_thumb.name
        if thumbnail_url.endswith(".png"):
            # Convert PNG to JPEG
            with Image.open(io.BytesIO(img_data)) as img_png:
                img_rgb = img_png.convert("RGB")
                img_rgb.save(temp_thumb, format="JPEG")
        else:
            # Save the image directly
            temp_thumb.write(img_data)
            temp_thumb.flush()

    # Attempt to upload and ensure cleanup
    try:
        with open(temp_thumb_path, "rb") as file:
            files = {"thumb": ("thumbnail_image.jpg", file)}
            client = Client(token=token)
            response = client.post(
                f"/{page_id}/videos/?file_url={video_url}", files=files
            )

        data = response.json()
        if response.status_code != 200:
            return {"success": False, "data": data.get("error")}
        else:
            return {"success": True, "data": data}
    finally:
        # Remove the temporary file after use
        os.remove(temp_thumb_path)


def create_ad_creative(
    access_token: int | str,
    account_id: int | str,
    page_id: int | str,
    video_id: int | str,
    image_hash: int | str,
    primary_text: str,
    headline_text: str,
    description_text: str,
    ad_link: str,
):
    """
    Create a video creative for Facebook API.

    Args:
        access_token (str): The access token for authentication.
        account_id (int): The ID of the Facebook ad account.
        page_id (int): The ID of the Facebook page.
        video_id (str): The ID of the video.
        image_hash (str): The hash of the image associated with the video.
        primary_text (str): The primary text for the creative.
        headline_text (str): The headline text for the creative.
        description_text (str): The description text for the creative.
        ad_link (str): The link for the call-to-action button.

    Returns:
        dict: A dictionary containing the success status and data of the response.
    """
    creative_params = {
        "name": "test - Creative Name",
        "object_story_spec": {
            "page_id": page_id,
            "video_data": {
                "video_id": video_id,
                "image_hash": image_hash,
                "message": primary_text,
                "title": headline_text,
                "link_description": description_text,
                "call_to_action": {
                    "type": "LEARN_MORE",
                    "value": {"link": ad_link, "link_caption": ad_link.split("/?")[0]},
                },
            },
        },
        "degrees_of_freedom_spec": {
            "creative_features_spec": {
                "standard_enhancements": {"enroll_status": "OPT_OUT"}
            }
        },
    }
    client = Client(token=access_token)
    response = client.post(f"act_{account_id}/adcreatives", json=creative_params)
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


# --------------------
# Section: Insights
# --------------------


def get_account_insights(
    access_token, account_id, fields=None, since=None, until=None, params=None
):
    """
    Fetches insights for a specific Facebook Ads account with default fields and optional date range.
    Defaults to the current day's insights if no date range is provided.

    Args:
        access_token (str): The access token for authentication.
        account_id (str): The ID of the Facebook Ads account.
        fields (list, optional): The list of fields to retrieve. If None, defaults are used.
        since (str, optional): The start date of the range (YYYY-MM-DD).
        until (str, optional): The end date of the range (YYYY-MM-DD).
        params (dict, optional): Additional parameters for the request.

    Returns:
        dict: The insights data or error information.
    """
    default_fields = [
        "account_name",
        "impressions",
        "clicks",
        "spend",
        "reach",
        "cpc",
        "ctr",
        "cost_per_conversion",
        "cpm",
        "frequency",
    ]

    if fields is None:
        fields = default_fields
    if params is None:
        params = {}

    if since and until:
        params["time_range"] = {"since": since, "until": until}
    else:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        params["time_range"] = {"since": today, "until": today}

    client = Client(access_token)
    response = client.get(
        f"act_{account_id}/insights", params={"fields": ",".join(fields), **params}
    )
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def get_campaign_insights(
    access_token, campaign_id, fields=None, since=None, until=None, params=None
):
    """
    Fetches insights for a specific Facebook campaign with default fields and optional date range.

    Args:
        access_token (str): The access token for authentication.
        campaign_id (str): The ID of the campaign.
        fields (list, optional): The list of fields to retrieve. If None, defaults are used.
        since (str, optional): The start date of the range (YYYY-MM-DD).
        until (str, optional): The end date of the range (YYYY-MM-DD).
        params (dict, optional): Additional parameters for the request.

    Returns:
        dict: The insights data or error information.
    """
    default_fields = [
        "impressions",
        "clicks",
        "spend",
        "reach",
        "cpc",
        "ctr",
        "conversion_rate",
        "cost_per_conversion",
        "frequency",
        "cpm",
        "ad_delivery",
        "conversion_value",
    ]

    if fields is None:
        fields = default_fields
    if params is None:
        params = {}

    if since and until:
        params["time_range"] = {"since": since, "until": until}
    else:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        params["time_range"] = {"since": today, "until": today}

    client = Client(access_token)
    response = client.get(
        f"act_{campaign_id}/insights", params={"fields": ",".join(fields), **params}
    )
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def get_ad_set_insights(
    access_token, ad_set_id, fields=None, since=None, until=None, params=None
):
    """
    Fetches insights for a specific Facebook ad set with default fields and optional date range.

    Args:
        access_token (str): The access token for authentication.
        ad_set_id (str): The ID of the ad set.
        fields (list, optional): The list of fields to retrieve. If None, defaults are used.
        since (str, optional): The start date of the range (YYYY-MM-DD).
        until (str, optional): The end date of the range (YYYY-MM-DD).
        params (dict, optional): Additional parameters for the request.

    Returns:
        dict: The insights data or error information.
    """
    default_fields = [
        "impressions",
        "clicks",
        "spend",
        "reach",
        "cpc",
        "ctr",
        "conversion_rate",
        "cost_per_conversion",
        "frequency",
        "cpm",
        "ad_delivery",
        "conversion_value",
    ]

    if fields is None:
        fields = default_fields
    if params is None:
        params = {}

    if since and until:
        params["time_range"] = {"since": since, "until": until}
    else:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        params["time_range"] = {"since": today, "until": today}

    client = Client(access_token)
    response = client.get(
        f"{ad_set_id}/insights", params={"fields": ",".join(fields), **params}
    )
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}


def get_ad_insights(
    access_token, ad_id, fields=None, since=None, until=None, params=None
):
    """
    Fetches insights for a specific Facebook ad with default fields and optional date range.
    Defaults to the current day's insights if no date range is provided.

    Args:
        access_token (str): The access token for authentication.
        ad_id (str): The ID of the ad.
        fields (list, optional): The list of fields to retrieve. If None, defaults are used.
        since (str, optional): The start date of the range (YYYY-MM-DD).
        until (str, optional): The end date of the range (YYYY-MM-DD).
        params (dict, optional): Additional parameters for the request.

    Returns:
        dict: The insights data or error information.
    """
    default_fields = [
        "impressions",
        "clicks",
        "spend",
        "reach",
        "cpc",
        "ctr",
        "conversion_rate",
        "cost_per_conversion",
        "frequency",
        "cpm",
        "ad_delivery",
        "video_views",
        "engagement_rate",
        "quality_ranking",
        "conversion_value",
    ]

    if fields is None:
        fields = default_fields
    if params is None:
        params = {}

    if since and until:
        params["time_range"] = {"since": since, "until": until}
    else:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        params["time_range"] = {"since": today, "until": today}

    client = Client(access_token)
    response = client.get(
        f"{ad_id}/insights", params={"fields": ",".join(fields), **params}
    )
    data = response.json()
    if response.status_code != 200:
        return {"success": False, "data": data.get("error")}
    else:
        return {"success": True, "data": data}
