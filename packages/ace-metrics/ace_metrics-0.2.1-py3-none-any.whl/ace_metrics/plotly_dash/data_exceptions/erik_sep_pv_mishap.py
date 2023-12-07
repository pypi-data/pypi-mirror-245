"""In September 2020, ATOS miss-configured the PAN FW and we were alerting on VVV voice traffic hitting our network.
This event caused hundreds of alerts over a few weeks. We collectively dispositioned these alerts as PV.
Erik apparently made a disposition mistake and took it upon himself to correct it.

On October 5th, Eric dispositioned 445 of these alerts, at the same time, as PV.

Of the 445 alerts Erik dispositioned, the first one became an alert at “2020-09-26 05:36:14 -0400” and the last one became an alert at “2020-09-30 10:15:32 -0400”.

This mass disposition greatly skewed all time based metrics for the month of September.

This is why it’s important for us to update dispositions as soon as we know the disposition should be changed.
"""

import logging
import pandas as pd

def remove_ek_september_pv_skew(alerts: pd.DataFrame) -> pd.DataFrame:
    """remove the alerts Erik mass dispo'd"""
    if '202009' not in  alerts.index:
        return alerts
    # Assuming alerts are currently indexed by month
    alerts.reset_index(level=0, inplace=True)
    ek_445 = alerts[ (alerts.disposition == 'POLICY_VIOLATION') 
                 & (alerts.month == '202009')
                 & (alerts.disposition_user_id == 24) 
                 & (alerts.disposition_time.astype(str).str.contains('2020-10-05 18') )]

    assert len(ek_445) == 445

    logging.info(f"removing ekovacs mass late pv dispo skewed alerts.")

    df_new = alerts.merge(ek_445, how='left', indicator=True)
    alerts = df_new[df_new['_merge'] == 'left_only']
    # set index back
    alerts.set_index('month', inplace=True)
    return alerts
