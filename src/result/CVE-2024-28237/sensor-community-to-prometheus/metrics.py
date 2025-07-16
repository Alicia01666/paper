import re
import requests

def generate(sensors: list[str]) -> str:
    node_query = '(' + 'OR'.join(f''' "node" = '{sensor}' ''' for sensor in sensors) + ')'

    query = f'''
        SELECT time, last("temperature") AS "temperature"
        FROM "autogen"."sensors" WHERE {node_query} group by type, node;

        SELECT time, last("humidity") AS "humidity"
        FROM "autogen"."sensors" WHERE {node_query} group by type, node;

        SELECT time, last("pressure") / 100 AS "pressure"
        FROM "autogen"."sensors" WHERE {node_query} group by type, node;

        SELECT time, last("signal") AS "wifi_signal" FROM "autogen"."sensors" WHERE {node_query} group by node;
        SELECT time, last("quality") AS "wifi_quality" FROM "autogen"."sensors" WHERE {node_query} group by node;
    '''

    query += ''.join(f'''
        SELECT time, last("{sensor_type}_P0") AS "{sensor_type}_pm1"
        FROM "autogen"."sensors" WHERE ({node_query} AND "type" = '{sensor_type}') group by node;

        SELECT time, last("{sensor_type}_P2") AS "{sensor_type}_pm2_5" 
        FROM "autogen"."sensors" WHERE ({node_query} AND "type" = '{sensor_type}') group by node;

        SELECT time, last("{sensor_type}_P1") AS "{sensor_type}_pm10" 
        FROM "autogen"."sensors" WHERE ({node_query} AND "type" = '{sensor_type}') group by node;

        ''' for sensor_type in ['SDS011', 'PMS', 'SPS30', 'NPM', 'HPM']
    )

    query = re.sub(r'(\n\s*)', '', query)

    output = ''
    r = requests.get('https://api-rrd.madavi.de:3000/grafana/api/datasources/proxy/uid/zVHIU1WMz/query?db=sensorcommunity&epoch=ms', params={"q": query})
    r.raise_for_status()
    for result in r.json()['results']:
        if 'series' in result:
            for record in result['series']:
                m_tags = record['tags']
                m_type = record['columns'][1]
                m_time = record['values'][0][0]
                m_value = record['values'][0][1]

                if '_pm' in m_type:
                    device_type, m_type = m_type.split('_', 1)
                    m_tags['type'] = device_type

                tag_str = ','.join(f'{k}="{v}"' for k,v in record['tags'].items())

                output += f'pm_sensor_{m_type}{{{tag_str}}} {m_value} {m_time}\n'
        elif 'error' in result:
            print('error:', result)
    return output