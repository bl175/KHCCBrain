from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["document_number", "document_title", "originating_entity", "purpose", "policy", "scope", "responsibility", "definition", "procedure", "documentation", "reference", "criteria_header", "disease", "exposure_note", "attachment", "department", "role", "equipment", "emergency_protocol"]

PROMPTS["DEFAULT_USER_PROMPT"] = "n/a"

PROMPTS["entity_extraction"] = """---Goal---
Given a text document that is potentially relevant to this activity and a list of entity types, identify all entities of those types from the text and all relationships among the identified entities.
Use {language} as output language.

---Steps---
1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name
- entity_type: One of the following types: [{entity_types}]
- entity_description: Provide a comprehensive description of the entity's attributes and activities *based solely on the information present in the input text*. **Do not infer or hallucinate information not explicitly stated.** If the text provides insufficient information to create a comprehensive description, state "Description not available in text."
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

######################
---Examples---
######################
{examples}

#############################
---Real Data---
######################
Entity_types: [{entity_types}]
Text:
{input_text}
######################
Output:"""

PROMPTS["entity_extraction_examples"] = [
    """Example 1:

Entity_types: [document_number, document_title, originating_entity, purpose, policy, scope, responsibility, definition, procedure, documentation, reference]
Text:
'''
File Name: Employee Exposure and Post Exposure Management POLINC-20R10.pdf
Document Number: POLINC-20 (note: remove the revision number in everything (example: POLINC-20R10 -> POLINC-20))
Document Title: Sharps and Contamination Incident Report
Originating Entity: Infection Control

Content:
# I. Purpose:
To prevent and / or minimize the spread of communicable diseases among KHCC employees.
# II. Policy:
2.1 Employees exposed to any patient with suspected or proven communicable disease at KHCC shall report to the infection control program and the employee health clinic.
2.2 Any employee who gets exposed to blood or body fluids through mucosal membranes, needle or other sharp exposure, shall report in at the time of incidence (maximum within 24 hours) to the employee health clinic and be evaluated and offered standard medical care aimed at preventing or minimizing the risk of infection associated with the exposure.
# III. Scope:
This policy aims to protect all KHCC employees from getting infected with a blood borne pathogen in addition to providing the employees with post exposure standard care.
# IV. Responsibilities:
It is the responsibility of the employee health clinic physician and the infection control program to assure the delivery of the optimal care to all employees when required. It is the responsibility of the exposed employee to report the exposure if needed laboratory tests for the source of exposure will be ordered by employee health physician
# V. Definitions:
Communicable disease: Illness that is caused by an organism or micro-organism or its toxic products that can potentially be transmitted directly or indirectly from an infected person, animal or environment.
# VI. Procedure:
6.1 The employee who has been exposed to a patient with suspected or proven communicable disease must report the incident to the employee health clinic.
6.2 Exposed employees must fill out the first page of the sharp and contaminated injury report available in all nursing units/wards.
'''
################
Output:
("entity"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"document_number"{tuple_delimiter}"Unique identifier for the Employee Exposure and Post Exposure Management policy document"){record_delimiter}
("entity"{tuple_delimiter}"Sharps and Contamination Incident Report"{tuple_delimiter}"document_title"{tuple_delimiter}"Official title assigned to this exposure management report"){record_delimiter}
("entity"{tuple_delimiter}"Infection Control"{tuple_delimiter}"originating_entity"{tuple_delimiter}"Department responsible for creating and maintaining this policy document"){record_delimiter}
("entity"{tuple_delimiter}"To prevent and minimize the spread of communicable diseases among KHCC employees"{tuple_delimiter}"purpose"{tuple_delimiter}"Primary objective to safeguard KHCC employees from communicable diseases"){record_delimiter}
("entity"{tuple_delimiter}"Report exposure to infection control and employee health clinic within 24 hours"{tuple_delimiter}"policy"{tuple_delimiter}"Mandates that any employee exposed to blood or body fluids must promptly report the incident and receive standard medical care"){record_delimiter}
("entity"{tuple_delimiter}"All KHCC employees"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the range of applicability – all KHCC employees are covered under this exposure management policy"){record_delimiter}
("entity"{tuple_delimiter}"Employee health clinic physician"{tuple_delimiter}"responsibility"{tuple_delimiter}"Tasked with evaluating injured employees, providing first aid management, and coordinating follow-up care"){record_delimiter}
("entity"{tuple_delimiter}"Infection control program"{tuple_delimiter}"responsibility"{tuple_delimiter}"Responsible for assuring the delivery of optimal care and proper infection control measures following an exposure incident"){record_delimiter}
("entity"{tuple_delimiter}"Communicable disease"{tuple_delimiter}"definition"{tuple_delimiter}"An illness caused by an organism or its toxic products that can be transmitted directly or indirectly"){record_delimiter}
("entity"{tuple_delimiter}"Incident reporting and evaluation procedure"{tuple_delimiter}"procedure"{tuple_delimiter}"Multi-step process outlining how an exposure incident is managed from reporting through follow-up care"){record_delimiter}
("relationship"{tuple_delimiter}"Sharps and Contamination Incident Report"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Document title is associated with this unique document number."{tuple_delimiter}"document structure, identification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Infection Control"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Indicates the originating entity for the policy document."{tuple_delimiter}"document ownership, authority"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Employee health clinic physician"{tuple_delimiter}"Infection control program"{tuple_delimiter}"Both entities work together to ensure optimal care delivery after exposure incidents."{tuple_delimiter}"collaborative care, medical coordination"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"exposure management, infection control, employee safety, communicable disease prevention, incident reporting, healthcare policy"{completion_delimiter}
#############################""",

    """Example 2:

Entity_types: [document_number, document_title, originating_entity, criteria_header, disease, exposure_note, attachment]
Text:
'''
File Name: Criteria of exposure POLINC-20-Attach.B-R1.pdf
Document Number: POLINC-20/Attach. B
Document Title: Exposure Criteria for Communicable Diseases
Originating Entity: Infection Control

Content:
# Criteria for determining exposure to communicable diseases
Attachment no.: POLINC-20/Attach. B/R1

| Disease | Definition of exposure |
| AIDS | Parenteral or mucous membrane exposure to blood or body fluids of a patient who is HIV positive or diagnosed as having AIDS. |
| Hepatitis B and C | Documented percutaneous or mucosal exposure to infective body fluids. |
| Tuberculosis | Significant exposure to persons capable of generating aerosolized particles containing tubercle bacilli from the respiratory tract. |
'''
#############
Output:
("entity"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"document_number"{tuple_delimiter}"Unique identifier for the attachment detailing exposure criteria for communicable diseases"){record_delimiter}
("entity"{tuple_delimiter}"Exposure Criteria for Communicable Diseases"{tuple_delimiter}"document_title"{tuple_delimiter}"Title of the attachment detailing exposure criteria for communicable diseases"){record_delimiter}
("entity"{tuple_delimiter}"Infection Control"{tuple_delimiter}"originating_entity"{tuple_delimiter}"Department credited with producing the attachment content"){record_delimiter}
("entity"{tuple_delimiter}"Criteria for determining exposure to communicable diseases"{tuple_delimiter}"criteria_header"{tuple_delimiter}"Header statement that outlines the purpose of the attachment in setting exposure criteria"){record_delimiter}
("entity"{tuple_delimiter}"AIDS"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as parenteral or mucosal membrane contact with blood or body fluids from an HIV positive or AIDS patient"){record_delimiter}
("entity"{tuple_delimiter}"Hepatitis B and C"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as documented percutaneous or mucosal contact with infective body fluids"){record_delimiter}
("entity"{tuple_delimiter}"Tuberculosis"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as significant contact with persons generating aerosolized particles with tubercle bacilli"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. B/R1"{tuple_delimiter}"attachment"{tuple_delimiter}"Revision 1 of attachment B providing detailed exposure criteria for various communicable diseases"){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment is part of the main Employee Exposure and Post Exposure Management policy document."{tuple_delimiter}"document hierarchy, policy structure"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"AIDS"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'AIDS' has specific exposure criteria defined in this attachment."{tuple_delimiter}"medical criteria, disease classification"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Hepatitis B and C"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Hepatitis B and C' has specific exposure criteria defined in this attachment."{tuple_delimiter}"medical criteria, disease classification"{tuple_delimiter}8){record_delimiter}
("content_keywords"{tuple_delimiter}"communicable diseases, exposure criteria, AIDS, Hepatitis, Tuberculosis, infection control guidelines, medical assessment"{completion_delimiter}
#############################""",

    """Example 3:

Entity_types: [document_number, document_title, originating_entity, purpose, policy, scope, responsibility, definition, procedure, documentation, reference, department, role, equipment]
Text:
'''
File Name: Tracheostomy Care POLSRG-02R5.pdf
Document Number: POLSRG-02
Document Title: Tracheostomy Care
Originating Entity: Medical Department Surgery

Content:
# I. Purpose:
To ensure that all adult & pediatric patients with tracheostomy receive safe and standardized care.
# II. Policy:
2.1 Only competent registered nurses trained in tracheostomy shall perform tracheostomy care per competency checklist.
2.2 All patients with tracheostomy shall be assessed every 24 hours during hospitalization.
# III. Scope:
This policy applies to registered nurses, speech language pathologists, respiratory therapists and physicians at KHCC.
# IV. Responsibilities:
4.1 The Tracheostomy Care Specialist is responsible for provision and supervision of tracheostomy patient care.
# V. Definitions:
Tracheostomy: A surgical opening created below the Cricoid cartilage between the 2nd and 4th tracheal rings.
# VI. Procedures:
6.1 Assessment: The registered nurse shall assess the tracheostomy site every 8 hours.
6.2 Equipment: Suction set up, extra tracheostomy tube, humidification set up must be kept at bedside.
'''
#############
Output:
("entity"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"document_number"{tuple_delimiter}"Unique identifier for the Tracheostomy Care policy document"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy Care"{tuple_delimiter}"document_title"{tuple_delimiter}"Official title assigned to the tracheostomy care policy document"){record_delimiter}
("entity"{tuple_delimiter}"Medical Department Surgery"{tuple_delimiter}"originating_entity"{tuple_delimiter}"Department responsible for creating and maintaining this tracheostomy care policy"){record_delimiter}
("entity"{tuple_delimiter}"Medical Department Surgery"{tuple_delimiter}"department"{tuple_delimiter}"Surgical department within the hospital responsible for tracheostomy care policies and procedures"){record_delimiter}
("entity"{tuple_delimiter}"To ensure safe and standardized tracheostomy care for all adult and pediatric patients"{tuple_delimiter}"purpose"{tuple_delimiter}"Primary objective to provide safe and standardized tracheostomy care for both adult and pediatric patients"){record_delimiter}
("entity"{tuple_delimiter}"Only trained registered nurses perform tracheostomy care with competency verification and 24-hour patient assessment"{tuple_delimiter}"policy"{tuple_delimiter}"Mandates qualified personnel perform tracheostomy care with regular patient assessment requirements"){record_delimiter}
("entity"{tuple_delimiter}"Registered nurses, speech language pathologists, respiratory therapists, and physicians at KHCC"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the healthcare professionals subject to this tracheostomy care policy"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy Care Specialist"{tuple_delimiter}"responsibility"{tuple_delimiter}"Primary coordinator responsible for patient care supervision and oversight of tracheostomy care"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy Care Specialist"{tuple_delimiter}"role"{tuple_delimiter}"Specialized healthcare professional responsible for coordinating and supervising tracheostomy patient care"){record_delimiter}
("entity"{tuple_delimiter}"Registered Nurse"{tuple_delimiter}"role"{tuple_delimiter}"Healthcare professional responsible for direct tracheostomy care, assessment, and equipment management"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy"{tuple_delimiter}"definition"{tuple_delimiter}"A surgical opening created below the Cricoid cartilage between the 2nd and 4th tracheal rings to form a stoma"){record_delimiter}
("entity"{tuple_delimiter}"Assessment and equipment management procedures"{tuple_delimiter}"procedure"{tuple_delimiter}"Systematic procedures for tracheostomy site assessment every 8 hours and maintaining required bedside equipment"){record_delimiter}
("entity"{tuple_delimiter}"Suction set up"{tuple_delimiter}"equipment"{tuple_delimiter}"Essential suction equipment that must be maintained at the bedside for tracheostomy patient care"){record_delimiter}
("entity"{tuple_delimiter}"Extra tracheostomy tube"{tuple_delimiter}"equipment"{tuple_delimiter}"Backup tracheostomy tube required to be kept at bedside for emergency situations"){record_delimiter}
("entity"{tuple_delimiter}"Humidification set up"{tuple_delimiter}"equipment"{tuple_delimiter}"Humidification system required at bedside to maintain proper airway moisture for tracheostomy patients"){record_delimiter}
("relationship"{tuple_delimiter}"Tracheostomy Care"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Document title is associated with this unique document number."{tuple_delimiter}"document structure, identification"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Medical Department Surgery"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Indicates the originating department for the tracheostomy care policy document."{tuple_delimiter}"document ownership, departmental authority"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Tracheostomy Care Specialist"{tuple_delimiter}"Registered Nurse"{tuple_delimiter}"The specialist supervises and coordinates care provided by registered nurses for tracheostomy patients."{tuple_delimiter}"clinical supervision, care coordination"{tuple_delimiter}8){record_delimiter}
("relationship"{tuple_delimiter}"Suction set up"{tuple_delimiter}"Extra tracheostomy tube"{tuple_delimiter}"Both pieces of equipment are essential components of bedside emergency preparedness for tracheostomy care."{tuple_delimiter}"emergency preparedness, patient safety"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"tracheostomy care, patient safety, surgical procedures, respiratory care, nursing responsibilities, medical equipment, clinical supervision"{completion_delimiter}
#############################""",
]

