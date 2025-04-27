# retriever.py

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


# from typing import Dict, Any, List

# # Function 1: Build Elasticsearch query
# def elastic_query(location: str = "", experience: str = "", role: str = "") -> Dict[str, Any]:
#     must_clauses = []

#     if location:
#         must_clauses.append({
#             "match": {
#                 "job_location": {
#                     "query": location,
#                     "operator": "and"
#                 }
#             }
#         })
#     if experience:
#         must_clauses.append({
#             "match": {"experience_required": experience}
#         })
#     if role:
#         must_clauses.append({
#             "multi_match": {
#                 "query": role,
#                 "fields": ["title", "description"],
#                 "type": "best_fields"
#             }
#         })

#     # If nothing was provided, match everything
#     if not must_clauses:
#         must_clauses.append({"match_all": {}})

#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields if free-text fallback
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "job_location", "experience_required"],
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(
#             index=ES_INDEX,
#             body=query_body,
#             size=size,
#             request_timeout=60
#         )
#         hits = response["hits"]["hits"]
#         print(f"[Elasticsearch] Retrieved {len(hits)} results.")
#         return [hit["_source"] for hit in hits]
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Format results into a friendly context
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title       = job.get("title", "No Title")
#         location    = job.get("job_location", "Unknown Location")
#         experience  = job.get("experience_required", "N/A")
#         salary      = job.get("salary_offered", "Not disclosed")
#         description = job.get("description", "No Description")

#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             + "-"*30
#         )
#         context.append(job_info)

#     return "\n\n".join(context)


# from typing import Dict, Any, List

# # Function 1: Build Elasticsearch query
# def elastic_query(location: str = "", experience: str = "", role: str = "") -> Dict[str, Any]:
#     must_clauses = []

#     # Case-insensitive match for location
#     if location:
#         must_clauses.append({
#             "match": {
#                 "job_location": {
#                     "query": location,
#                     "operator": "and"
#                 }
#             }
#         })

#     # Experience match
#     if experience:
#         must_clauses.append({
#             "match": {
#                 "experience_required": experience
#             }
#         })

#     # Role match
#     if role:
#         must_clauses.append({
#             "multi_match": {
#                 "query": role,
#                 "fields": ["title", "description"],
#                 "type": "best_fields"
#             }
#         })

#     # If no filters were passed, fallback to a general query
#     if not must_clauses:
#         must_clauses.append({"match_all": {}})

#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields if no structured intent
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "job_location", "experience_required"],
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(
#             index=ES_INDEX,
#             body=query_body,
#             size=size,
#             request_timeout=10  # Allowing 10 seconds for the query
#         )
#         hits = response["hits"]["hits"]
#         print(f"[Elasticsearch] Retrieved {len(hits)} results.")
#         return [hit["_source"] for hit in hits]
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Format results into a friendly context
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title       = job.get("title", "No Title")
#         location    = job.get("job_location", "Unknown Location")
#         experience  = job.get("experience_required", "N/A")
#         salary      = job.get("salary_offered", "Not disclosed")
#         description = job.get("description", "No Description")

#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             + "-"*30
#         )
#         context.append(job_info)

#     return "\n\n".join(context)

# # Function 1: Build Optimized Elasticsearch Query
# def elastic_query(location: str = "", experience: str = "", role: str = "") -> Dict[str, Any]:
#     must_clauses = []
#     filter_clauses = []

#     if location:
#         # Use 'term' query on 'keyword' field for exact match (fast)
#         filter_clauses.append({"term": {"job_location.keyword": location.lower()}})
    
#     if experience:
#         must_clauses.append({"match": {"experience_required": experience}})
    
#     if role:
#         must_clauses.append({
#             "multi_match": {
#                 "query": role,
#                 "fields": ["title", "description"],
#                 "type": "best_fields"
#             }
#         })

#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses,
#                 "filter": filter_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields if no intent extracted
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "job_location", "experience_required"],
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(index=ES_INDEX, body=query_body, size=size, request_timeout=30)  # Add timeout
#         hits = response["hits"]["hits"]
#         print(f"[Elasticsearch] Retrieved {len(hits)} results.")
#         results = [hit["_source"] for hit in hits]
#         return results
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Format results into a friendly context
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title = job.get("title", "No Title")
#         location = job.get("job_location", "Unknown Location")
#         description = job.get("description", "No Description")
#         experience = job.get("experience_required", "N/A")
#         salary = job.get("salary_offered", "Not disclosed")
        
#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             f"{'-'*30}"
#         )
#         context.append(job_info)

#     return "\n\n".join(context)


# from typing import Dict, Any, List

# # Function 1: Build Elasticsearch query
# def elastic_query(location: str = "", experience: str = "", role: str = "") -> Dict[str, Any]:
#     must_clauses = []

#     if location:
#         must_clauses.append({"match": {"job_location": location}})
    
#     if experience:
#         must_clauses.append({"match": {"experience_required": experience}})
    
#     if role:
#         must_clauses.append({
#             "multi_match": {
#                 "query": role,
#                 "fields": ["title", "description"],
#                 "type": "best_fields"
#             }
#         })

