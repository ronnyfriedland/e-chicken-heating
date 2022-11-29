"""
Control heat pad
"""
from flask import Flask

from _cron import create_cron, list_crons, datetime, ExecutionPlan

next_execution = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

create_cron("e-chicken-heating-check-job", "/usr/local/bin/python /usr/src/app/check.py --verbose",
            start=next_execution,
            interval=ExecutionPlan.DAILY)

app = Flask(__name__)


@app.route('/crons')
def crons():
    """
    List crons
    """
    return '<br/>'.join(list_crons())

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
