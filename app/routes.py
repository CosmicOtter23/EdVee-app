import secrets, os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt, mail
from app.forms import (RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm, 
                         ElementForm2, CollectionForm, RequestResetForm, ResetPasswordForm)
from app.models import User, Project, Element, Connection, Type, Access, Collection
from flask_login import login_user, current_user, logout_user, login_required
from math import ceil
from time import time
from flask import jsonify
from flask_mail import Message
# from dotenv import load_dotenv


@app.route("/")
@app.route("/home")
@login_required
def home():
  query = db.session.query(Project)

  accesses = Access.query.filter_by(user_id=current_user.id)
  project_ids = []
  for project in query:
    if (project.creator_id == current_user.id):
      project_ids.append(project.id)
    else:
      for access in accesses:
        # print("access:", access.project_id, "\nproject:", project)
        if (project.id == access.project_id):
          project_ids.append(project.id)
  
  page = int(request.args.get('page', 1))
  
  query = query.filter(Project.id.in_(project_ids))

#   for p in query:
#     print("project:", p)

  projects = query.order_by(Project.date_created.desc()).paginate(page=page, per_page=5)

  elements = Element.query.all()
  return render_template('home.html', projects=projects, elements=elements, title='Home')


@app.route("/about")
def about():
  
  if request.is_json:
    seconds = time()
    return jsonify({'seconds': seconds})

  return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('home'))
  form = RegistrationForm()
  if form.validate_on_submit():
    hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    user = User(name=form.name.data, email=form.email.data, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    flash(f'Your account has been created. You are now logged in', 'success')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
  logout_user()
  return redirect(url_for('home'))


def save_picture(form_picture):
  random_hex = secrets.token_hex(8)
  _, f_ext = os.path.splitext(form_picture.filename)
  picture_fn = random_hex + f_ext
  picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
  
  output_size = (128, 128)
  i = Image.open(form_picture)
  i.thumbnail(output_size)
  i.save(picture_path)
  return picture_fn


@app.route("/account/<int:id>", methods=['GET', 'POST'])
@login_required
def account(id):
  # user = current_user
  user = User.query.filter_by(id=id).first_or_404()
  page = request.args.get('page', 1, type=int)
  
  # projects = Project.query.filter_by(creator=user)\
  #   .order_by(Project.date_created.desc())\
  #   .paginate(page=page, per_page=5)

  query = db.session.query(Project)
  query = query.filter_by(creator_id=id)

  accesses = Access.query.filter_by(user_id=current_user.id)
  project_ids = []
  for project in query:
    if (project.creator_id == current_user.id):
      project_ids.append(project.id)
    else:
      for access in accesses:
        # print("access:", access.project_id, "\nproject:", project)
        if (project.id == access.project_id):
          project_ids.append(project.id)
  
  page = int(request.args.get('page', 1))
  
  query = query.filter(Project.id.in_(project_ids))

  for p in query:
    print("project:", p)

  projects = query.order_by(Project.date_created.desc()).paginate(page=page, per_page=5)
  collections = Collection.query.filter_by(creator_id=id)
  
  elements = Element.query.all()
  connections = Connection.query.all()
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.name = form.name.data
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated', 'success')
    return redirect(url_for('account', id=current_user.id))
  elif request.method == 'GET':
    form.name.data = current_user.name
    form.email.data = current_user.email
  image_file = url_for('static', filename='profile_pics/' + user.image_file)
  return render_template('account.html', title='Account', image_file=image_file, form=form, user=user, 
                         projects=projects, elements=elements, connections=connections, collections=collections)


@app.route("/project/<int:project_id>")
def project(project_id):
  project = Project.query.get_or_404(project_id)
  elements = Element.query.all()
  accesses = Access.query.filter_by(project_id=project.id)
  access_level = 0
  if (current_user.id == project.creator_id):
    access_level = 3
  else:
    for access in accesses:
      if (access.user_id == current_user.id and access.project_id == project.id):
        access_level = access.access_level

  collections = Collection.query.filter_by(creator_id=current_user.id).all()

  project_url = request.url
  print("access_level:", access_level)
  if (access_level > 0):
    return render_template('project.html', name=project.name, project=project, elements=elements, 
                          project_url=project_url, access_level=access_level, collections=collections)
  else:
    return render_template('no_access.html')


@app.route("/project/<int:project_id>/update", methods=['GET', 'POST'])
@login_required
def update_project(project_id):
  project = Project.query.get_or_404(project_id)
  elements = Element.query.all()
  connections = Connection.query.all()
  types = Type.query.all()
  sections = ["los", "content", "las", "assessments"]
  if project.creator != current_user:
    # HTTP response for a forbidden route
    abort(403)
  form = ProjectForm()
  if form.validate_on_submit():
    project.name = form.name.data
    project.desc = form.desc.data

    # For loop to determine if the user has added or removed any elements by
    # evaluating the elements in the box against those stored in the database
    for i in range(4):
      stored_items = Element.query.filter_by(element_type=i+1, project_id=project.id).all()
      print("Stored items:", stored_items)
      print("sections[i]:", sections[i])
      current_items = eval(f"form.{sections[i]}.data.split('|')")
      print("Current items:", current_items)
      for s_item in stored_items:
        for c_item in current_items:
          if (s_item.name == c_item):
            stored_items.remove(s_item)
            current_items.remove(c_item)

      # Runs if current_items has values left in it. This means user has added items
      for item in current_items:
        new_element = Element(name=item, desc="", element_type=i+1, project_id=project.id)
        db.session.add(new_element)
        
      # Runs if stored_items has values left in it. This means user has removed items
      for item in stored_items:
        element_to_remove = Element.query.filter_by(id=item.id).first()
        db.session.delete(element_to_remove)

    # Get the checkbox matrix data from the form submission
    checkbox_matrix = request.form.getlist('checkbox')
    print("checkbox_matrix:", checkbox_matrix)
    submitted_connections = {tuple(value.split(',')) for value in checkbox_matrix}

    print("submitted_connections:", submitted_connections)

    # Fetch existing records from the database
    existing_records = Connection.query.all()
    existing_connections = {(record.element1, record.element2) for record in existing_records}

    print("existing_connections:", existing_connections)

    # Add new connections
    for row, column in submitted_connections - existing_connections:
      record = Connection(element1=row, element2=column)
      db.session.add(record)

    # Remove unchecked connections
    for row, column in existing_connections - submitted_connections:
      record_to_delete = Connection.query.filter_by(element1=row, element2=column).first()
      db.session.delete(record_to_delete)

    db.session.commit()
    flash('Your project has been updated', 'success')
    return redirect(url_for('project', project_id=project.id))
  elif request.method == 'GET':
    form.name.data = project.name
    form.desc.data = project.desc

    # for i in range(4):
    #   output = ""
    #   items = Element.query.filter_by(element_type=i+1, project_id=project.id).all()
    #   for item in items:
    #     output += item.name + "|"
    #   setattr(form, f"{sections[i]}.data", output[:-1])
      
    output = ""
    items = Element.query.filter_by(element_type=1, project_id=project.id).all()
    for item in items:
      output += item.name + "|"
    form.los.data = output[:-1]
    output = ""
    items = Element.query.filter_by(element_type=2, project_id=project.id).all()
    for item in items:
      output += item.name + "|"
    form.content.data = output[:-1]
    output = ""
    items = Element.query.filter_by(element_type=3, project_id=project.id).all()
    for item in items:
      output += item.name + "|"
    form.las.data = output[:-1]
    output = ""
    items = Element.query.filter_by(element_type=4, project_id=project.id).all()
    for item in items:
      output += item.name + "|"
    form.assessments.data = output[:-1]

  db.session.commit()
  return render_template('create_project.html', title='Update Project', form=form, 
                         legend='Update Project', project=project, elements=elements,
                         connections=connections, types = types)


@app.route("/project/<int:project_id>/delete", methods=['POST'])
@login_required
def delete_project(project_id):
    project = Project.query.get_or_404(project_id)
    if project.creator != current_user:
        abort(403)

    for connection in Connection.query.filter_by(project_id=project_id):
        db.session.delete(connection)
    db.session.commit()

    for element in Element.query.filter_by(project_id=project_id):
        db.session.delete(element)
    db.session.commit()

    for access in Access.query.filter_by(project_id=project_id):
        db.session.delete(access)
    db.session.commit()

    db.session.delete(project)
    db.session.commit()
    flash('Your project has been deleted', 'success')
    return redirect(url_for('home'))


@app.route("/add_to_collection/<int:project_id>", methods=['GET', 'POST'])
@login_required
def add_to_collection(project_id):
  collection_id = request.form.get('selected_collection')
  print("Collection_id:", collection_id)
  project = Project.query.filter_by(id=project_id).first()
  collection = Collection.query.filter_by(id=collection_id).first()
  project.collection_id = collection.id
  db.session.commit()
  print("added", project.name, "to", collection.name)

  return redirect(url_for('project', project_id=project_id))


@app.route("/remove_from_collection/<int:project_id>", methods=['GET', 'POST'])
@login_required
def remove_from_collection(project_id):
  project = Project.query.filter_by(id=project_id).first()
  collection_id = project.collection_id
  project.collection_id = None
  db.session.commit()
  print("removed", project.name)

  return redirect(url_for('collection', collection_id=collection_id))

@app.route("/project_wizard")
@login_required
def project_wizard():
  form = ProjectForm()
  return render_template('project_wizard.html', form=form)


@app.route("/project_wiz_1/<int:project_id>", methods=['GET', 'POST'])
@login_required
def project_wiz_1(project_id):
  form = ProjectForm()
  project = Project.query.get_or_404(project_id)
  if form.validate_on_submit():
    # project = Project(name=form.name.data, desc=form.desc.data, creator=current_user)
    project.name = form.name.data
    project.desc = form.desc.data
    db.session.add(project)
    db.session.commit()
    print(project)
    # project_id = Project.query.order_by(Project.id).first()
    # flash("Project added to db. ID:", project_id)
    # print("Project added to db. ID:", project_id)
    return redirect(url_for('project_wiz_2A', project_id=project.id, element_type=1))
  elif request.method == 'GET':
    form.name.data = project.name
    form.desc.data = project.desc

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/project_wiz_1.html', form=form, project=project)
  else:
    return render_template('no_access.html')


@app.route("/project/new", methods=['GET', 'POST'])
@login_required
def project_new():
    form = ElementForm2()
    project = Project(name="Untitled Project", desc="", creator=current_user)
    db.session.add(project)
    db.session.commit()
    print("Date created:", project.date_created)
    return render_template("wizard/project_wiz_4.html", project=project, form=form, access_level=4)

#     form = ProjectForm()
#     if form.validate_on_submit():
#         project = Project(name=form.name.data, desc=form.desc.data, creator=current_user)
#         db.session.add(project)
#         db.session.commit()
#         print(project)
#         # project_id = Project.query.order_by(Project.id).first()
#         # flash("Project added to db. ID:", project_id)
#         # print("Project added to db. ID:", project_id)
#         return redirect(url_for('project_wiz_2A', project_id=project.id, element_type=1))

# #   return render_template('wizard/project_wiz_1.html', form=form)
#     return redirect(url_for('project', project_id=project.id))


@app.route("/project_wiz_2A/<int:project_id>/<int:element_type>", methods=['GET', 'POST'])
@login_required
def project_wiz_2A(project_id, element_type):
  project = Project.query.get_or_404(project_id)
  # form = ElementForm2()
  elements = Element.query.filter_by(project_id=project_id, element_type=element_type)
  print("elements:", elements)

  if (element_type == 5):
    return redirect(url_for('project_wiz_3A', project_id=project_id, current_index=0))
  elif (element_type == 0):
    return redirect(url_for('project_wiz_1', project_id=project_id))

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/project_wiz_2A.html', project=project,
                            element_type=element_type, elements=elements)
  else:
    return render_template('no_access.html')


