from freelancersdk.session import Session
from freelancersdk.resources.projects import search_projects, get_project_by_id, place_project_bid
from freelancersdk.resources.projects.exceptions import \
    ProjectsNotFoundException
from freelancersdk.resources.projects.helpers import (
    create_search_projects_filter,
    create_get_projects_user_details_object,
    create_get_projects_project_details_object,
)
from freelancersdk.resources.users \
    import get_self_user_id
from freelancersdk.exceptions import BidNotPlacedException

from dotenv import load_dotenv
import os

load_dotenv()

def _search_projects(query_str):
    url = os.environ.get('FLN_URL')
    oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
    session = Session(oauth_token=oauth_token, url=url)

    query = query_str
    search_filter = create_search_projects_filter(
        sort_field= 'time_updated',
        or_search_query= True,
        languages= 'en',
    )

    try:
        p = search_projects(
            session,
            query=query,
            # ! Hardcoded limit=10 default
            active_only=True,
            search_filter=search_filter,
        )

    except ProjectsNotFoundException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return None
    else:
        return p

def _get_project_by_id(id):
    url = os.environ.get('FLN_URL')
    oauth_token = os.environ.get('FLN_OAUTH_TOKEN')
    session = Session(oauth_token=oauth_token, url=url)

    project_id = id
    project_details = create_get_projects_project_details_object(
        full_description=True
    )
    user_details = create_get_projects_user_details_object(
        basic=True
    )

    try:
        p = get_project_by_id(session, project_id, project_details, user_details)
    except ProjectsNotFoundException as e:
        print('Error message: {}'.format(e.message))
        print('Server response: {}'.format(e.error_code))
        return None
    else:
        return p
    
def _place_project_bid(project_id, amount, proposal):

    url = os.environ.get('FLN_URL')
    oauth_token = os.environ.get('FLN_OAUTH_TOKEN')

    session = Session(oauth_token=oauth_token, url=url)
    my_user_id = get_self_user_id(session)
    bid_data = {
        'project_id': int(project_id),
        'bidder_id': int(my_user_id),
        'amount': amount,
        # !Hardcoded Period
        'period': 7,
        # !Hardcoded Milestone
        'milestone_percentage': 100,
        'description': proposal,
    }
    try:
        return place_project_bid(session, **bid_data)
    except BidNotPlacedException as e:
        # print(('Error message: %s' % e.message))
        print(('Error code: %s' % e.error_code))
        return None