from google.appengine.api import urlfetch
from helpers.config import config
import json
import urllib
import logging
import pprint

DEBUG = config.curl.debug

"""
	request_type: json or urlencode (default)
	response_type: json (default) or raw
"""
def execute_post(endpoint_url, post_data, headers={}, request_type='urlencode', response_type='json'):
	# prepare the post data according the request type chosen
	post_data = _get_post_data_according_request_type(post_data, request_type)

	# prepare content type header
	headers = _set_headers_according_request_type(headers, request_type)

	if DEBUG:
		# log the request
		logging.debug('=======================')
		logging.debug('REQUEST')
		logging.debug('POST %s' % endpoint_url)
		logging.debug('Headers:')
		logging.debug('\n'.join(['%s: %s' % (k, headers[k]) for k in headers]))
		logging.debug('Body')
		pprint.pprint(post_data)
		logging.debug('=======================')
		logging.debug('RESPONSE')

	urlfetch.set_default_fetch_deadline(60)
	response = urlfetch.fetch(url=endpoint_url,
		payload=post_data,
		method=urlfetch.POST,
		headers=headers);

	body = _get_body_according_response_type(response.content, response_type)

	if DEBUG:
		logging.debug('status_code: %s' % response.status_code)
		logging.debug(body)

	result = {
		'body': body,
		'status_code': response.status_code
	}

	return result


def execute_patch(endpoint_url, post_data, headers={}, request_type='urlencode', response_type='json'):
	# prepare the post data according the request type chosen
	post_data = _get_post_data_according_request_type(post_data, request_type)

	# prepare content type header
	headers = _set_headers_according_request_type(headers, request_type)

	if DEBUG:
		# log the request
		logging.debug('=======================')
		logging.debug('REQUEST')
		logging.debug('PATCH %s' % endpoint_url)
		logging.debug('Headers:')
		logging.debug('\n'.join(['%s: %s' % (k, headers[k]) for k in headers]))
		logging.debug('Body')
		pprint.pprint(post_data)
		logging.debug('=======================')
		logging.debug('RESPONSE')

	urlfetch.set_default_fetch_deadline(60)
	response = urlfetch.fetch(url=endpoint_url,
		payload=post_data,
		method=urlfetch.PATCH,
		headers=headers);

	body = _get_body_according_response_type(response.content, response_type)

	logging.debug('status_code: %s' % response.status_code)
	logging.debug(body)

	result = {
		'body': body,
		'status_code': response.status_code
	}

	return result



def execute_get(endpoint_url, headers={}, response_type='json'):
	# prepare content type header
	headers = _set_headers_according_request_type(headers, 'urlencode')

	if DEBUG:
		# log the request
		logging.debug('=======================')
		logging.debug('REQUEST')
		logging.debug('GET %s' % endpoint_url)
		logging.debug('Headers:')
		logging.debug('\n'.join(['%s: %s' % (k, headers[k]) for k in headers]))
		logging.debug('=======================')
		logging.debug('RESPONSE')

	urlfetch.set_default_fetch_deadline(60)
	response = urlfetch.fetch(url=endpoint_url,
		method=urlfetch.GET,
		headers=headers);

	body = _get_body_according_response_type(response.content, response_type)

	if DEBUG:
		logging.debug('status_code: %s' % response.status_code)
		logging.debug(body)

	result = {
		'body': body,
		'status_code': response.status_code
	}

	return result


def _set_headers_according_request_type(headers, request_type):
	if request_type == 'urlencode':
		headers['Content-Type'] = 'application/x-www-form-urlencoded'
		return headers

	if request_type == 'json':
		headers['Content-Type'] = 'application/json'
		return headers


def _get_post_data_according_request_type(post_data, request_type):
	if request_type == 'urlencode':
		str_post_data = {}
		for k, v in post_data.iteritems():
			str_post_data[k] = unicode(v).encode('utf-8')
		return urllib.urlencode(str_post_data)

	if request_type == 'json':
		return json.dumps(post_data)


def _get_body_according_response_type(body, response_type):
	if response_type == 'json':
		try:
			return json.loads(body)
		except:
			return body
	if response_type == 'raw':
		return body