import logging

import json
import ast

from popcrn.ingestion.apis.twitter import Twitter
from popcrn.ingestion.tasks import import_user_tweets

from pyramid.view import view_config
from pyramid.httpexceptions import (
    HTTPOk,
    HTTPBadRequest
)

import random

from pyramid.response import Response

logger = logging.getLogger(__name__)

twitter = Twitter()

@view_config(renderer='json')
def country_sentiment(request):
    topic = request.params.get("topic")

    if not topic:
        return HTTPBadRequest("A 'topic' parameter is required to calculate map sentiment data.")

    country_list = [
        "AFG",
        "ALB",
        "ARG",
        "ARM",
        "ABW",
        "AUS",
        "AUT",
        "AZE",
        "BHS",
        "BHR",
        "BGD",
        "BRB",
        "BLR",
        "BEL",
        "BLZ",
        "BEN",
        "BMU",
        "BTN",
        "BOL",
        "BIH",
        "BWA",
        "BRA",
        "BRN",
        "BGR",
        "BFA",
        "BDI",
        "CPV",
        "KHM",
        "CMR",
        "CAN",
        "CYM",
        "CAF",
        "TCD",
        "CHI",
        "CHL",
        "CHN",
        "COL",
        "COM",
        "COD",
        "COG",
        "CRI",
        "DNK",
        "EGY",
        "SLV",
        "GNQ",
        "ERI",
        "EST",
        "ETH",
        "FRO",
        "FJI",
        "FIN",
        "FRA",
        "PYF",
        "GAB",
        "GMB",
        "GEO",
        "DEU",
        "GHA",
        "GRC",
        "GRL",
        "GRD",
        "GUM",
        "GTM",
        "GIN",
        "GNB",
        "HND",
        "IDN",
        "IRN",
        "IRQ",
        "IRL",
        "IMY",
        "ISR",
        "ITA",
        "JAM",
        "JPN",
        "JOR",
        "KAZ",
        "KEN",
        "KIR",
        "PRK",
        "KOR",
        "KSV",
        "KWT",
        "KGZ",
        "LAO",
        "LVA",
        "LBN",
        "LSO",
        "LBR",
        "MDV",
        "MLI",
        "MLT",
        "MHL",
        "MRT",
        "MUS",
        "MEX",
        "FSM",
        "MDA",
        "MCO",
        "MNG",
        "MNE",
        "MAR",
        "MOZ",
        "MMR",
        "NAM",
        "NPL",
        "OMN",
        "PAK",
        "PLW",
        "PHL",
        "POL",
        "SXM",
        "LCA",
        "THA",
        "TMP",
        "TGO",
        "TON",
        "TTO",
        "TUR",
        "TKM",
        "TCA",
        "TUV",
        "UGA",
        "UKR",
        "ARE",
        "GBR",
        "USA",
        "UZB"
    ]

    negative_range = [-2, -1, 0]
    positive_range = [1, 2, 3]
    result_list = []

    encountered = set()

    for i in xrange(30):
        country = random.choice(country_list)
        if country in encountered:
            continue
        else:
            if i % 6 == 0 and topic == "deadpool":
                result_list.append(
                    {"country": country,
                     "sentiment": random.choice(negative_range)
                     }
                )
            elif i % 4 == 0 and topic == "apple":
                result_list.append({"country": country, "sentiment": random.choice(negative_range)})
            elif i % 3 == 0 and topic == "datascience":
                result_list.append((country, random.choice(negative_range)))
            else:
                result_list.append({"country": country, "sentiment": random.choice(positive_range)})

    if "USA" not in encountered:
        result_list.append({"country": "USA", "sentiment": random.choice(positive_range)})
    return Response(json.dumps(result_list))
