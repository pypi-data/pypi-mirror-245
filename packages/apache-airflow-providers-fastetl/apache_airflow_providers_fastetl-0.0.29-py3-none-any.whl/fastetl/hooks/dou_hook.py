"""
print('PESQUISA COM RETRY')
Hook para realizar operações de consultas à API do Diário Oficial da União.
"""
import logging
from datetime import datetime, timedelta
import time
from enum import Enum
import json
from typing import List
import requests

from airflow.hooks.base import BaseHook

from bs4 import BeautifulSoup


class Section(Enum):
    """Define the section options to be used as parameter in the search"""

    SECAO_1 = "do1"
    SECAO_2 = "do2"
    SECAO_3 = "do3"
    EDICAO_EXTRA = "doe"
    EDICAO_EXTRA_1A = "do1_extra_a"
    EDICAO_EXTRA_1B = "do1_extra_b"
    EDICAO_EXTRA_1D = "do1_extra_d"
    EDICAO_EXTRA_2A = "do2_extra_a"
    EDICAO_EXTRA_2B = "do2_extra_b"
    EDICAO_EXTRA_2D = "do2_extra_d"
    EDICAO_EXTRA_3A = "do3_extra_a"
    EDICAO_EXTRA_3B = "do3_extra_b"
    EDICAO_EXTRA_3D = "do3_extra_d"
    EDICAO_SUPLEMENTAR = "do1a"
    TODOS = "todos"


class SearchDate(Enum):
    """Define the search date options to be used as parameter in the search"""

    DIA = "dia"
    SEMANA = "semana"
    MES = "mes"
    ANO = "ano"


class Field(Enum):
    """Define the search field options to be used as parameter in the search"""

    TUDO = "tudo"
    TITULO = "title_pt_BR"
    CONTEUDO = "ddm__text__21040__texto_pt_BR"


class DOUHook(BaseHook):
    IN_WEB_BASE_URL = "https://www.in.gov.br/web/dou/-/"
    IN_API_BASE_URL = "https://www.in.gov.br/consulta/-/buscar/dou"
    SEC_DESCRIPTION = {
        Section.SECAO_1.value: "Seção 1",
        Section.SECAO_2.value: "Seção 2",
        Section.SECAO_3.value: "Seção 3",
        Section.EDICAO_EXTRA.value: "Edição Extra",
        Section.EDICAO_EXTRA_1A.value: "Seção: 1 - Extra A",
        Section.EDICAO_EXTRA_1B.value: "Seção: 1 - Extra B",
        Section.EDICAO_EXTRA_1D.value: "Seção: 1 - Extra D",
        Section.EDICAO_EXTRA_2A.value: "Seção: 2 - Extra A",
        Section.EDICAO_EXTRA_2B.value: "Seção: 2 - Extra B",
        Section.EDICAO_EXTRA_2D.value: "Seção: 2 - Extra D",
        Section.EDICAO_EXTRA_3A.value: "Seção: 3 - Extra A",
        Section.EDICAO_EXTRA_3B.value: "Seção: 3 - Extra B",
        Section.EDICAO_EXTRA_3D.value: "Seção: 3 - Extra D",
        Section.EDICAO_SUPLEMENTAR.value: "Edição Suplementar",
        Section.TODOS.value: "Todas",
    }

    def __init__(self, *args, **kwargs):
        pass

    def _get_query_str(self, term, field, is_exact_search):
        """
        Adiciona aspas duplas no inicio e no fim de cada termo para o
        caso de eles serem formados por mais de uma palavra
        """
        if is_exact_search:
            term = f'"{term}"'

        if field == Field.TUDO:
            return term
        else:
            return f"{field.value}-{term}"

    def calculate_from_datetime(
        self, publish_to_date: datetime, search_date: SearchDate
    ):
        """
        Calculate parameter `publishFrom` to be passed to the API based
        on publishTo parameter and `search_date`. Perform especial
        calculation to the MES (month) parameter option
        """
        if search_date == SearchDate.DIA:
            return publish_to_date

        elif search_date == SearchDate.SEMANA:
            return publish_to_date - timedelta(days=6)

        elif search_date == SearchDate.MES:
            end_prev_month = publish_to_date.replace(day=1) - timedelta(days=1)
            publish_from_date = end_prev_month.replace(day=publish_to_date.day)
            return publish_from_date - timedelta(days=1)

        elif search_date == SearchDate.ANO:
            return publish_to_date - timedelta(days=364)

    def _request_page(self, with_retry: bool, payload: dict):
        try:
            return requests.get(self.IN_API_BASE_URL, params=payload, timeout=10)
        except requests.exceptions.ConnectionError:
            if with_retry:
                logging.info("Sleep for 30 seconds before retry requests.get().")
                time.sleep(30)
                return requests.get(self.IN_API_BASE_URL, params=payload, timeout=10)   


    def search_text(
        self,
        search_term: str,
        sections: List[Section],
        reference_date: datetime = datetime.now(),
        search_date=SearchDate.DIA,
        field=Field.TUDO,
        is_exact_search=True,
        with_retry=True,
    ):
        """
        Search for a term in the API and return all ocurrences.

        Args:
            - search_term: The term to perform the search with.
            - section: The Journal section to perform the search on.

        Return:
            - A list of dicts of structred results.
        """

        publish_from = self.calculate_from_datetime(reference_date, search_date)

        payload = {
            "q": self._get_query_str(search_term, field, is_exact_search),
            "exactDate": "personalizado",
            "publishFrom": publish_from.strftime("%d-%m-%Y"),
            "publishTo": reference_date.strftime("%d-%m-%Y"),
            "sortType": "0",    
            "s": [section.value for section in sections]
        }
        page = self._request_page(payload=payload, with_retry=with_retry)

        soup = BeautifulSoup(page.content, "html.parser")
        
        # Checks if there is more than one page of results
        pagination_tag = soup.find(
            'button', id='lastPage'
        )
        
        if (pagination_tag) is not None:
            # Get the number of pages in the pagination bar
            number_pages = int(pagination_tag.text.strip())
        else:
            # If is a single page
            number_pages = 1

        logging.info("Total pages: %s", number_pages)

        all_results = []

        # Loop for each page of result
        for page_num in range(number_pages):
            logging.info("Searching in page %s", str(page_num + 1))
            
            # If there is more than one page add extra payload params and reload the page
            if page_num > 0:
                # The id is needed for pagination to work because it requires
                # passing the last id from the previous item page in request URL          
                # Delta is the number of records per page. By now is restricted up to 20.
                payload.update({
                    "id": item["id"],
                    "displayDate": item["display_date_sortable"],
                    # "delta": 20,
                    "newPage": page_num + 1,
                    "currentPage": page_num,
                })
                page = self._request_page(payload=payload, with_retry=with_retry)
                soup = BeautifulSoup(page.content, "html.parser")            

            script_tag = soup.find(
                "script", id="_br_com_seatecnologia_in_buscadou_BuscaDouPortlet_params"
            )   
            search_results = json.loads(script_tag.contents[0])["jsonArray"]

            if search_results:
                for content in search_results:
                    item = {}
                    item["section"] = content["pubName"].lower()
                    item["title"] = content["title"]
                    item["href"] = self.IN_WEB_BASE_URL + content["urlTitle"]
                    item["abstract"] = content["content"]
                    item["date"] = content["pubDate"]
                    item["id"] = content["classPK"]
                    item["display_date_sortable"] = content["displayDateSortable"]

                    all_results.append(item)

        return all_results
