import base64
import json
import math
import numpy as np
from datetime import date, timedelta, datetime, timezone
import pandas as pd
import pytz

from creaap.formats import to_tz_aware_datetime


# handling JSON serialization fo datetime objects
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if type(obj) is float and math.isnan(obj):
        return "NaN"
    if isinstance(obj, np.int64): 
        try:
            return int(obj)
        except:
            return "NaN"
    elif isinstance(obj, (datetime, date)):
        return obj.isoformat()
    else:
        try:
            return obj.__dict__
        except:
            raise TypeError ("Type %s not serializable" % type(obj)) 

def get_parameter_with_default(req, par_name, default_val = None):
	'''
	Parameters
	----------
	req:
		an http request from an Azure Function
	par_name:str
		how the parameter is supposed to be named in the http request
	default_val: whatever
		a fallback value, defaults to None
	
	Returns
	-------
	object
		whatever the httprequest contained under par_name
		or whatever fuckery you passed as default value
	'''
	value = req.params.get(par_name)
	if value is None:
		try:
			req_body = req.get_json()
		except ValueError:
			value = default_val
		else:
			value = req_body.get(par_name)
			if value is None:
				value = default_val
	return value

def get_parameter(req, par_name):
	'''
	Parameters
	----------
	req:
		an http request from an Azure Function
	par_name:str
		how the parameter is supposed to be named in the http request

	Returns
	-------
	object
		whatever the httprequest contained under par_name
	'''
	value = req.params.get(par_name)
	if value is None:
		try:
			req_body = req.get_json()
		except ValueError:
			pass
		else:
			value = req_body.get(par_name)
			if value is None:
				raise ValueError(str(par_name) + ' cannot be None')
	return value

def get_datetime_parameter_with_default(req, par_name:str, default_val:datetime, timezone_par:str = None, target_timezone = pytz.utc, **kwargs)->datetime:
	'''
	Parameters
	----------
	req:
		an http request from an Azure Function
	par_name:str
		how the datatime parameter is supposed to be named in the http request
	default_val:datetime
		a fallback datetime value
	timezone_par:str
		the name the timezone paramter has in the http request, if any.
		If this paramter is not provided and the datetime in the htto request is naive,
		the function will assume it is in the same timezone as the target_timezone.
	target_timezone:str ot pytz timezone
		the desired output timezone

	Returns
	-------
	datetime
		a timezone-aware datetime object
		or whatever shit you entered as default_val

	'''
	val = get_parameter_with_default(req, par_name, default_val = None)
	# parse the timezone parameter, if any
	if timezone_par:
		tz = get_parameter_with_default(req, timezone_par, default_val = target_timezone)
	else:
		tz = target_timezone
	if val:
		try:
			return to_tz_aware_datetime(val, origin_timezone = tz, target_timezone= target_timezone, **kwargs)
		except:
			return default_val
	return default_val


