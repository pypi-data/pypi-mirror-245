import uuid
import time


class VendBuilder:
  def __init__(self, db, company_data: list) -> None:
    self.company_id = str(uuid.uuid4())
    self.company_name = company_data[0]
    self.db = db
    self.company_data = company_data

  
  def format(self, item):
    item['id'] = str(uuid.uuid4())
    item['type'] = item['itemType']

    if item['type'] != 'company':
      item['vendorId'] = self.company_id
      item['vendorName'] = self.company_name

    del item['itemType']

    return item

  
  def build_company(self):
    company = self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'company'")

    company['name'] =  self.company_name
    company['email'] = self.company_data[14]
    company['isDemo'] = self.company_data[1]   
    company['subscriptionType'] = self.company_data[2]        
    company['website'] = self.company_data[3]
    company['address'] = {
      'street': self.company_data[4],
      'city': self.company_data[5],
      'province': self.company_data[6],
      'postalCode': self.company_data[7],
      'country': self.company_data[8],
      'office': self.company_data[9]
    }
    company['phone'] = self.company_data[10]
    company['dates']['added'] = int(time.time())

    company = self.format(company)

    company['id'] = self.company_id
    return company


  def build_profile_state(self):
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualProfileState'"))


  def build_payment_state(self):
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualPaymentState'"))
  

  def build_documents_state(self):
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualDocumentsState'"))


  def build_requirements_state(self):
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorPreQualRequirementsState'"))


  def build_stepper_state(self):
    return self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorStepperState'"))


  ## Remove After Refactor
  def build_additional_requirements(self):
    additional_requirements = self.db.get_results(query="SELECT * FROM c WHERE c.type = 'additionalRequirement'")
    for item in additional_requirements:
      item["id"] = str(uuid.uuid4())
      item["type"] = "vendorAdditionalRequirement"
      item["text"] = item['text']
      item["defaultDocumentIdList"] = ["4270e05d-8339-4d13-b2ec-2f7a6848a063"]
      item["additionalRequirementId"] = item['id']
      item["vendorId"] = self.company_id
      item["isActive"] = False

    return additional_requirements


  ## Remove After Refactor
  def build_safety_policies(self):
    safety_policies = self.db.get_results(query="SELECT * FROM c WHERE c.type = 'doc' AND c.docClass = 'safetyPolicy'")
    for item in safety_policies:
      item["defaultDocumentIdList"] = [item['id']]
      item["id"] = str(uuid.uuid4())
      item["isActive"] = False
      item["type"] = "vendorSafetyPolicy"
      item["text"] = item['docType']
      item["vendorId"] = self.company_id          

    return safety_policies


  def build_safety_stats(self):
    safety_stats = self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'vendorSafetyStats'"))
    del safety_stats['vendorName']
    return safety_stats
  

  ## Remove After Refactor
  def build_service_locations(self):
    service_locations = self.db.get_results(query="SELECT * FROM c WHERE c.type = 'serviceLocation'")
    doc_results = self.db.get_results(query="SELECT c.id FROM c where c.type = 'doc' and (c.docClass = 'cor' or c.docClass = 'wcb')")
    for item in service_locations:
      item["serviceLocationId"] = item['id']
      item["id"] = str(uuid.uuid4())
      item["isActive"] = False
      item["type"] = "vendorServiceLocation"
      item["text"] = item['text']
      item["vendorDocKey"] = item['typeKey']
      item["defaultDocumentIdList"] = [x['id'] for x in doc_results]
      item["highChartsKey"] = item['highChartsKey']
      item["highChartsValue"] = 0
      item["vendorId"] = self.company_id

    return service_locations
      




