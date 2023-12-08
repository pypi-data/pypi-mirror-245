from nazca4sdk.sdk import SDK

sdk = SDK(False)
# print(sdk.variables.read('symulator', ['V1'], time_unit='HOUR', time_amount=5))
#
# print(sdk.variables.pivot('symulator', ['V1', 'V2'], time_unit='HOUR', time_amount=5))
#
#
# """ Module to communicate with Brain"""
#
# import requests
#
# brain_url = 'http://127.0.0.1:5002'
# requests.post(f'{brain_url}/chat/', json={"user_input": "Ile zużyłem energii w ostatnią godzinę?"})
# print(sdk.npoe.calculate_pt_max_window())
sdk.analytics.energy.calculate_co2_emissions(start_date="2023-11-02T13:00:00.000Z",
                                             end_date="2023-11-10T15:00:00.000Z",
                                             organization_id="08db98ca-9a39-4f74-8e10-ed646e685372",
                                             meters=["alpha_251_dev", "apa260", "test_149"])
