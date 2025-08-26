from __future__ import annotations
from typing import Any


PROMPTS: dict[str, Any] = {}

PROMPTS["DEFAULT_LANGUAGE"] = "English"
PROMPTS["DEFAULT_TUPLE_DELIMITER"] = "<|>"
PROMPTS["DEFAULT_RECORD_DELIMITER"] = "##"
PROMPTS["DEFAULT_COMPLETION_DELIMITER"] = "<|COMPLETE|>"

PROMPTS["DEFAULT_ENTITY_TYPES"] = ["document_number", "document_title", "originating_entity", "purpose", "policy", "scope", "responsibility", "definition", "procedure", "documentation", "reference"]

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
Originating Entity: nan nan infection contorl

Content:
# I. Purpose:
To prevent and / or minimize the spread of communicable diseases among KHCC employees.
# II. Policy:
2.1 Employees exposed to any patient with suspected or proven communicable disease at KHCC shall report to the infection control program and the employee health clinic.
2.2 Any employee who gets exposed to blood or body fluids through mucosal membranes, needle or other sharp exposure, shall report in at the time of incidence (maximum within 24 hours) to the employee health clinic and be evaluated and offered standard medical care aimed at preventing or minimizing the risk of infection associated with the exposure.
2.3 In case of weekend or after working hours, employees shall report to triage room.
# III. Scope:
This policy aims to protect all KHCC employees from getting infected with a blood borne pathogen in addition to providing the employees with post exposure standard care.
# IV. Responsibilities:
It is the responsibility of the employee health clinic physician and the infection control program to assure the delivery of the optimal care to all employees when required. It is the responsibility of the exposed employee to report the exposure if needed laboratory tests for the source of exposure will be ordered by employee health physician
# V. Definitions:
Communicable disease: Illness that is caused by an organism or micro-organism or its toxic products that can potentially be transmitted directly or indirectly from an infected person, animal or environment.
# VI. Procedure:
6.1 The employee who has been exposed to a patient with suspected or proven communicable disease must report the incident to the employee health clinic (see of communicable diseases Attachment POLINC-16/Attach. A).
6.2 Exposed employees must fill out the first page of the sharp and contaminated injury report available in all nursing units/wards (see Sharps and Contamination Incident Report attachment POLINC-20/Attach. A).
6.3 Employee health physician will fill out the second page of the incident report marked “For Doctor use only”. This copy will then be filed and relevant database updated. A reportable disease may need to be communicated to the ministry of health (MOH) as per MOH regulations.

6.4 A copy of the incidence report will be given to the infection control program office, the safety office and the social security office in case of the development of actual illness related to the exposure.
6.5 It is the responsibility of the employee health clinic physician to determine the immunization status of the exposed employee. As part of the pre-employment screening and immunization, all health care workers (new and old) will be tested (unless they provide a proof of immunity/prior testing) for hepatitis B and C, HIV, PPD, and the immune status will be determined for mumps, measles, rubella and chicken pox. A record of these results will be kept in the employee's record. Consultation with the infection control physician before employment on all positive results is required.
6.6 Employee health physician will do the initial evaluation and provide the injured with standard first aid management, including cleaning, suturing and anti-tetanus as necessary. If incident occurred after regular working hours of the clinic, such evaluation and management will take place in the triage room by the triage room physician. The employee will then visit the employee health clinic on the next working day with the above form.
6.7 The employee health physician will determine the significance of the employee’s exposure to communicable diseases according to the attached criteria (see Attachment POLINC20/Attach. B) and will consult the head of infection control program if medical treatment be required.
6.8 Employee health clinic physician, in consultation with the head of the infection control program, will order the necessary lab tests and provide the appropriate post exposure prophylaxis (PEP) according to the attachment (HBV post exposure management POLINC20-Attach.E & Management o accidental exposure to communicable diseases POLINC20-Attach. C).
6.9 Pregnant health care personnel's occupational exposure will be guided by the attached guidelines (see attachment pregnant women POLINC-20-Attach.F).
6.10 Employee health physician, in consultation with the head of infection control program, will determine the work restriction required, if needed, according to the attachment (see attachment work restrictions POLINC-20-Attach.D).
# VII. Documentation Requirements:
Copy of laboratory investigation results required by the employee health physician must be kept in the employee file in human resources department and employee health clinic.