@app.route("/element_form/<int:project_id>/<int:element_type>", methods=['GET', 'POST'])
@login_required
def element_form(project_id, element_type):
  project = Project.query.get_or_404(project_id)
  form = ElementForm2()

  if (element_type == 5):
    return redirect(url_for('project_wiz_3', project_id=project_id))

  if form.validate_on_submit():
    stored_items = Element.query.filter_by(element_type=element_type, project_id=project.id).all()
    current_items = form.name.data.splitlines()
    for s_item in stored_items:
      for c_item in current_items:
        if (s_item.id == c_item):
          stored_items.remove(s_item)
          current_items.remove(c_item)

    # Runs if current_items has values left in it. This means user has added items
    for item in current_items:
      print("Element Added")
      new_element = Element(name=item, desc="Default desc", element_type=element_type, project_id=project.id)
      db.session.add(new_element)
      
    # Runs if stored_items has values left in it. This means user has removed items
    for item in stored_items:
      print("Element removed")
      for connection in Connection.query.filter_by(element1=item.id):
        db.session.delete(connection)
      for connection in Connection.query.filter_by(element2=item.id):
        db.session.delete(connection)

      element_to_remove = Element.query.filter_by(id=item.id).first()
      db.session.delete(element_to_remove)

    db.session.commit()

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/project_wiz_2A.html', form=form, project=project, element_type=element_type)
  else:
    return render_template('no_access.html')


