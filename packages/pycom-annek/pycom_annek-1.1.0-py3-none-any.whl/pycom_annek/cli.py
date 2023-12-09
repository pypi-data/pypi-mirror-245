""" Core module with cli """
import click
import os
import requests
import time
from requests_oauthlib import OAuth1
from termcolor import cprint
from pprint import pprint


@click.group()
def main():
    """
    PyCom is a CLI for the SmartCom appliance management API\n
    Set the following environment variables\n
    SC_API_URL = 'https://na4.smartcommunications.cloud'\n
    SC_CLIENT_KEY = 'OAuth1 Client Key'\n
    SC_CLIENT_SECRET = 'OAuth CLient Secret'\n
    SC_APPLIANCE = 'DevAppliance_00-50-56-95-00-00'\n

    Example Usage: pycom get-status

    """

@main.command('check-env', short_help='Check required environment variables')
def check_env():
    """ Prints out the necessary environment variables """
    sc_api_url = os.getenv('SC_API_URL')
    sc_client_key = os.getenv('SC_CLIENT_KEY')
    sc_client_secret = os.getenv('SC_CLIENT_SECRET')
    sc_appliance = os.getenv('SC_APPLIANCE')
    print(f"SC_API_URL: {sc_api_url}")
    print(f"SC_CLIENT_KEY: {sc_client_key}")
    print(f"SC_CLIENT_SECRET: {sc_client_secret}")
    print(f"SC_APPLIANCE: {sc_appliance}")


def create_request_url(base_url, appliance_id, request_endpoint):
    """ Creates the URL from variables

    Arguments:
        base_url: The base of the API endpoint
        appliance_id: The appliance ID to check
        request_endpoint: The end of the url that specifies
        request type.

    """
    request_url = (base_url + '/one/oauth1/bulkServices/api/v9/appliances/'
            + appliance_id + '/' + request_endpoint)
    return request_url


@main.command('get-appliance-status', short_help='Get Appliance Status')
def get_appliance_status():
    """ Get the appliance status """
    sc_api_url = os.getenv('SC_API_URL')
    client_key = os.getenv('SC_CLIENT_KEY')
    client_secret = os.getenv('SC_CLIENT_SECRET')
    sc_appliance = os.getenv('SC_APPLIANCE')
    sc_endpoint = 'status'
    oauth = OAuth1(client_key, client_secret=client_secret)
    requests_token_url = create_request_url(sc_api_url, sc_appliance, sc_endpoint)
    r = requests.get(url=requests_token_url, auth=oauth)
    #print(f"HTTP Response is {r}.")
    print(f"The appliance is {r.content.decode('utf-8')}")
    return r.content.decode("utf-8")


@main.command('pause-appliance', short_help='Pause the appliance')
def pause_appliance():
    """ Pause the appliance """
    sc_api_url = os.getenv('SC_API_URL')
    client_key = os.getenv('SC_CLIENT_KEY')
    client_secret = os.getenv('SC_CLIENT_SECRET')
    sc_appliance = os.getenv('SC_APPLIANCE')
    sc_endpoint = 'pause'
    oauth = OAuth1(client_key, client_secret=client_secret)
    requests_token_url = create_request_url(sc_api_url, sc_appliance, sc_endpoint)
    r = requests.post(url=requests_token_url, auth=oauth)
    sc_endpoint = 'status'
    requests_token_url = create_request_url(sc_api_url, sc_appliance, sc_endpoint)
    r = requests.get(url=requests_token_url, auth=oauth)
    checks = 0
    while r.content.decode("utf-8") != 'PAUSED':
        time.sleep(2)
        r = requests.get(url=requests_token_url, auth=oauth)
        checks += 1
        if checks >= 10:
            print("Failed to pause after 20 seconds")
            sys.exit(1)
    print("Appliance is paused")
    return r.content.decode("utf-8")


@main.command('resume-appliance', short_help='Resume the appliance')
def resume_appliance():
    """ Resume the appliance """
    sc_api_url = os.getenv('SC_API_URL')
    client_key = os.getenv('SC_CLIENT_KEY')
    client_secret = os.getenv('SC_CLIENT_SECRET')
    sc_appliance = os.getenv('SC_APPLIANCE')
    sc_endpoint = 'resume'
    oauth = OAuth1(client_key, client_secret=client_secret)
    requests_token_url = create_request_url(sc_api_url, sc_appliance, sc_endpoint)
    r = requests.post(url=requests_token_url, auth=oauth)
    sc_endpoint = 'status'
    requests_token_url = create_request_url(sc_api_url, sc_appliance, sc_endpoint)
    r = requests.get(url=requests_token_url, auth=oauth)
    checks = 0
    while r.content.decode("utf-8") != 'AVAILABLE':
        time.sleep(2)
        r = requests.get(url=requests_token_url, auth=oauth)
        checks += 1
        if checks >= 10:
            print("Failed to resume after 20 seconds")
            sys.exit(1)
    print("Appliance is available")
    return r.content.decode("utf-8")
