Edit the zid.json file and include the necessary data from Zid Partner Platform,
On Zid you should also change the redirect url to your endpoint
1. Open a browser and login to Zid
2. Access the login endpoint /zid/login (Sometimes you have to open it twice)
3. Zid will ask for permissions for the scopes you set on Zid Partner platform
4. Once you allow the permissions, the access codes will be sent to the callback url - /zid/callback. I set it up so that it is saved to the file credentials.json
5. Use the data in the credentials.json to access the API.