@app.route("/new_element/<int:project_id>/<int:element_type>", methods=['GET', 'POST'])
@login_required
def new_element(project_id, element_type):
  project = Project.query.get_or_404(project_id)
  form = ElementForm2()

  if form.validate_on_submit():
    element = Element(name=form.name.data, desc=form.desc.data, 
                      element_type=element_type, project_id=project_id)    
    db.session.add(element)
    db.session.commit()
    return redirect(url_for('project_wiz_2A', project_id=project.id, element_type=element_type))

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/new_element.html', form=form, project=project, element_type=element_type, previous_page=2)
  else:
    return render_template('no_access.html')


@app.route("/update_element/<int:project_id>/<int:element_id>/<int:previous_page>", methods=['GET', 'POST'])
@login_required
def update_element(project_id, element_id, previous_page):
  project = Project.query.get_or_404(project_id)
  form = ElementForm2()
  element = Element.query.filter_by(id=element_id).first()
  print("element:", element)

  if form.validate_on_submit():   
    element.name = form.name.data
    element.desc = form.desc.data
    db.session.commit()
    print("form:", form.desc.data)
    print("element:", element.desc)
    if (previous_page == 2):
      return redirect(url_for('project_wiz_2A', project_id=project.id, element_type=element.element_type))
    elif (previous_page == 4):
      return redirect(url_for('project_wiz_4', project_id=project.id))
  elif request.method == 'GET':
    form.name.data = element.name
    form.desc.data = element.desc

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/new_element.html', form=form, project=project, element=element, previous_page=previous_page)
  else:
    return render_template('no_access.html')


