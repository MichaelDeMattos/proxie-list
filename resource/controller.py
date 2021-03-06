# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    controller.py                                      :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: michael.ortiz <michael.ortiz@dotpyc.com    +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2022/06/18 23:55:26 by michael.ort       #+#    #+#              #
#    Updated: 2022/06/18 23:55:38 by michael.ort      ###   ########.fr        #
#                                                                              #
# **************************************************************************** #


import requests
from bs4 import BeautifulSoup
from flask_restful import Resource
from flask import make_response, jsonify, request


class Proxie(object):
    def __init__(self, *args):
        self.url = "https://sslproxies.org/"
        self.list_proxie = []

    """ This function return page html for scrape """

    def get_page_html(self):
        try:

            page = requests.get(self.url)
            if page.status_code == 200:
                soup = BeautifulSoup(page.text, 'html.parser')
                return soup

        except Exception as error:
            print("Error: ", error)
            return {"status": 404, "error": str(error)}

    """ This function formated html and transformed in dict """

    def format_layout(self, soup, country=None):
        """ 
        Layout in 14/04/2021 
        <tr>
            <td>20.151.27.156</td>           # param: ==> hostname: {"type": "CharField", "return": "CharField"}
            <td>3128</td>                    # param: ==> port: {"type": "CharField", "return": "CharField"}
            <td>CA</td>                      # param: ==> id_country: {"type": "CharField", "return": "CharField"}
            <td class="hm">Canada</td>       # param: ==> country: {"type": "CharField", "return": "CharField"}
            <td>anonymous</td>               # param: ==> anonymity: {"type": "CharField", "return": "CharField"}
            <td class="hm">no</td>           # param: ==> google: {"type": "CharField", "return": "Boolean"}
            <td class="hx">yes</td>          # param: ==> https: {"type": "CharField", "return": "Boolean"}
            <td class="hm">1 minute ago</td> # param: ==> last_checked: {"type": "CharField", "return": "TimeStampDescription"}
        </tr>
        """
        try:

            table = soup.body.tbody.find_all(["tr"])
            self.list_proxie = []
            for tag in table:
                if tag is not [] and country.lower() == "all":

                    self.list_proxie.append({"hostname": tag.findAll("td")[0].text,
                                             "port": tag.findAll("td")[1].text,
                                             "id_country": tag.findAll("td")[2].text,
                                             "country": tag.findAll("td")[3].text,
                                             "anonymity": tag.findAll("td")[4].text,
                                             "google": tag.findAll("td")[5].text,
                                             "https": tag.findAll("td")[6].text,
                                             "last_checked": tag.findAll("td")[7].text
                                             })

                if country and tag is not [] and tag.findAll("td")[2].text.lower() == country:
                    self.list_proxie.append({"hostname": tag.findAll("td")[0].text,
                                             "port": tag.findAll("td")[1].text,
                                             "id_country": tag.findAll("td")[2].text,
                                             "country": tag.findAll("td")[3].text,
                                             "anonymity": tag.findAll("td")[4].text,
                                             "google": tag.findAll("td")[5].text,
                                             "https": tag.findAll("td")[6].text,
                                             "last_checked": tag.findAll("td")[7].text
                                             })

            if self.list_proxie == []:
                return {"return": "Servers not found"}

            else:
                return self.list_proxie

        except Exception as error:
            print("Error: ", error)
            return {"status": 404, "error": str(error)}


class ProxieAPI(Resource):
    def __init__(self, *args):
        ...

    def get(self):
        try:
            id_country = request.args.get("id_country")
            if not id_country:
                raise Exception("Id country not found!")

            page = Proxie().get_page_html()
            layout = Proxie().format_layout(page, id_country)
            return make_response(
                jsonify({
                    "response": layout,
                    "status": 200
                }), 200)

        except Exception as error:
            return make_response(
                jsonify({
                    "error": str(error)
                }), 503
            )
