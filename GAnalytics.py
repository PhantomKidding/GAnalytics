__author__ = 'cchen224'

import argparse
import re
import sys, getopt
from apiclient.discovery import build
import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools

SCOPE = ['https://www.googleapis.com/auth/analytics.readonly']
PARAMS = {}

def print_help():
    print 'GAnalytics.py\n' \
        ' -h  --help\n' \
        ' -a --account\n' \
        ' -b --property\n' \
        ' -p  --profile\n' \
        ' -s  --start\t\t<yyyy-mm-dd or #daysAgo>\n' \
        ' -e  --end  \t\t<yyyy-mm-dd or #daysAgo>\n' \
        ' -f  --filters\t\t<ga:filter>\n' \
        ' -d  --dimensions\t<ga:dimensions>\n' \
        ' -m  --metrics\t\t<ga:metrics>\n' \
        ' -j  --json\t\t<client_secret_file.json>\n' \
        ' -o  --output\t\t<output.csv>\n'


def setup_params(argv):
    try:
        opts, args = getopt.getopt(argv, 'ha:b:p:s:e:f:d:m:j:o:i:l:u:m:g:',
                                   ['account=','property=','profile=',
                                    'start_date=','end_date=','filters=',
                                    'dimensions=','metrics=','json=','output=',
                                    'start_index=', 'sampling_level=',
                                    'sort=', 'max_results=', 'segment=', 'sort='])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-a', '--account'):
            PARAMS['account'] = arg
        elif opt in ('-b', '--property'):
            PARAMS['property'] = arg
        elif opt in ('-p', '--profile'):
            PARAMS['profile'] = arg
        elif opt in ("-s", "--start_date"):
            PARAMS['start_date'] = arg
        elif opt in ("-e", "--end_date"):
            PARAMS['end_date'] = arg
        elif opt in ("-f", "--filters"):
            PARAMS['filters'] = arg
        elif opt in ("-d", "--dimensions"):
            PARAMS['dimensions'] = arg
        elif opt in ("-m", "--metrics"):
            PARAMS['metrics'] = arg
        elif opt in ("-j", "--json"):
            PARAMS['json'] = arg
        elif opt in ("-o", "--output"):
            PARAMS['output'] = arg
        elif opt in ("-i", "--start_index"):
            PARAMS['start_index'] = arg
        elif opt in ("-l", "--sampling_level"):
            PARAMS['sampling_level'] = arg
        elif opt in ("-l", "--sampling_level"):
            PARAMS['sampling_level'] = arg
        elif opt in ("-l", "--sampling_level"):
            PARAMS['sampling_level'] = arg
        elif opt in ("-m", "--max_results"):
            PARAMS['max_results'] = arg
        elif opt in ("-g", "--segment"):
            PARAMS['segment'] = arg
        elif opt in ("--sort"):
            PARAMS['sort'] = arg

def get_service(api_name, api_version, scope, client_secrets_path):
  """Get a service that communicates to a Google API.

  Args:
    api_name: string The name of the api to connect to.
    api_version: string The api version to connect to.
    scope: A list of strings representing the auth scopes to authorize for the
      connection.
    client_secrets_path: string A path to a valid client secrets file.

  Returns:
    A service that is connected to the specified API.
  """

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      parents=[tools.argparser])
  flags = parser.parse_args([])
  flow = client.flow_from_clientsecrets(
      client_secrets_path, scope=scope,
      message=tools.message_if_missing(client_secrets_path))
  #storage = file.Storage(api_name + '.dat')
  storage = file.Storage(re.sub('json$', 'dat', PARAMS['json']))
  credentials = storage.get()
  if credentials is None or credentials.invalid:
    credentials = tools.run_flow(flow, storage, flags)
  http = credentials.authorize(http=httplib2.Http())

  return build(api_name, api_version, http=http)

def get_profile_id(service, accountname, propertyname, profilename):
    accountId = None
    propertyId = None
    profileId = None

    accounts = service.management().accounts().list().execute()
    if accounts['items']:
        for account in accounts['items']:
            if accountname.lower() == account['name'].lower():
                accountId = account['id']

        if accountId != None:
            properties = service.management().webproperties().list(
                accountId=accountId).execute()
            if properties['items']:
                for property in properties['items']:
                    if propertyname.lower() == property['name'].lower():
                        propertyId = property['id']

                if propertyId != None:
                    profiles = service.management().profiles().list(
                        accountId=accountId,
                        webPropertyId=propertyId).execute()
                    if profiles['items']:
                        for profile in profiles['items']:
                            if profilename.lower() == profile['name'].lower():
                                profileId = profile['id']
    return profileId

def get_results(service, profile_id, start_date, end_date, filters, dimensions, metrics,
                segment, start_index, sampling_level, max_results, sort):
    # Use the Analytics Service Object to query the Core Reporting API
    # for the number of sessions in the past seven days.
    return service.data().ga().get(
        ids='ga:' + profile_id,
        start_date=start_date,
        end_date=end_date,
        max_results=10000 if max_results=='' else max_results,
        filters=None if filters=='' else filters,
        dimensions=None if dimensions=='' else dimensions,
        metrics=None if metrics=='' else metrics,
        segment=None if segment=='' else segment,
        start_index=None if start_index=='' else start_index,
        samplingLevel=None if sampling_level=='' else sampling_level,
        sort=None if sort=='' else sort
    ).execute()

def export_results(results, file):
    with open(file, 'wb') as f:
        if PARAMS['dimensions']:
            f.write(re.sub('ga\\:', '', PARAMS['dimensions'] + ','))
        if PARAMS['metrics']:
            f.write(re.sub('ga\\:', '', PARAMS['metrics']) + '\n')
        for row in results['rows']:
            writeline = '"'
            for word in row:
                writeline += word + '","'
            f.write(re.sub('(,")$', '\n', writeline))
    f.close()

def print_results(results):
  # Print data nicely for the user.
  if results:
    print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
    print 'Total Sessions: %s' % results.get('rows')[0][0]

  else:
    print 'No results found'

def main():
    service = get_service('analytics', 'v3', SCOPE, PARAMS['json'])
    profileId = get_profile_id(service, PARAMS['account'], PARAMS['property'], PARAMS['profile'])
    query_data = get_results(service, profileId, PARAMS['start_date'], PARAMS['end_date'],
                             PARAMS['filters'], PARAMS['dimensions'], PARAMS['metrics'],
                             PARAMS['segment'], PARAMS['start_index'], PARAMS['sampling_level'],
                             PARAMS['max_results'], PARAMS['sort'])
    export_results(query_data, PARAMS['output'])

if __name__ == '__main__':
    argvs = sys.argv[1:]
    if len(argvs) == 0:
        print_help()
    elif argvs[0] in ('-h', '--help'):
        print_help()
        sys.exit()
    elif argvs[0] in ('-s', '--setup'):
        arg = []
        setup_file_name = ''
        if argvs[1:]:
            setup_file_name = argvs[1]
        else:
            setup_file_name = 'setup.txt'
        with open(setup_file_name, 'rb') as f:
            for line in f:
                if line != '':
                    argTokens = re.sub('\n', '', line).split(' : ')
                    if len(argTokens) == 2:
                        arg.append('--' + argTokens[0])
                        arg.append(argTokens[1])
        f.close()
        setup_params(arg)
        main()
    else:
        setup_params(argvs)
        main()