@app.route("/delete_element/<int:element_id>", methods=['GET', 'POST'])
@login_required
def delete_element(element_id):
  element = Element.query.filter_by(id=element_id).first()
  project = Project.query.get_or_404(element.project_id)
  elements = Element.query.filter_by(project_id=element.project_id, element_type=element.element_type).order_by(Element.id)
  
  connections = Connection.query.filter(Connection.element1 == element.id and Connection.element2 == element.id).all()
  for connection in connections:
    print(connection)
    db.session.delete(connection)
  db.session.commit()

  db.session.delete(element)
  db.session.commit()
  flash('Your element has been deleted', 'success')

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/project_wiz_2A.html', project=project,
                          element_type=element.element_type, elements=elements)
  else:
    return render_template('no_access.html')


@app.route("/project_wiz_3/<int:project_id>", methods=['GET', 'POST'])
@login_required
def project_wiz_3(project_id):
  project = Project.query.get_or_404(project_id)
  elements = Element.query.filter_by(project_id=project_id)
  connections = Connection.query.filter_by()
  element_1s = []
  element_2s = []
  for connection in connections:
    for element_1 in elements:
      for element_2 in elements:
        if (connection.element1 == element_1.id and connection.element2 == element_2.id):
          # flash("Connection found!")
          # print("Connection found!")
          element_1s.append(element_1)
          element_2s.append(element_2)
          
  elements = Element.query.all()

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/project_wiz_3.html', project=project, elements=elements, 
                         element_1s=element_1s, element_2s=element_2s)
  else:
    return render_template('no_access.html')


@app.route("/project_wiz_3A/<int:project_id>/<string:current_index>", methods=['GET', 'POST'])
@login_required
def project_wiz_3A(project_id, current_index):
  project = Project.query.get_or_404(project_id)
  elements = Element.query.filter_by(project_id=project_id)
  connections = Connection.query.filter_by(project_id=project_id)
  types = ["Learning Outcomes", "Content", "Learning Activities", "Assessments"]
#   indexes = [[1,3], [3,2], [2,4], [4,1]]
  indexes = [[1,3], [2,3], [2,4], [1,4]]
  current_index = int(current_index)

  if (current_index > 3):
    return redirect(url_for('project_wiz_4', project_id=project_id))
  elif (current_index < 0):
    return redirect(url_for('project_wiz_2A', project_id=project_id, element_type=4))

  access_level = getAccessLevel(current_user.id, project.id)
  
  if (access_level > 1):
    return render_template('wizard/project_wiz_3A.html', project=project, elements=elements, 
                          connections=connections, types=types, indexes=indexes, current_index=current_index)
  else:
    return render_template('no_access.html')