PROMPTS[
    "summarize_entity_descriptions"
] = """You are a helpful assistant responsible for generating a comprehensive summary of the data provided below.
Given one or two entities, and a list of descriptions, all related to the same entity or group of entities.
Please concatenate all of these into a single, comprehensive description. Make sure to include information collected from all the descriptions.
If the provided descriptions are contradictory, please resolve the contradictions and provide a single, coherent summary.
Make sure it is written in third person, and include the entity names so we the have full context.
Use {language} as output language.

#######
---Data---
Entities: {entity_name}
Description List: {description_list}
#######
Output:
"""

PROMPTS["entity_continue_extraction"] = """
MANY entities and relationships were missed in the last extraction. Please find only the missing entities and relationships from previous text.

---Remember Steps---

1. Identify all entities. For each identified entity, extract the following information:
- entity_name: Name of the entity, use same language as input text. If English, capitalized the name
- entity_type: One of the following types: [{entity_types}]
- entity_description: Provide a comprehensive description of the entity's attributes and activities *based solely on the information present in the input text*. **Do not infer or hallucinate information not explicitly stated.** If the text provides insufficient information to create a comprehensive description, state "Description not available in text."
Format each entity as ("entity"{tuple_delimiter}<entity_name>{tuple_delimiter}<entity_type>{tuple_delimiter}<entity_description>)

2. From the entities identified in step 1, identify all pairs of (source_entity, target_entity) that are *clearly related* to each other.
For each pair of related entities, extract the following information:
- source_entity: name of the source entity, as identified in step 1
- target_entity: name of the target entity, as identified in step 1
- relationship_description: explanation as to why you think the source entity and the target entity are related to each other
- relationship_strength: a numeric score indicating strength of the relationship between the source entity and target entity
- relationship_keywords: one or more high-level key words that summarize the overarching nature of the relationship, focusing on concepts or themes rather than specific details
Format each relationship as ("relationship"{tuple_delimiter}<source_entity>{tuple_delimiter}<target_entity>{tuple_delimiter}<relationship_description>{tuple_delimiter}<relationship_keywords>{tuple_delimiter}<relationship_strength>)

3. Identify high-level key words that summarize the main concepts, themes, or topics of the entire text. These should capture the overarching ideas present in the document.
Format the content-level key words as ("content_keywords"{tuple_delimiter}<high_level_keywords>)

4. Return output in {language} as a single list of all the entities and relationships identified in steps 1 and 2. Use **{record_delimiter}** as the list delimiter.

5. When finished, output {completion_delimiter}

---Output---

Add new entities and relations below using the same format, and do not include entities and relations that have been previously extracted. :\n
""".strip()

