mobilemoney.py
==========

A modern, easy to use, feature-rich, and async ready API wrapper for MobileMoney written in Python.

Key Features
-------------

- Modern Pythonic API using ``async`` and ``await``.
- Optimised in both speed and memory.

Installing
----------

**Python 3.8 or higher is required**

To install the library, you can just run the following command:

.. code:: sh

    # Linux/macOS
    python3 -m pip install -U mobilemoney.py

    # Windows
    py -3 -m pip install -U mobilemoney.py

To install from github repository, do the following:

.. code:: sh

    $ git clone https://github.com/rewriteapi/mobilemoney.py
    $ cd mobilemoney.py
    $ python3 -m pip install -U .


Quick Example
--------------

.. code:: py

    import mobilemoney
    import asyncio

    #NOTICE : the library is working in both side (Production and Sandbox), 
    #for Production environement don't use the is_sandbox() method and 
    #make sure to replace credential correctly 

    async def main():
        subsciption_key = 'COLLECTION_OR_DISBURSEMENT_CREDENTIAL_MAKE_SURE_TO_REPLACE_IT_CORRECTLY'

        user = mobilemoney.Client()

        #switchh to sandbox env
        user.is_sandbox()

        #Creating user and getting Key in sandbox env using Collection credential
        uuid = user.get_reference_id()
        print(uuid)


        api_user = await user.create_api_user(uuid, subsciption_key)
        print('-------- creating api user----------')
        print(api_user)

        resp, api_user_details = await user.get_api_user(uuid, subsciption_key)
        print('-----------getting api user------------')
        print(api_user_details)

        resp, api_key = await user.create_api_key(uuid, subsciption_key)
        print('---------api key-----------')
        print(type(api_key))
        print(api_key)


        basic_auth = user.basic_token(uuid, api_key["apiKey"])
        print('------------Basic auth---------')
        print(basic_auth)

        #Initialising Collection product
        collect = user.collection(subsciption_key)

        #creating access token
        resp, access_token = await collect.create_access_token(basic_auth)
        print('---------creating access token-----------')
        print(access_token)

        #convert it to bearer token
        bearer_token = user.bearer_token(access_token['access_token'])

        #request to pay
        body = {
            "amount": "5",
            "currency": "EUR",
            "externalId": "45464546454",
            "payer": {
                "partyIdType": "MSISDN",
                "partyId": "87937389"
            },
            "payerMessage": "BUY THING",
            "payeeNote": "THANKS"
            }
            
        resp, req_to_pay = await collect.request_to_pay(bearer_token, user.get_reference_id(), api_user_details['targetEnvironment'], body)
        print('-----------------Request to pay-----------------')
        print(resp)
        print(req_to_pay)
        if resp:
            print('Successfull')
        else:
            print('Not worked')

        #withdraw
        resp, with_req = await collect.withdraw(bearer_token, user.get_reference_id(), api_user_details['targetEnvironment'], body)
        print('--------------req to withdraw------------------------')
        print(resp)
        print(with_req)
    


    asyncio.run(main())

Links
------

- `Documentation <https://mobilemoneypy.rewriteapi.cm>`_
- `Official Discord Server <https://discord.gg/>`_
- `Website <https://rewriteapi.cm>`_