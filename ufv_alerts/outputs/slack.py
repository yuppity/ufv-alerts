from ..handler_helpers import alert_handler
from ..http import simple_post

@alert_handler
def send_to_slack(config, alert, *args, **kwargs):

    payload = {
        'username': 'UniFiVideo',
        'channel': config.get('channel', '#general'),
    }

    if 'icon_url' in config:
        payload['icon_url'] = config['icon_url']
    else:
        payload['icon_emoji'] = ':camera:'

    datetimes = [
        alert['exec_datetime'],
        alert['alert_datetime'],
    ]

    payload['text'] = 'Motion detected on camera {} at site {} (`{}`)'.format(
        alert['camera'],
        alert['site'],
        sorted(datetimes)[0].strftime('%Y-%m-%dT%H:%M:%S'))

    simple_post(config['webhook_url'], data=payload, as_json=True)
