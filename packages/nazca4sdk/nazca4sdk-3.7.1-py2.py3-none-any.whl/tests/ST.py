from nazca4sdk.sdk import SDK

sdk = SDK(False)

print(sdk.modules)

help(sdk.variables.read)

# vars = sdk.variables.read(module_name="symulator", variable_names=["V1"], start_date="2023-12-01TOO:OO:00", end_date="2023-12-01TO1:OO:00")
# print(vars)

print(sdk.variables.read('E-I-S-A40', ['V1'], time_amount = 10, time_unit = 'MINUTE'))