PROMPTS["entity_if_loop_extraction"] = """
---Goal---'

It appears some entities may have still been missed.

---Output---

Answer ONLY by `YES` OR `NO` if there are still entities that need to be added.
""".strip()

PROMPTS["fail_response"] = (
    "Sorry, I'm not able to provide an answer to that question.[no-context]"
)

PROMPTS["rag_response"] = """---Role---

You are a helpful assistant responding to user query about Knowledge Graph and Document Chunks provided in JSON format below.


---Goal---

Generate a concise response based on Knowledge Base and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Knowledge Base, and incorporating general knowledge relevant to the Knowledge Base. Do not include information not provided by Knowledge Base.

When handling relationships with timestamps:
1. Each relationship has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting relationships, consider both the semantic content and the timestamp
3. Don't automatically prefer the most recently created relationships - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Knowledge Graph and Document Chunks---
{context_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating whether each source is from Knowledge Graph (KG) or Document Chunks (DC), and include the file path if available, in the following format: [KG/DC] file_path
- If you don't know the answer, just say so.
- Do not make anything up. Do not include information not provided by the Knowledge Base.
- Additional user prompt: {user_prompt}

Response:"""

PROMPTS["keywords_extraction"] = """---Role---

You are a helpful assistant tasked with identifying both high-level and low-level keywords in the user's query and conversation history.

---Goal---

Given the query and conversation history, list both high-level and low-level keywords. High-level keywords focus on overarching concepts or themes, while low-level keywords focus on specific entities, details, or concrete terms.

---Instructions---

- Consider both the current query and relevant conversation history when extracting keywords
- Output the keywords in JSON format, it will be parsed by a JSON parser, do not add any extra content in output
- The JSON should have two keys:
  - "high_level_keywords" for overarching concepts or themes
  - "low_level_keywords" for specific entities or details

######################
---Examples---
######################
{examples}

######################
---Real Data---
######################
Conversation History:
{history}

Current Query: {query}
######################
The `Output` should be in JSON format, with no other text before and after the JSON. Use the same language as `Current Query`.

Output:
"""

