
# -*- coding: utf-8 -*-
# this file is used to test the editor


from datetime import datetime

def edit_procedure():
    """
    This function received ajax request to generated the HTML content for editor

    : parameter precedure_id: the precedure_id parameter in precedure TABLE sent by request.vars
    : type precedure_id: int
    :return: Dict with HTML content of editor and procedure_id, procedure data, editor preferences
    :rtype: Json
    """
    # parameter for CodeMirror option parameter used for setting the editor feature
    preferences={'theme':'web2py', 'editor': 'default', 'closetag': 'true', 'codefolding': 'false', 'tabwidth':'4', 'indentwithtabs':'false', 'linenumbers':'true', 'highlightline':'true'}

    # get the procedure_id of procedure in TABLE procedure
    procedure_id = request.vars.procedure_id

    # the final edition will use Team 2 API "get_procedure_data(procedure_id, stable)"  to get the data
    data = db(db.coding.id == procedure_id).select(db.coding.procedures).first().procedures

    file_details = dict(
                    editor_settings=preferences,     # the option parameters used for setting editor feature.
                    id=procedure_id,                 # the procedure_id in the procedures TALBE
                    data=data,                       # code for procedure which is related with the id.
                    )

    #generated HTML code for editor by parameters in file_details
    plain_html = response.render('editor/edit_js.html', file_details)

    # add the HTML content element for editor to file_details dictionary
    file_details['plain_html'] = plain_html

    return response.json(file_details)


def save_procedure():
    """
    This function received ajax request to save procedure to the procedure TABLE

    : parameter procedure_id: the precedure_id parameter in precedure TABLE sent by request.vars
    : type procedure_id: int
    : parameter procedure: the procedure data in procedure TABLE sent by request.vars
    : type procedure: str
    : parameter stable: the sign to identify if saved procedure is stable
    : type stable: boolean
    :return: whether the procedure is saved correctlly.
    :rtype: str
    """

    # obtain parameter from ajax request
    procedure_id = request.vars.procedure_id
    data = request.vars.procedure
    stable = request.vars.stable

    #save the procedure data to the database
    if stable is False:

        #the final edition will use Team 2 API save(procedure_id, stable) to save the data
        db(db.coding.id == procedure_id).update(procedures =data)

    return dict(result='true')


## all the following function is used for self debug and will be deleted at final edition
def create():
    """
    This function is only used for self debug to create a new procedure and will be deleted in the final edition
    Team 2 provide the API create_procedure() to create a new procedure and return the procedure_id
    :return: the time for create one row in database
    :rtype: str
    """

    # get the utc time for the create process
    now = datetime.utcnow()

    # the initial procedure data that saved for this row
    code = "# enter your new procedure in the following" + now.strftime("%Y-%m-%d %H:%M:%S")

    # insert a new row for procedure
    db.coding.insert(procedures=code, times=now)

    return dict(result = now)


def select():
    """
    This function is only used for self debug to show exited procedure in database and will be deleted in the final edition
    Team 2 provide the API get_procedures_for_user(user_id) to return the list of procedure_id belong to a user
    :return: the existed rows for procedure in database
    :rtype: dict
    """

    return dict(code_list = db(db.coding).select())


def test_edit():
    """
    This is served for the test example view page, which help UI team to integrate editor
    This function will be delete at final edition
    parameter procedure_id: the precedure_id parameter in precedure TABLE sent by request.vars
    type procedure_id: int
    :return: the procedure_id for procedure in procedure TABLE
    :rtype: dict
    """
    # get the procedure_id of procedure in TABLE procedure
    procedure_id = request.vars.procedure_id

    return dict(procedure_id = procedure_id)