@app.route("/project_wiz_4/<int:project_id>", methods=['GET', 'POST'])
@login_required
def project_wiz_4(project_id):
    form = ElementForm2()
    project = Project.query.get_or_404(project_id)
    elements = Element.query.filter_by(project_id=project_id)
    connections = Connection.query.filter_by()
    element_1s = []
    element_2s = []
    for connection in connections:
        for element_1 in elements:
            for element_2 in elements:
                if (connection.element1 == element_1.id and connection.element2 == element_2.id):
                    # flash("Connection found!")
                    # print("Connection found!")
                    element_1s.append(element_1)
                    element_2s.append(element_2)

            
    if form.validate_on_submit():
        idNo = request.form.get('hiddenValue')
        for element in elements:
            if (element.id == int(idNo)):
                element.name = form.name.data
                element.desc = form.desc.data
                print("element found!", element.id)
        db.session.commit()
            
    elements = Element.query.all()

    access_level = getAccessLevel(current_user.id, project.id)
    
    if (access_level > 1):
        return render_template('wizard/project_wiz_4.html', form=form, project=project, elements=elements, 
                            connections=connections)
    else:
        return render_template('no_access.html')
  

@app.route("/collection/<int:collection_id>", methods=['GET', 'POST'])
@login_required
def collection(collection_id):
  collection = Collection.query.filter_by(id=collection_id).first()
  creator = User.query.filter_by(id=current_user.id).first()

  page = request.args.get('page', 1, type=int)
  
  projects = Project.query.filter_by(collection_id=collection.id)\
    .order_by(Project.date_created.desc())\
    .paginate(page=page, per_page=5)

  return render_template('collection.html', collection=collection, creator=creator, projects=projects)
  

@app.route("/collection/new", methods=['GET', 'POST'])
@login_required
def create_collection():
  form = CollectionForm()
  if form.validate_on_submit():
    collection = Collection(name=form.name.data, desc=form.desc.data, creator_id=current_user.id)
    db.session.add(collection)
    db.session.commit()
    print(collection.id)
    return redirect(url_for('collection', collection_id=collection.id))

  return render_template('create_collection.html', form=form)

@app.route("/collection/delete/<int:collection_id>", methods=['GET', 'POST'])
@login_required
def delete_collection(collection_id):
  projects = Project.query.filter_by(collection_id=collection_id)
  for project in projects:
    project.collection_id = None

  collection = Collection.query.filter_by(id=collection_id).first()
  db.session.delete(collection)
  db.session.commit()

  return redirect(url_for('account', id=collection.creator_id))


@app.route("/api/recordLine", methods=['POST'])
def record_line():
  try:
    data = request.json
    box1_id = data['box1Id']
    box2_id = data['box2Id']

    element1_id = box1_id.split('|')[0]
    element2_id = box2_id.split('|')[0]

    # Your code to record the line here
    # print("Box 1:", element1_id, "\nBox 2:", element2_id)
    element = Element.query.filter_by(id=element1_id).first()
    # print(element)
    project = Project.query.filter_by(id=element.project_id).first()
    connection = Connection(project_id=project.id, element1=element1_id, element2=element2_id)
    # print(connection)
    db.session.add(connection)
    db.session.commit()

    # Assuming recording is successful
    return jsonify({'message': 'Line recorded successfully'}), 200

  except Exception as e:
    return jsonify({'error': 'Error recording line: ' + str(e)}), 500
  

@app.route("/api/deleteLine", methods=['POST'])
def delete_line():
  try:
    data = request.json
    box1_id = data['box1Id']
    box2_id = data['box2Id']

    element1_id = box1_id.split('|')[0]
    element2_id = box2_id.split('|')[0]

    # Your code to record the line here
    # print("Box 1:", element1_id, "\nBox 2:", element2_id)
    connection = Connection.query.filter_by(element1=element1_id, element2=element2_id).first()
    if (connection):
      db.session.delete(connection)

    connection = Connection.query.filter_by(element1=element2_id, element2=element1_id).first()
    if (connection):
      db.session.delete(connection)
    
    db.session.commit()

    # Assuming deletion is successful
    return jsonify({'message': 'Line deleted successfully'}), 200

  except Exception as e:
    return jsonify({'error': 'Error deleting line: ' + str(e)}), 500
  

