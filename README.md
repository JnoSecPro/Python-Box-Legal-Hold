ABOUT
This program was written with the intention of creating an executable for the Windows platform to enable teams responsible for eDiscovery and required to put legal holds on Box accouts.
It's a great way to help with the learning curve for new Administrators unfamiliar with the Box Cloud storage platform and the process of creating legal holds. This is a great tool to use
if there is a backlog of legal holds that need to be placed. You will need to set up the app in the Box admin console and Box developer console. 

WHAT YOU NEED:
- Box admin privileges with access to governance.
- Box Client ID and Client Secret (set up a Box app in admin console and dev console https://developer.box.com/guides/mobile/ios/quick-start/configure-box-app/).
- You will need to create an OAuth 2.0 Redirect URI for authenticating to Box and you WILL need to add it to the Python Code before running it or it will fail..
- Content actions for your application. You will need to open a ticket with Box to enable governance for the that app.
  - Read all files and folders stored in Box
  - Manage Users
  - Manage retention policies
  - Manage enterprise properties
- Text document of email addresses to use to assign to legal hold policies following the creation of the policy.