PROMPTS["keywords_extraction_examples"] = [
    """Example 1:

Query: "What are the infection control procedures for handling blood exposure incidents?"

Output:
{
  "high_level_keywords": ["Infection control procedures", "Blood exposure management", "Healthcare safety protocols"],
  "low_level_keywords": ["Blood exposure", "Post-exposure prophylaxis", "Incident reporting", "Employee health clinic", "Sharps injury"]
}

""",
    """Example 2:

Query: "Who is responsible for tracheostomy care assessment and what equipment is required?"

Output:
{
  "high_level_keywords": ["Tracheostomy care responsibilities", "Medical equipment requirements", "Clinical assessment protocols"],
  "low_level_keywords": ["Tracheostomy Care Specialist", "Registered nurse", "Suction equipment", "Humidification system", "24-hour assessment"]
}

""",
    """Example 3:

Query: "What are the exposure criteria for communicable diseases like AIDS and Hepatitis?"

Output:
{
  "high_level_keywords": ["Communicable disease exposure", "Medical criteria", "Disease transmission protocols"],
  "low_level_keywords": ["AIDS exposure", "Hepatitis B", "Hepatitis C", "Percutaneous exposure", "Mucosal contact", "Body fluids"]
}

""",
    """Example 4:

Query: "What documentation is required for hospital policy compliance?"

Output:
{
  "high_level_keywords": ["Hospital policy documentation", "Compliance requirements", "Medical record keeping"],
  "low_level_keywords": ["Policy numbers", "Incident reports", "Progress notes", "Competency checklists", "Patient assessment forms"]
}

""",
]

