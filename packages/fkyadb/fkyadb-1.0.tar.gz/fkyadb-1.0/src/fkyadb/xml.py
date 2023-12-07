import json,re
def xml_to_json(xml):
  list=['index','text','resource-id','class','package','content-desc','checkable','checked','clickable','long','enabled','focusable','focused','scrollable','password','selected','bounds']
  list_node=re.findall('<node.*?>',xml)
  list_node_json=[]
  for node in list_node:
    node=node.replace('<node','{').replace('>','}')
    node=node.replace('" ','",').replace('=',':')
    replace_element=node.replace('long-clickable','long').replace(',/','')
    for element in list:
      if element in node:
        node=replace_element.replace(element,f'"{element}"')
        replace_element=node
      else:
        pass
    list_node_json.append(replace_element)
  return list_node_json
class find_text:
  def __init__(self,element,list_node_json):
    for get_node_json in list_node_json:
      try:
        node_json=json.loads(get_node_json)
      except:
        pass
      if element == node_json['text']:
        self.status='True'
        self.json=node_json
        break
      else:
        self.status='False'
  def get_key(self,key):
    if self.status == 'True':
      list=['index','text','resource-id','class','package','content-desc','checkable','checked','clickable','long','enabled','focusable','focused','scrollable','password','selected','bounds','boundsxy']
      if key in list:
        if key == 'boundsxy':
          return self.json['bounds'].split('[')[1].split(']')[0].split(',')
          self.status='True'
        else:
          value=self.json[key]
          self.status='True'
          return value
      else:
        return 'key does not exist'
    else:
      return None
  def __str__(self):
    if self.status =='True':
      return str(self.json)
    else:
      return self.status
class find_id:
  def __init__(self,element,list_node_json):
    for get_node_json in list_node_json:
      try:
        node_json=json.loads(get_node_json)
      except:
        pass
      if element == node_json['resource-id']:
        self.status='True'
        self.json=node_json
        break
      else:
        self.status='False'
  def get_key(self,key):
    if self.status == 'True':
      list=['index','text','resource-id','class','package','content-desc','checkable','checked','clickable','long','enabled','focusable','focused','scrollable','password','selected','bounds','boundsxy']
      if key in list:
        if key == 'boundsxy':
          return self.json['bounds'].split('[')[1].split(']')[0].split(',')
        else:
          value=self.json[key]
          return value
      else:
        return 'key does not exist'
    else:
      return None
  def __str__(self):
    if self.status =='True':
      return self.json
    else:
      return self.status
class find_class:
  def __init__(element,list_node_json):
    for get_node_json in list_node_json:
      try:
        node_json=json.loads(get_node_json)
      except:
        pass
      if element == node_json['class']:
        self.status='True'
        self.json=node_json
        break
      else:
        self.status='False'
  def get_key(self,key):
    if self.status == 'True':
      list=['index','text','resource-id','class','package','content-desc','checkable','checked','clickable','long','enabled','focusable','focused','scrollable','password','selected','bounds','boundsxy']
      if key in list:
        if key == 'boundsxy':
          return self.json['bounds'].split('[')[1].split(']')[0].split(',')
          
        else:
          value=self.json[key]
          return value
          
      else:
        return 'key does not exist'
    else:
      return None
  def __str__(self):
    if self.status =='True':
      return self.json
    else:
      return self.status
#with open('xml.xml','r') as xml:
  #xml=xml_to_json(xml.read())
  #print(find_text('HOME',xml))