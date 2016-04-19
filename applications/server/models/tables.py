#########################################################################
## Define your tables below, for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)

from datetime import datetime

# For the user management team?
db.define_table('devices',
                # if we give the device an ID, we can do checks to verify devices belong to which device
                Field('device_id', 'string', required=True),
                Field('user_email', 'string', default=db.auth_user.email),
                Field('name', 'string', required=True, default='Unknown Device'), # Name of device
                Field('description', 'text', default=''),
                Field('last_sync', 'datetime', required=True,default=datetime.utcnow()), # TODO: move to synch code?
                Field('device_icon', 'string', required=True, default='fa-globe')  # FA ID needed by UI team
                )

# This is a table that specifies what procedure runs on what device for what user
db.define_table('runs_on',
                Field('user_email', required=True),
                Field('device_id', 'string', required=True),
                Field('proc_id', 'string', required=True)
                )

## These tables are synched "up" from the clients to the server.

db.define_table('logs',
                Field('device_id'),
                Field('time_stamp', 'datetime', default=datetime.utcnow()),
                Field('modulename'),
                Field('log_level', 'integer'), #  int, 0 = most important.
                Field('log_message', 'text'),
                )

db.define_table('outputs',
                Field('device_id'),
                Field('time_stamp', 'datetime', default=datetime.utcnow()),
                Field('modulename'),
                Field('name'), # Name of variable
                Field('output_value', 'text'), # Json, short please
                Field('tag')
                )

db.define_table('module_values',
                Field('device_id'),
                Field('time_stamp', 'datetime', default=datetime.utcnow()),
                Field('modulename'),
                Field('name'),  # Name of variable
                Field('output_value', 'text'),  # Json, short please
                )

db.logs.log_level.requires = IS_INT_IN_RANGE(0, 4)  # limit log type to 5 (INFO, WARNING, DEBUG, ERROR, CRITICAL)
db.logs.time_stamp.writable=False                   # can not manual change log data (time, log_level, log_message)
db.logs.log_level.writable=False
db.logs.log_message.writable=False

## TODO: define the tables that need to be synched "down", for settings, and procedures.
