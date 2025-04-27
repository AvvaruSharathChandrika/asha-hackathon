from elasticsearch import Elasticsearch
from typing import List, Dict, Any
import os

# Connect to Elasticsearch (update credentials or host if needed)
es = Elasticsearch("http://localhost:9200")

# Define the index name
ES_INDEX = "job-index-v1"

from typing import Dict, Any, List

# Function 1: Build Elasticsearch query
def elastic_query(location: str = "", experience: str = "", role: str = "") -> Dict[str, Any]:
    must_clauses = []

    if location:
        must_clauses.append({
            "term": {
                "job_location.keyword": location
            }
        })
    if experience:
        must_clauses.append({
            "term": {
                "experience_required.keyword": experience
            }
        })
    if role:
        must_clauses.append({
            "multi_match": {
                "query": role,
                "fields": ["title", "title.keyword", "description", "description.keyword"],
                "type": "best_fields"
            }
        })

    if not must_clauses:
        must_clauses.append({"match_all": {}})

    return {
        "query": {
            "bool": {
                "must": must_clauses
            }
        }
    }

# Function 2: OR search across fields if free-text fallback
def or_search_query(keyword: str) -> Dict[str, Any]:
    return {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["title", "title.keyword", "description", "description.keyword", "job_location", "job_location.keyword", "experience_required", "experience_required.keyword"],
                "type": "best_fields"
            }
        }
    }

# Function 3: Get data from Elasticsearch
def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
    try:
        response = es.search(
            index=ES_INDEX,
            body=query_body,
            size=size,
            request_timeout=60
        )
        hits = response["hits"]["hits"]
        print(f"[Elasticsearch] Retrieved {len(hits)} results.")
        return [hit["_source"] for hit in hits]
    except Exception as e:
        print(f"[Elasticsearch ERROR]: {e}")
        return []

# Function 4: Format results into a friendly context
def get_context_sources(results: List[Dict[str, Any]]) -> str:
    if not results:
        return "I couldn't find any jobs matching your request at the moment."

    context = []
    for job in results:
        def extract_field(field_name, default="N/A"):
            val = job.get(field_name, default)
            if isinstance(val, list):
                return val[0] if val else default
            return val

        title = extract_field("title", "No Title")
        location = extract_field("job_location", "Unknown Location")
        experience = extract_field("experience_required", "N/A")
        salary = extract_field("salary_offered", "Not disclosed")
        description = extract_field("description", "No Description")

        job_info = (
            f"**Job Title:** {title.strip()}\n"
            f"**Location:** {location.strip()}\n"
            f"**Experience Required:** {experience.strip()}\n"
            f"**Salary Offered:** {salary.strip()}\n"
            f"**Description:** {description.strip()}\n"
            + "-"*30
        )
        context.append(job_info)

    return "\n\n".join(context)