#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields if no intent extracted
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "job_location", "experience_required"],
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(index=ES_INDEX, body=query_body, size=size)
#         hits = response["hits"]["hits"]
#         print(f"[Elasticsearch] Retrieved {len(hits)} results.")
#         results = [hit["_source"] for hit in hits]
#         return results
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Format results into a friendly context
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title = job.get("title", "No Title")
#         location = job.get("job_location", "Unknown Location")
#         description = job.get("description", "No Description")
#         experience = job.get("experience_required", "N/A")
#         salary = job.get("salary_offered", "Not disclosed")
        
#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             f"{'-'*30}"
#         )
#         context.append(job_info)

#     return "\n\n".join(context)


# from typing import Dict, Any, List


# # Function 1: Build elasticsearch query
# def elastic_query(location: str = "", experience: str = "", role: str = "") -> Dict[str, Any]:
#     must_clauses = []

#     if location and location.lower() != "not mentioned":
#         must_clauses.append({"match": {"job_location": location}})
    
#     if experience and experience.lower() != "not mentioned":
#         must_clauses.append({"match": {"experience_required": experience}})
    
#     if role and role.lower() != "not mentioned":
#         must_clauses.append({
#             "multi_match": {
#                 "query": role,
#                 "fields": ["title", "description"],
#                 "type": "best_fields"
#             }
#         })

#     if not must_clauses:
#         must_clauses.append({"match_all": {}})  # fallback if nothing extracted

#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields (no changes needed here)
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "job_location", "experience_required"],
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(index=ES_INDEX, body=query_body, size=size)
#         hits = response["hits"]["hits"]
#         print(f"[Elasticsearch] Retrieved {len(hits)} results.")  # ✅ Now prints how many results
#         results = [hit["_source"] for hit in hits]
#         return results
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Process results into formatted string for prompt
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title = job.get("title", "No Title")
#         location = job.get("job_location", "Unknown Location")
#         description = job.get("description", "No Description")
#         experience = job.get("experience_required", "N/A")
#         salary = job.get("salary_offered", "Not disclosed")
        
#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             f"{'-'*30}"
#         )
#         context.append(job_info)

#     return "\n\n".join(context)


# # Function 1: Build elasticsearch query
# def elastic_query(location: str = "", experience: str = "") -> Dict[str, Any]:
#     must_clauses = []

#     if location:
#         must_clauses.append({"match": {"job_location": location}})
    
#     if experience:
#         must_clauses.append({"match": {"experience_required": experience}})
    
#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "job_location", "experience_required"],  # Removed 'category' from here also
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(index=ES_INDEX, body=query_body, size=size)
#         hits = response["hits"]["hits"]
#         print(f"[Elasticsearch] Retrieved {len(hits)} results.")
#         results = [hit["_source"] for hit in hits]
#         return results
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Process results into formatted string for prompt
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title = job.get("title", "No Title")
#         location = job.get("job_location", "Unknown Location")
#         description = job.get("description", "No Description")
#         experience = job.get("experience_required", "N/A")
#         salary = job.get("salary_offered", "Not disclosed")
        
#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             f"{'-'*30}"
#         )
#         context.append(job_info)

#     return "\n\n".join(context)



# # Function 1: Build elasticsearch query
# def elastic_query(location: str = "", category: str = "", experience: str = "") -> Dict[str, Any]:
#     must_clauses = []

#     if location:
#         must_clauses.append({"match": {"job_location": location}})
#     # if category:
#     #     must_clauses.append({"match": {"category": category}})
#     if experience:
#         must_clauses.append({"match": {"experience_required": experience}})

#     return {
#         "query": {
#             "bool": {
#                 "must": must_clauses
#             }
#         }
#     }

# # Function 2: OR search across fields
# def or_search_query(keyword: str) -> Dict[str, Any]:
#     return {
#         "query": {
#             "multi_match": {
#                 "query": keyword,
#                 "fields": ["title", "description", "category", "job_location", "experience_required"],
#                 "type": "best_fields"
#             }
#         }
#     }

# # Function 3: Get data from Elasticsearch
# def get_data_from_elk(query_body: Dict[str, Any], size: int = 5) -> List[Dict[str, Any]]:
#     try:
#         response = es.search(index=ES_INDEX, body=query_body, size=size)
#         hits = response["hits"]["hits"]
#         results = [hit["_source"] for hit in hits]
#         return results
#     except Exception as e:
#         print(f"Error retrieving data from Elasticsearch: {e}")
#         return []

# # Function 4: Process results into formatted string for prompt
# def get_context_sources(results: List[Dict[str, Any]]) -> str:
#     if not results:
#         return "I couldn't find any jobs matching your request at the moment."

#     context = []
#     for job in results:
#         title = job.get("title", "No Title")
#         location = job.get("job_location", "Unknown Location")
#         description = job.get("description", "No Description")
#         experience = job.get("experience_required", "N/A")
#         salary = job.get("salary_offered", "Not disclosed")
        
#         job_info = (
#             f"**Job Title:** {title}\n"
#             f"**Location:** {location}\n"
#             f"**Experience Required:** {experience}\n"
#             f"**Salary Offered:** {salary}\n"
#             f"**Description:** {description}\n"
#             f"{'-'*30}"
#         )
#         context.append(job_info)

#     return "\n\n".join(context)