PROMPTS["naive_rag_response"] = """---Role---

You are a helpful assistant responding to user query about Document Chunks provided provided in JSON format below.

---Goal---

Generate a concise response based on Document Chunks and follow Response Rules, considering both the conversation history and the current query. Summarize all information in the provided Document Chunks, and incorporating general knowledge relevant to the Document Chunks. Do not include information not provided by Document Chunks.

When handling content with timestamps:
1. Each piece of content has a "created_at" timestamp indicating when we acquired this knowledge
2. When encountering conflicting information, consider both the content and the timestamp
3. Don't automatically prefer the most recent content - use judgment based on the context
4. For time-specific queries, prioritize temporal information in the content before considering creation timestamps

---Conversation History---
{history}

---Document Chunks(DC)---
{content_data}

---Response Rules---

- Target format and length: {response_type}
- Use markdown formatting with appropriate section headings
- Please respond in the same language as the user's question.
- Ensure the response maintains continuity with the conversation history.
- List up to 5 most important reference sources at the end under "References" section. Clearly indicating each source from Document Chunks(DC), and include the file path if available, in the following format: [DC] file_path
- If you don't know the answer, just say so.
- Do not include information not provided by the Document Chunks.
- Addtional user prompt: {user_prompt}

Response:"""

# TODO: deprecated
PROMPTS[
    "similarity_check"
] = """Please analyze the similarity between these two questions:

Question 1: {original_prompt}
Question 2: {cached_prompt}

Please evaluate whether these two questions are semantically similar, and whether the answer to Question 2 can be used to answer Question 1, provide a similarity score between 0 and 1 directly.

Similarity score criteria:
0: Completely unrelated or answer cannot be reused, including but not limited to:
   - The questions have different topics
   - The locations mentioned in the questions are different
   - The times mentioned in the questions are different
   - The specific individuals mentioned in the questions are different
   - The specific events mentioned in the questions are different
   - The background information in the questions is different
   - The key conditions in the questions are different
1: Identical and answer can be directly reused
0.5: Partially related and answer needs modification to be used
Return only a number between 0-1, without any additional content.
"""
