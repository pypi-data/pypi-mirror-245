import uuid
import time
from eam_db_helper import db


class EmpBuilder:
  def __init__(self, db, company_data: list) -> None:
    self.company_id = str(uuid.uuid4())
    self.company_name = company_data[0]
    self.db = db
    self.company_data = company_data


  def format(self, item):
    item['id'] = str(uuid.uuid4())
    item['type'] = item['itemType']
    del item['itemType']

    return item


  def build_company(self):
    company = self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'company'")
    company['id'] = self.company_id
    company['name'] = self.company_data[0]
    company['type'] = 'company'
    del company['itemType']
    company['accountType'] = 'employer'
    company['email'] = self.company_data[13]
    company['isDemo'] = self.company_data[1]
    company['website'] = self.company_data[2]
    company['address'] = {
      'street': self.company_data[3],
      'city': self.company_data[4],
      'province': self.company_data[5],
      'postalCode': self.company_data[6],
      'country': self.company_data[7],
      'office': self.company_data[8]
    }
    company['phone'] = self.company_data[9]
    company['dates']['added'] = int(time.time())

    return company


  def build_tags(self):
    tags = self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'tags'"))
    tags['companyId'] = self.company_id
    return tags
  

  def build_employer_doc_config(self):
    emp_doc_config = self.format(self.db.get_result(query="SELECT * FROM c WHERE c.type = 'template' AND c.itemType = 'employerDocConfig'"))
    emp_doc_config['employerId'] = self.company_id
    emp_doc_config['employerName'] = self.company_name
    return emp_doc_config


  ## ADD MANUALLY FOR NOW
  # def build_questions(self):
  #   pass


  ## ADD MANUALLY FOR NOW
  # def build_doc_notes(self):
  #   pass






