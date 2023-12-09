# Instagram Profile Importer
The Instagram Profile Importer can import data from instagram profiles by using Instagram's Graph API.

## Prerequisites
Before running this program, you need to have the following:
-An Instagram Business Account or Instagram Creator Account
-A Facebook Page connected to that account
-A Facebook Developer account that can perform Tasks on that Page
-A registered Facebook App with Basic settings configured

## How to Run Locally
To run the program locally, follow these steps:

1. Create a Facebook page: [How to create a Facebook Page](https://www.facebook.com/business/help/1199464373557428?id=418112142508425)
2. Create a business or creater instagram account: [How to set up a business account on Instagram](https://help.instagram.com/502981923235522) or [How to set up a creator account on Instagram](https://help.instagram.com/2358103564437429)
3.Connect your business or creater instagram account to your facebook page: [How to connect or disconnect an Instagram account from your Page](https://www.facebook.com/business/help/connect-instagram-to-page)
4. Create a Facebook Developer account: [Register as a Facebook Developer](https://developers.facebook.com/docs/development/register)
5. Create an app: [How to create an app](https://developers.facebook.com/docs/development/create-an-app/). IMPORTANT: After clicking the "Create App" green button, select other, click next, and then select "None" type.
6. Set up Graph API for your app: Go to "My Apps" at your Facebook Developer account, then click on your app. Scroll down until you see Instagram Graph API , then click on the "Set up" button.
In the menu on the top of the page, select Tools->GraphAPI Explorer.
Get your Instagram user id and Facebook page id by following this guide [Get instagram ID](https://developers.facebook.com/docs/instagram-api/getting-started), you can use the Graph API Explorer instead of "curl -i -X GET" commands. Save these ID's in .env file as EXTERNAL_INSTAGRAM_USER_ID and EXTERNAL_FACEBOOK_PAGE_ID.
Select the following permissions for you app in the GraphAPI Explorer:
pages_show_list,
instagram_basic,
instagram_manage_insights.
Use the generated access token to initialize an InstagramAPI object.
The access token is valid for a limited time, it's possible to generate new tokens in the GraphAPI Explorer.