# VIII. References:
CDC Guidance for Evaluating Health-Care Personnel for Hepatitis B Virus Protection and for Administering Post exposure Management Recommendations and Reports December 20, 2013 / 62(RR10);1-19
Occupational Management of Communicable Disease Exposure and Illness in Healthcare Workers, March 2012, For Healthcare Professionals
Chin, J. Control of Communicable Diseases Manual, $17^[mathrm[th]]$ ed. 2000. American Public Health Association, Washington, DC.
CDC Guidelines For Infection Control in Health Care Personnel, 1998, AJIC, Vol. 26, No. 3, pp. 289-354.
CDC, MMWR, "Updated U.S. Public Health Service Guidelines for the Management of Occupational Exposures to HBV, HCV and HIV and Recommendations for Post exposure Prophylaxis". June 29, 2001, Vol. 50, No. RR_11, pp. 1-53.
CDC Guidance for Evaluating Health-Care Personnel for Hepatitis B Virus Protection and for Administering Post exposure Management Recommendations and Reports December 20, 2013 / 62(RR10);1-19
Occupational Management of Communicable Disease Exposure and Illness in Healthcare Workers, March 2012, For Healthcare Professionals
'''
################
Output:
("entity"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"document_number"{tuple_delimiter}"Unique identifier for the Employee Exposure and Post Exposure Management policy document"){record_delimiter}
("entity"{tuple_delimiter}"Sharps and Contamination Incident Report"{tuple_delimiter}"document_title"{tuple_delimiter}"Official title assigned to this exposure management report"){record_delimiter}
("entity"{tuple_delimiter}"Infection Control"{tuple_delimiter}"originating_entity"{tuple_delimiter}"Stated originator of the document (the name appears to be an error)"){record_delimiter}
("entity"{tuple_delimiter}"To prevent and / or minimize the spread of communicable diseases among KHCC employees"{tuple_delimiter}"purpose"{tuple_delimiter}"Primary objective to safeguard KHCC employees from communicable diseases"){record_delimiter}
("entity"{tuple_delimiter}"Report exposure to infection control and employee health clinic within 24 hours, with off-hours reporting via triage room"{tuple_delimiter}"policy"{tuple_delimiter}"Mandates that any employee exposed to blood or body fluids must promptly report the incident and receive standard medical care"){record_delimiter}
("entity"{tuple_delimiter}"This policy aims to protect all KHCC employees from blood borne pathogens and ensures timely post exposure standard care"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the range of applicability – all KHCC employees are covered under this exposure management policy"){record_delimiter}
("entity"{tuple_delimiter}"employee health clinic physician"{tuple_delimiter}"responsibility"{tuple_delimiter}"Tasked with evaluating injured employees, providing first aid management, and coordinating follow-up care"){record_delimiter}
("entity"{tuple_delimiter}"infection control program"{tuple_delimiter}"responsibility"{tuple_delimiter}"Responsible for assuring the delivery of optimal care and proper infection control measures following an exposure incident"){record_delimiter}
("entity"{tuple_delimiter}"exposed employee"{tuple_delimiter}"responsibility"{tuple_delimiter}"Obligated to report any exposure incident promptly to trigger medical evaluation and necessary lab tests"){record_delimiter}
("entity"{tuple_delimiter}"Communicable disease"{tuple_delimiter}"definition"{tuple_delimiter}"An illness caused by an organism or its toxic products that can be transmitted directly or indirectly"){record_delimiter}
("entity"{tuple_delimiter}"6.1–6.10 steps, including incident reporting, evaluation, lab testing, post exposure prophylaxis, and work restriction determination"{tuple_delimiter}"procedure"{tuple_delimiter}"Detailed multi-step process outlining how an exposure incident is managed from reporting through follow-up care"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-16/Attach. A"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment providing detailed instructions for initial reporting of exposure incidents, outlining the steps for timely notification of the employee health clinic"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. A"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment containing the first page of the Sharp and Contamination Incident Report form, used to document initial details of sharp or contamination incidents"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment detailing the criteria for determining the significance of an exposure to communicable diseases, guiding the evaluation process by the health physician"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. C"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment outlining management protocols for accidental exposure to communicable diseases, including required follow-up actions and clinical measures"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. D"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment specifying guidelines for determining necessary work restrictions following an exposure incident"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. E"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment providing detailed guidelines for post exposure prophylaxis for hepatitis B virus (HBV), including treatment recommendations and follow-up protocols"){record_delimiter}
("entity"{tuple_delimiter}"POLINC-20/Attach. F"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment outlining specific guidelines for managing occupational exposures among pregnant healthcare personnel"){record_delimiter}("entity"{tuple_delimiter}"Laboratory investigation results maintained in the employee file (in HR and employee health clinic)"{tuple_delimiter}"documentation"{tuple_delimiter}"Specifies that lab results from exposure incidents must be documented and stored in designated employee files"){record_delimiter}
("entity"{tuple_delimiter}"CDC Guidance for Evaluating Health-Care Personnel for Hepatitis B Virus Protection and for Administering Post exposure Management Recommendations and Reports December 20, 2013 / 62(RR10);1-19"{tuple_delimiter}"reference"{tuple_delimiter}"Provides CDC guidelines for HBV protection and post exposure management"){record_delimiter}
("entity"{tuple_delimiter}"Occupational Management of Communicable Disease Exposure and Illness in Healthcare Workers, March 2012, For Healthcare Professionals"{tuple_delimiter}"reference"{tuple_delimiter}"Reference for managing occupational exposure and illness in healthcare settings"){record_delimiter}
("entity"{tuple_delimiter}"Chin, J. Control of Communicable Diseases Manual, 17th ed. 2000. American Public Health Association, Washington, DC"{tuple_delimiter}"reference"{tuple_delimiter}"Standard manual offering comprehensive control measures for communicable diseases"){record_delimiter}
("entity"{tuple_delimiter}"CDC Guidelines For Infection Control in Health Care Personnel, 1998, AJIC, Vol. 26, No. 3, pp. 289-354"{tuple_delimiter}"reference"{tuple_delimiter}"Establishes best practices for infection control in healthcare facilities"){record_delimiter}
("entity"{tuple_delimiter}"CDC, MMWR, 'Updated U.S. Public Health Service Guidelines for the Management of Occupational Exposures to HBV, HCV and HIV and Recommendations for Post exposure Prophylaxis'. June 29, 2001, Vol. 50, No. RR_11, pp. 1-53"{tuple_delimiter}"reference"{tuple_delimiter}"Guidelines for managing occupational exposures to HBV, HCV, and HIV with prophylaxis recommendations"){record_delimiter}
("relationship"{tuple_delimiter}"Sharps and Contamination Incident Report"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Document title is associated with this unique document number."{tuple_delimiter}"document_title, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Infection Control"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Indicates the originating entity for the policy document."{tuple_delimiter}"originating_entity, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"To prevent and / or minimize the spread of communicable diseases among KHCC employees"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"States the fundamental purpose of this exposure management policy."{tuple_delimiter}"purpose, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Report exposure to infection control and employee health clinic within 24 hours, with off-hours reporting via triage room"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Outlines the mandatory reporting procedure as per the policy."{tuple_delimiter}"policy, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"This policy aims to protect all KHCC employees from blood borne pathogens and ensures timely post exposure standard care"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Defines the scope and protective objectives of the policy."{tuple_delimiter}"scope, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"employee health clinic physician"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Specifies that the employee health clinic physician is responsible for evaluating injured employees, providing initial care, and coordinating follow-up management after an exposure incident."{tuple_delimiter}"responsibility, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"infection control program"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Specifies that the infection control program is responsible for ensuring the implementation of optimal care and infection control measures following an exposure incident."{tuple_delimiter}"responsibility, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"exposed employee"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Specifies that the exposed employee is responsible for promptly reporting any exposure incident, triggering further evaluation and management."{tuple_delimiter}"responsibility, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Communicable disease"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Provides the definition for a key term that underpins the policy's context."{tuple_delimiter}"definition, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"6.1–6.10 steps, including incident reporting, evaluation, lab testing, post exposure prophylaxis, and work restriction determination"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Outlines the procedural steps for managing employee exposure events."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-16/Attach. A"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment provides detailed instructions for initial reporting of exposure incidents as described in step 6.1."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. A"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment contains the first page of the Sharp and Contamination Incident Report form used to document initial exposure details in step 6.2."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment outlines the criteria for determining the significance of an exposure, guiding the evaluation process in step 6.7."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. C"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment details management protocols for accidental exposure to communicable diseases, referenced in step 6.8 alongside post exposure prophylaxis."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. D"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment specifies the guidelines for determining necessary work restrictions following an exposure, as outlined in step 6.10."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. E"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment provides detailed recommendations for post exposure prophylaxis for HBV, supplementing the protocols described in step 6.8."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. F"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment outlines specific guidelines for managing exposure incidents among pregnant healthcare personnel, as mentioned in step 6.9."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Laboratory investigation results maintained in the employee file (in HR and employee health clinic)"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Specifies the documentation requirements for recording exposure-related laboratory results."{tuple_delimiter}"documentation, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"CDC Guidance for Evaluating Health-Care Personnel for Hepatitis B Virus Protection and for Administering Post exposure Management Recommendations and Reports December 20, 2013 / 62(RR10);1-19"{tuple_delimiter}"Policy is supported by CDC guidelines for HBV protection and post exposure management."{tuple_delimiter}"policy, reference"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Occupational Management of Communicable Disease Exposure and Illness in Healthcare Workers, March 2012, For Healthcare Professionals"{tuple_delimiter}"Policy references occupational exposure management guidelines."{tuple_delimiter}"policy, reference"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"Chin, J. Control of Communicable Diseases Manual, 17th ed. 2000. American Public Health Association, Washington, DC"{tuple_delimiter}"Standard practices for communicable disease control inform this policy."{tuple_delimiter}"policy, reference"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"CDC Guidelines For Infection Control in Health Care Personnel, 1998, AJIC, Vol. 26, No. 3, pp. 289-354"{tuple_delimiter}"Infection control practices from CDC guidelines support this policy."{tuple_delimiter}"policy, reference"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"CDC, MMWR, 'Updated U.S. Public Health Service Guidelines for the Management of Occupational Exposures to HBV, HCV and HIV and Recommendations for Post exposure Prophylaxis'. June 29, 2001, Vol. 50, No. RR_11, pp. 1-53"{tuple_delimiter}"Guidelines for managing occupational exposures to blood borne pathogens underpin the policy's procedures."{tuple_delimiter}"policy, reference"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"pediatric procedures, outpatient setting, pre-procedure screening, procedure workflow, chemotherapy protocols, patient assessment, documentation requirements, consent forms, sedation monitoring, pharmacy coordination, patient education, NPO guidelines, recovery procedures"){completion_delimiter}
#############################""",
    """Example 2:

Entity_types: [document_number, document_title, originating_entity, purpose, policy, scope, responsibility, definition, procedure, documentation, reference]
Text:
'''
File Name: Criteria of exposure POLINC-20-Attach.B-R1 (2).pdf
Document Number: POLINC-20 (note: if it's an attachment, add to the document number (example: POLINC-20/Attach. B))
Document Title: Sharps and Contamination Incident Report Attachment B
Originating Entity: nan nan infection contorl

Content:
# Criteria for determining exposure to communicable diseases
Attachment no.: POLINC-20/Attach. B/R1
Effective date: 25/2/2013

| Serial # | Disease | Definition of exposure |
| --- | --- | --- |
| 1 | AIDS | Parenteral or mucous membrane exposure to blood or body fluids of a patient who is HIV positive or diagnosed as having AIDS. |
| 2 | Hepatitis A | An eligible contact should be a person who has during a period of 15 days before onset of overt symptoms or during the first few days after the development of jaundice: 1. Lived in the same household with the patient/employee. 2. Incurred known exposure to fecal material or vomitus of |
| 3 | Hepatitis B and C | Documented percutaneous or mucosal exposure to infective body fluids. |
| 4 | Herpes (acute gingivo-stomatitis) | Direct contact with the saliva of carriers. |
| 5 | Measles | Direct contact with nasal or throat secretions or airborne by droplet spread by personnel who have not had measles or immunization against measles. |
| 6 | Meningitis (meningococcal) | Direct contact with respiratory secretions from nose and throat of infected person. |
| 7 | Mumps | Airborne transmission or by droplet spread and by direct contact with saliva of an infected person by those not having mumps infection or immunization against mumps. |
| 8 | Pediculosis capitus (head lice) | Direct contact with an infected person/indirect contact with their clothing, head gear, or linen. |
| 9 | Rubella | Direct contact with nasopharyngeal secretions of infected people. |
| 10 | Scabies | Direct contact with the skin of infected persons. |
| 11 | Tuberculosis | Significant exposure to persons capable of generating aerosolized particles containing tubercle bacilli from the respiratory tract. |
| 12 | Varicella zoster (chicken pox) | Direct contact, droplet or airborne spread of vesicle fluid or secretions of the respiratory tract of chicken pox cases or of vesicle fluid of persons with herpes zoster (shingles). |
| Note: Significant exposures will be determined on an individual basis. Factors to be considered include the following: | | |
'''
#############
Output:
("entity"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"document_number"{tuple_delimiter}"Unique identifier for the Sharps and Contamination Incident Report Attachment B document"){record_delimiter}
("entity"{tuple_delimiter}"Sharps and Contamination Incident Report Attachment B"{tuple_delimiter}"document_title"{tuple_delimiter}"Title of the attachment detailing exposure criteria for communicable diseases"){record_delimiter}
("entity"{tuple_delimiter}"Infection Control"{tuple_delimiter}"originating_entity"{tuple_delimiter}"Entity credited with producing the attachment content"){record_delimiter}
("entity"{tuple_delimiter}"Criteria for determining exposure to communicable diseases"{tuple_delimiter}"criteria_header"{tuple_delimiter}"Header statement that outlines the purpose of the attachment in setting exposure criteria"){record_delimiter}
("entity"{tuple_delimiter}"AIDS"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as parenteral or mucosal membrane contact with blood or body fluids from an HIV positive or AIDS patient"){record_delimiter}
("entity"{tuple_delimiter}"Hepatitis A"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure criteria: contact within 15 days before symptoms or early jaundice, including household or known fecal/vomitus exposure"){record_delimiter}
("entity"{tuple_delimiter}"Hepatitis B and C"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as documented percutaneous or mucosal contact with infective body fluids"){record_delimiter}
("entity"{tuple_delimiter}"Herpes (acute gingivo-stomatitis)"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as direct contact with saliva of affected carriers"){record_delimiter}
("entity"{tuple_delimiter}"Measles"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as direct contact with nasal/throat secretions or airborne/droplet spread among non-immunized persons"){record_delimiter}
("entity"{tuple_delimiter}"Meningitis (meningococcal)"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as direct contact with respiratory secretions from an infected individual"){record_delimiter}
("entity"{tuple_delimiter}"Mumps"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as airborne, droplet, or direct saliva contact in persons lacking mumps immunity"){record_delimiter}
("entity"{tuple_delimiter}"Pediculosis capitus (head lice)"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as direct or indirect (via clothing/headgear/linen) contact with an infected person"){record_delimiter}
("entity"{tuple_delimiter}"Rubella"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as direct contact with nasopharyngeal secretions of infected individuals"){record_delimiter}
("entity"{tuple_delimiter}"Scabies"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as direct skin-to-skin contact with infected persons"){record_delimiter}
("entity"{tuple_delimiter}"Tuberculosis"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as significant contact with persons generating aerosolized particles with tubercle bacilli"){record_delimiter}
("entity"{tuple_delimiter}"Varicella zoster (chicken pox)"{tuple_delimiter}"disease"{tuple_delimiter}"Exposure defined as transmission via direct contact, droplets, or airborne spread of vesicle fluid/respiratory secretions associated with chicken pox or shingles"){record_delimiter}
("entity"{tuple_delimiter}"Significant exposures determined on an individual basis"{tuple_delimiter}"exposure_note"{tuple_delimiter}"Advisory note stating that exposure significance will be evaluated case by case"){record_delimiter}
("relationship"{tuple_delimiter}"Sharps and Contamination Incident Report Attachment B"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment document is linked to the overarching Employee Exposure and Post Exposure Management policy document (POLINC-20)"{tuple_delimiter}"document_title, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"POLINC-20"{tuple_delimiter}"This attachment is part of the Employee Exposure and Post Exposure Management policy document (POLINC-20)"{tuple_delimiter}"document_number, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Infection Control"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Links the originating entity of the attachment with its unique document identifier"{tuple_delimiter}"originating_entity, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Sharps and Contamination Incident Report Attachment B"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Document title entity is associated with attachment POLINC-20/Attach. B"{tuple_delimiter}"document_title, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Infection Control"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Originating entity is linked to attachment POLINC-20/Attach. B"{tuple_delimiter}"originating_entity, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Criteria for determining exposure to communicable diseases"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Criteria header is part of attachment POLINC-20/Attach. B"{tuple_delimiter}"criteria_header, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"AIDS"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'AIDS' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Hepatitis A"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Hepatitis A' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Hepatitis B and C"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Hepatitis B and C' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Herpes (acute gingivo-stomatitis)"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Herpes (acute gingivo-stomatitis)' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Measles"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Measles' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Meningitis (meningococcal)"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Meningitis (meningococcal)' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Mumps"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Mumps' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Pediculosis capitus (head lice)"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Pediculosis capitus (head lice)' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Rubella"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Rubella' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Scabies"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Scabies' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Tuberculosis"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Tuberculosis' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Varicella zoster (chicken pox)"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Disease entity 'Varicella zoster (chicken pox)' is included in attachment POLINC-20/Attach. B"{tuple_delimiter}"disease, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Significant exposures determined on an individual basis"{tuple_delimiter}"POLINC-20/Attach. B"{tuple_delimiter}"Exposure note is part of attachment POLINC-20/Attach. B"{tuple_delimiter}"exposure_note, document_number"{tuple_delimiter}9){record_delimiter}
("content_keywords"{tuple_delimiter}"AIDS, Hepatitis A, Hepatitis B and C, Herpes, Measles, Meningitis, Mumps, Pediculosis, Rubella, Scabies, Tuberculosis, Varicella zoster, exposure criteria, communicable diseases"{completion_delimiter}
#############################""",
    """Example 3:

Entity_types: [document_number, document_title, originating_entity, purpose, policy, scope, responsibility, definition, procedure, documentation, reference]
Text:
'''
File Name: Tracheostomy Care POLSRG-02R5.pdf
Document Number: POLSRG-02R5 (note: remove the revision number in everything (example: POLSRG-02R5 -> POLSRG-02))
Document Title: Tracheostomy Care
Originating Entity: Medical Department Surgery

Content:
# I. Purpose:
To ensure that all adult & pediatric patients with tracheostomy receive safe and standardized care.
# II. Policy:
2.1 Only competent registered nurses trained in tracheostomy shall perform tracheostomy care per competency checklist that is completed by clinical resource nurse and the Tracheostomy Care Specialist.
2.2 All patients with tracheostomy shall be assessed by the surgical resident and Tracheostomy Care Specialist upon admission, after tracheostomy tube insertion, when changed and every $24mathbf[hr]$ . during hospitalization, with documentation of at least once the tracheostomy care sheet.
2.3 All hospitalized patients with tracheostomy should be placed on O2 therapy (as needed).
2.4 All patients with tracheostomy should be referred to Speech-Language Pathology Services.
# III. Scope:
This policy will be applied to The Tracheostomy Care Specialist, all registered nurses, speech language pathologists (SLP), respiratory therapists (RT) and physicians at KHCC.
# IV. Responsibilities:
4.1 All the multidisciplinary team members should adhere to the policy content and apply the tracheostomy care guidelines.
4.2 It is the responsibility of the Nurse Manager to communicate this policy to the nursing staff.
4.3 The Tracheostomy Care Specialist is the responsible for provision and supervision of tracheostomy patient at KHCC in conjunction with head and neck surgeon /ENT on service.
4.4 The Tracheostomy Care Specialist, considered the clinical educator who should conduct registered nurse training about tracheostomy care at KHCC.in collaboration with nursing training center

# V. Definitions:
 Tracheostomy: A temporary or permanent surgical opening created by an incision below the Cricoid cartilage between the $2^[mathrm[nd]]$ and $4^[mathrm[th]]$ tracheal rings to make an exterior opening called the stoma.
 Tracheostomy tube: A device inserted into the trachea to maintain a patent airway, to bypass an Airway obstruction, to facilitate ventilation and for the removal of tracheal secretions.
 Suctioning: Mechanical aspiration of secretions from the airway.
# VI. Procedures:
# 6.1 Assessment:
6.1.1 The registered nurse shall assess the tracheostomy site upon admission, after A tracheostomy tube insertion, after a tracheostomy tube change, then every 8 hours. 6
6.1.2 Registered nurse shall notify the physician and The Tracheostomy Care Specialist to assess the patient according to the attached Tracheostomy Guidelines.
# 6.2 Care:
# 6.2.1 Role of Physician The physician shall:
6.2.1.1 Assess patients with tracheostomy upon admission, after tracheostomy tube insertion and after tracheostomy tube change.
6.2.1.2 Remove the tracheostomy tube sutures when indicated.
6.2.1.3 Change tracheostomy tube as indicated
6.2.1.4 Written orders that include the followings:  The Tracheostomy Care Specialist notification  Cuff status  Humidification/O2 needs  $mathrm[HOB]>30$ at all times  Nutrition/hydration & medication route Speech-Language Pathology consults

6.2.1.5 Perform the 1st tracheostomy tube change with the assistance of tracheostomy Care Specialist and Registered Nurse on the presence of the head and neck surgeon / ENT
6.2.1.6 The following items should be present on the trolley during the tracheostomy Tube change:
Correct tracheostomy tube type & size. and one size below Correct suction catheters.
 Pulse Oximetry. Sutures’ set. Lubricant.
 Gauze. Saline Scissors. Tracheostomy tie
6.2.1.7 Document the followings:
Indicate the tracheostomy type, size and specifications upon admission, post tracheostomy tube insertion and change
Respiratory status assessment every 24 hours.
# 6.2.2 Role of Registered Nurse The Registered Nurse shall:
6.2.2.1 Inform the tracheostomy care Specialist after the patient arrive to the floor from other unit.
6.2.2.2 Suction the tracheostomy tube Q 2 hours post operation first 8 hours, and every 4 hours during the patient on floor and as needed.
6.2.2.3 Check & clean the inner cannula Q 2hours post operation first 8 hours, and every 4 hours during the patient on floor for first 24 hours then as need and/or physician order.
6.2.2.4 Ensure adequate delivery of the humidified oxygen.
6.2.2.5 Provide nasal and oral hygiene every 8hrs and as needed.
6.2.2.6 Deflate the tracheostomy tube cuff per physician’s order.
6.2.2.7 Change the tracheostomy tube dressing daily, when soiled and as needed.
6.2.2.8 Change the tracheostomy tube tie every 24-48 hours and/or when soiled.

6.2.2.9 Perform oral care per basic patient hygiene policy-POLNUR -13.
6.2.2.10 Elevate head of bed 30-45 degrees at all times unless contraindicated.
# 6.2.3 Role of The Tracheostomy Care Specialist:
6.2.3.1 Considered as the primary coordinator for the care of tracheostomy patient at KHCC.
6.2.3.2 Supervise, assist and coordinate the tracheostomy patient care between the head and neck surgeon /ENT, surgical resident, registered staff nurse and speech –language pathologist.
6.2.3.3 He /she is the clinical resource and coordinator for different KHCC departments regarding tracheostomy care.
6.2.3.4 Fill out the tracheostomy sheet for tracheostomy patient at least once per admission and follow admitted tracheostomy patients during their stay in hospital.
6.2.3.5 Maintain records of tracheostomy tubes stock in coordination with storage department and do proper request for needed sizes and types of tracheostomy tubes in coordination with the head and neck surgeon /ENT.
6.2.3.6 Assure safe practice of tracheostomy care at KHCC.
6.2.3.7 After discharge home care instruction for all tracheostomy patients (Follow and educate tracheostomy patient in outpatient clinic).
# 6.2.4 Role of speech language pathologists The speech language pathologists shall:
6.2.3.1 Educate patient and family about:
Communication methods.  Swallowing precautions. Safety issues.
# 6.2.5 Role of Respiratory Therapists
6.2.5.1 In non-emergency situations:
Monitor the cuff inflation pressure every 4 hours for all ventilated patients. The RT could assist the nurse during tracheostomy tie change and emergency situations.

6.2.5.2 In case of Emergency which include the followings (Respiratory Therapists and/or Physician):
6.2.5.3 Accidental tracheostomy tube dislodgement (Expert Respiratory Therapists and/or Physician).
6.2.5.4 Respiratory distress not relieved by suctioning per policy (Respiratory Therapists and/or Physician).
# 6.3 Bedside equipment:
The registered nurse shall keep the following items at bedside:
 Suction set up. Extra tracheostomy (same size & type, a tracheostomy tube one size smaller with the same Humidification set up. Correct suction catheter size.
 Oral suction catheter.
 Obturator.
 Gauze. Normal saline.
# 6.4 In Case of Emergency:
Emergency management shall be according to the emergency tracheostomy management algorithm. ）?
6.5 For all ventilator -dependent patients, and in off- duty time call respiratory therapy team
# VII. Documentation Requirements:
Daily nursing flow sheet
Tracheostomy Care technician Note
Physician Progress note.
Interdisciplinary patient / family education note
Emergency tracheostomy management algorithm (POLSRG -02/Attach. A)
# VIII. References:
http://www.n-i.nhs.uk/mater/pubinfo/ (www.tracheostomy.org.uk) http://www.langara.bc.ca/vnc/trach.htm
# FRMQMO-03R2
Confidential Information Not to be Reproduced / Disclosed Without Prior Written Approval

AACN Procedure manual for critical care, Philadelphia, 2001-2005
American thoracic society (2004)
Association of Standardized Tracheostomy Care Protocol Implementation and
Reinforcement With the Prevention of Life-Threatening Respiratory Events JAMA Otolaryngol Head Neck Surg. doi:10.1001/jamaoto.2018.0484 Published online May 24, 2018.

| FRMQMO-03R2 |
| --- |
| ConfidentialInformation |
| Not to be Reproduced / Disclosed Without Prior Written Approval |
'''
#############
Output:
("entity"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"document_number"{tuple_delimiter}"Unique identifier for the Tracheostomy Care policy document"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy Care"{tuple_delimiter}"document_title"{tuple_delimiter}"Official title assigned to the tracheostomy care document"){record_delimiter}
("entity"{tuple_delimiter}"Medical Department Surgery"{tuple_delimiter}"originating_entity"{tuple_delimiter}"Stated originator of the document"){record_delimiter}
("entity"{tuple_delimiter}"To ensure that all adult & pediatric patients with tracheostomy receive safe and standardized care"{tuple_delimiter}"purpose"{tuple_delimiter}"Primary objective to provide safe and standardized tracheostomy care for both adult and pediatric patients"){record_delimiter}
("entity"{tuple_delimiter}"Only competent registered nurses trained in tracheostomy shall perform tracheostomy care per competency checklist; all patients with tracheostomy assessed upon admission, after tube insertion/change and every 24 hours; patients placed on oxygen therapy; and referred to Speech-Language Pathology Services"{tuple_delimiter}"policy"{tuple_delimiter}"Mandates adherence to specific tracheostomy care guidelines including qualified personnel, regular assessment, and appropriate referrals"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy Care Specialist"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the multidisciplinary team subject to the policy"){record_delimiter}
("entity"{tuple_delimiter}"registered nurses"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the multidisciplinary team subject to the policy"){record_delimiter}
("entity"{tuple_delimiter}"speech language pathologists"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the multidisciplinary team subject to the policy"){record_delimiter}
("entity"{tuple_delimiter}"respiratory therapists"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the multidisciplinary team subject to the policy"){record_delimiter}
("entity"{tuple_delimiter}"physicians"{tuple_delimiter}"scope"{tuple_delimiter}"Defines the multidisciplinary team subject to the policy"){record_delimiter}
("entity"{tuple_delimiter}"Nurse Manager"{tuple_delimiter}"responsibility"{tuple_delimiter}"Tasked with communicating the tracheostomy care policy to the nursing staff"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy Care Specialist"{tuple_delimiter}"responsibility"{tuple_delimiter}"Primary coordinator responsible for patient care supervision and nurse training in tracheostomy care"){record_delimiter}
("entity"{tuple_delimiter}"Multidisciplinary Team"{tuple_delimiter}"responsibility"{tuple_delimiter}"All team members must adhere to the tracheostomy care guidelines"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy"{tuple_delimiter}"definition"{tuple_delimiter}"A surgical opening created below the Cricoid cartilage between the 2nd and 4th tracheal rings to form a stoma"){record_delimiter}
("entity"{tuple_delimiter}"Tracheostomy tube"{tuple_delimiter}"definition"{tuple_delimiter}"A device inserted into the trachea to maintain airway patency, bypass obstructions, facilitate ventilation, and remove secretions"){record_delimiter}
("entity"{tuple_delimiter}"Suctioning"{tuple_delimiter}"definition"{tuple_delimiter}"Mechanical aspiration of secretions from the airway"){record_delimiter}
("entity"{tuple_delimiter}"6.1–6.5 steps, including assessment, multidisciplinary care roles, equipment setup, and emergency response"{tuple_delimiter}"procedure"{tuple_delimiter}"Comprehensive procedure detailing assessment, care delivery by various roles, equipment requirements, and emergency protocols for tracheostomy care"){record_delimiter}
("entity"{tuple_delimiter}"POLSRG-02/Attach. A"{tuple_delimiter}"procedure"{tuple_delimiter}"Attachment containing the emergency tracheostomy management algorithm"){record_delimiter}
("entity"{tuple_delimiter}"Daily nursing flow sheet, Tracheostomy Care technician Note, Physician Progress note, Interdisciplinary patient/family education note, Emergency tracheostomy management algorithm (POLSRG-02/Attach. A)"{tuple_delimiter}"documentation"{tuple_delimiter}"Specifies standardized documentation requirements for recording tracheostomy care details"){record_delimiter}
("entity"{tuple_delimiter}"http://www.n-i.nhs.uk/mater/pubinfo/ (www.tracheostomy.org.uk) http://www.langara.bc.ca/vnc/trach.htm"{tuple_delimiter}"reference"{tuple_delimiter}"Online resources providing tracheostomy care information"){record_delimiter}
("entity"{tuple_delimiter}"AACN Procedure manual for critical care, Philadelphia, 2001-2005"{tuple_delimiter}"reference"{tuple_delimiter}"Reference manual for critical care procedures"){record_delimiter}
("entity"{tuple_delimiter}"American thoracic society (2004)"{tuple_delimiter}"reference"{tuple_delimiter}"Guidelines from the American Thoracic Society on tracheostomy care"){record_delimiter}
("entity"{tuple_delimiter}"Association of Standardized Tracheostomy Care Protocol Implementation and Reinforcement With the Prevention of Life-Threatening Respiratory Events JAMA Otolaryngol Head Neck Surg. doi:10.1001/jamaoto.2018.0484 Published online May 24, 2018"{tuple_delimiter}"reference"{tuple_delimiter}"Published guidelines on standardized tracheostomy care protocol"){record_delimiter}
("relationship"{tuple_delimiter}"Tracheostomy Care"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Document title is associated with this unique document number."{tuple_delimiter}"document_title, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Medical Department Surgery"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Indicates the originating entity for the tracheostomy care document."{tuple_delimiter}"originating_entity, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"To ensure that all adult & pediatric patients with tracheostomy receive safe and standardized care"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"States the fundamental purpose of the tracheostomy care policy."{tuple_delimiter}"purpose, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Only competent registered nurses trained in tracheostomy shall perform tracheostomy care per competency checklist; all patients with tracheostomy assessed upon admission, after tube insertion/change and every 24 hours; patients placed on oxygen therapy; and referred to Speech-Language Pathology Services"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Outlines the key policy mandates for tracheostomy care delivery."{tuple_delimiter}"policy, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Applied to the Tracheostomy Care Specialist, registered nurses, speech language pathologists, respiratory therapists, and physicians at KHCC"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Defines the multidisciplinary team subject to the policy."{tuple_delimiter}"scope, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Nurse Manager"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Responsible for communicating the tracheostomy care policy to the nursing staff."{tuple_delimiter}"responsibility, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Tracheostomy Care Specialist"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Serves as the primary coordinator for patient care supervision and nurse training in tracheostomy care."{tuple_delimiter}"responsibility, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Multidisciplinary Team"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Mandates that all team members adhere to the tracheostomy care guidelines."{tuple_delimiter}"responsibility, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Tracheostomy"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Provides the definition for the surgical opening created in the trachea."{tuple_delimiter}"definition, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Tracheostomy tube"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Defines the device used to maintain airway patency in tracheostomy care."{tuple_delimiter}"definition, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Suctioning"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Defines the process of aspirating secretions from the airway."{tuple_delimiter}"definition, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"6.1–6.5 steps, including assessment, multidisciplinary care roles, equipment setup, and emergency response"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Outlines the comprehensive procedures for tracheostomy care."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"POLSRG-02/Attach. A"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Links the attachment containing the emergency tracheostomy management algorithm."{tuple_delimiter}"procedure, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"Daily nursing flow sheet, Tracheostomy Care technician Note, Physician Progress note, Interdisciplinary patient/family education note, Emergency tracheostomy management algorithm (POLSRG-02/Attach. A)"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Specifies the documentation required for tracheostomy care."{tuple_delimiter}"documentation, document_number"{tuple_delimiter}9){record_delimiter}
("relationship"{tuple_delimiter}"http://www.n-i.nhs.uk/mater/pubinfo/ (www.tracheostomy.org.uk) http://www.langara.bc.ca/vnc/trach.htm"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Online references supporting tracheostomy care guidelines."{tuple_delimiter}"reference, document_number"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"AACN Procedure manual for critical care, Philadelphia, 2001-2005"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Reference manual for critical care procedures cited in the policy."{tuple_delimiter}"reference, document_number"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"American thoracic society (2004)"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Guidelines from the American Thoracic Society on tracheostomy care."{tuple_delimiter}"reference, document_number"{tuple_delimiter}7){record_delimiter}
("relationship"{tuple_delimiter}"Association of Standardized Tracheostomy Care Protocol Implementation and Reinforcement With the Prevention of Life-Threatening Respiratory Events JAMA Otolaryngol Head Neck Surg. doi:10.1001/jamaoto.2018.0484 Published online May 24, 2018"{tuple_delimiter}"POLSRG-02"{tuple_delimiter}"Published guidelines on standardized tracheostomy care protocol."{tuple_delimiter}"reference, document_number"{tuple_delimiter}7){record_delimiter}
("content_keywords"{tuple_delimiter}"tracheostomy care, registered nurse, surgical resident, emergency management, oxygen therapy, speech-language pathology, multidisciplinary, assessment, documentation, tracheostomy tube, suctioning"{completion_delimiter}
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