@app.route("/get_connections", methods=['GET'])
def get_connections():
  connections = Connection.query.all()
  # Convert SQLAlchemy model objects to dictionaries
  connections_dict = [connection.__dict__ for connection in connections]
  
  # Optionally, remove any unwanted properties before JSON serialization
  for connection in connections_dict:
    connection.pop('_sa_instance_state', None)
    # print(connection)

  return jsonify(connections_dict)
  

@app.route("/get_elements", methods=['GET'])
def get_elements():
  elements = Element.query.all()
  # Convert SQLAlchemy model objects to dictionaries
  elements_dict = [connection.__dict__ for connection in elements]
  
  # Optionally, remove any unwanted properties before JSON serialization
  for connection in elements_dict:
    connection.pop('_sa_instance_state', None)
    # print(connection)

  return jsonify(elements_dict)


@app.route("/api/addAccess", methods=['GET', 'POST'])
def addAccess():
  try:
    data = request.json
    user_id = data['userId']
    project_id = data['projectId']
    access_level = data['accessLevel']

    existing = Access.query.filter_by(user_id=user_id, project_id=project_id).first()

    if (existing):
      # If record already exists, make sure access level matches by updating it
      print("record exists")
      existing.access_level = access_level
    else:
      # If record does not exist, create new
      print("record does not yet exist")
      access = Access(user_id=user_id, project_id=project_id, access_level=access_level)
      db.session.add(access)

    db.session.commit()

    return jsonify({'message': 'Access recorded/updated successfully'}), 200

  except Exception as e:
    return jsonify({'error': 'Error recording line: ' + str(e)}), 500
  

@app.route("/removeAccess/<int:access_id>", methods=['GET', 'POST'])
def removeAccess(access_id):
  itemToRemove = Access.query.filter_by(id=access_id).first()
  project_id = itemToRemove.project_id
  db.session.delete(itemToRemove)
  print("Access removed")
  db.session.commit()

  return redirect(url_for('search_users', project_id=project_id))


@app.route("/search_users/<int:project_id>", methods=['GET', 'POST'])
def search_users(project_id):
  form = ElementForm2()
  project = Project.query.filter_by(id=project_id).first()
  accesses = Access.query.filter_by(project_id=project.id)

  usersWithAccess = []
  for a in accesses:
    user = User.query.filter_by(id=a.user_id).first()
    if user not in usersWithAccess:
      usersWithAccess.append(user)

  # print(project.id)
  users = []
  if form.validate_on_submit:
    input = ""
    input = str(form.name.data).lower()
    for user in User.query.all():
      if ((input in user.name.lower() or input in user.email.lower() or input in str(user.id).lower())
           and (user != current_user) and (user not in usersWithAccess)):
        users.append(user)

  return render_template('search_users.html', form=form, users=users, project=project, accesses=accesses,
                          usersWithAccess=usersWithAccess)


# @app.route("/no_access", methods=['GET', 'POST'])
# def no_access():


@app.route("/test_page", methods=['GET', 'POST'])
def test_page():
  return render_template('test_page.html')


def getAccessLevel(user_id, project_id):
  project = Project.query.filter_by(id = project_id).first()
  if (project.creator_id == user_id):
    level = 4
  else:
    access = Access.query.filter(Access.user_id == user_id and Access.project_id == project_id).first()
    level = access.access_level
  if (level):
    return level
  else:
    return 0
  

@app.route("/register_email", methods=['GET', 'POST'])
def register_email():
    if request.method == 'GET':
        return '<form action="/register_email" methos="POST"><input name="email><input type="submit"></form>'
    return 'The email you entered is {}'.formate(request.form['email'])
    

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='info.edvee@gmail.com', recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:\n

                {url_for('reset_token', token=token, _external=True)}

                If you did not make this request, ignore this email and no changes will be made.
                '''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    # load_dotenv()
    # flash(os.environ.get('EMAIL_USER'))
    # print(os.environ.get('EMAIL_PASSWORD'))
    # print(os.getenv('EMAIL_PASSWORD'))
    # print(os.environ)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        print('An email has been sent with instructions to reset your password', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', form=form)
    

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    # flash("User:", user.name)
    if user is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Your password has been updated.', 'success')
        return redirect(url_for('home'))
    return render_template('reset_token.html', form=form)
