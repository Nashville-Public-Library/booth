# booth

[ntlbooth.com](http://ntlbooth.com)

 a simple web app to assist with TL booth schedule

 ----

 ## Read this before deploying!

 ### Health Checks

 When we initially created this app, the home route `/` would immediately call up Selenium to do its thing. The problem was: that was a slow process; we call up Selenium, it pulls up the scheduling website, logs in, clicks a button, then scrapes the HTML and returns the data, then we do our processing on the data, then return the HTML. It could take 8+ seconds to do all of this, only after which app returns a proper HTTP response.

 We've since changed this to have a 'landing' page, which will indeed immediately return a response, then redirects to start the Selenium process. Still, though, I'd prefer the Health Check to avoid the cumbersome part of this app. I just want to know whether the server is up or not.

 The fix for this is to adjust the health checks paramaters. Once you deploy the app on EB, head to the EC2 dashboard. On the left column, go down to the Load Balancing tab, and under that click Target Groups. Once there, select the target group. Under the Health Checks tab, click Edit. Once there, (you may need to select Advanced Settings) change the Health check path to `/health`. I added this route specifically for this purpose. When you visit the URL, Flask immediately returns some plain text, which takes no time.

 You need to make this change immediately after deploying. It SEEMS you only need to do this when you first create your EB environment; if you're just updating your code and redeploying, the previous settings for this will remain. In other words, you don't need to go do this each time you update your source code. I'm just putting this note here for future reference.

 ### Selenium

 I tried uploading a linux binary of the chrome driver at root of project and passing in that location when creating the `driver = webdriver.Chrome(...)` instance. this did not work. long story short, I found [selenium's preferred method](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-driver-management-software) is using [webdriver manager](https://github.com/SergeyPirogov/webdriver_manager). this will install it for you, and also keep it up to date with the latest version.

 even still, when running this on EC2, chrome failed to start properly. it seems this is because webdriver manager does install the web driver, but not Chome itself. so you need to add a [predeploy hook](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html) to do this; that's what the bash script in `.platform\hooks\predeploy\` is for. note that Amazon's version of Linux doesn't use `apt/apt-get` for packages; it uses `yum`.

 once I got this working, Chrome still complained. the error was `Chrome failed to start: exited abnormally.` this has something to do with the virtual display settings. the solution was provided on [SO](https://stackoverflow.com/questions/22424737/unknown-error-chrome-failed-to-start-exited-abnormally). also note that according to one commentator, `no-sandbox` needs to be passed in as the first argument (I don't know why.)

 ### .ebextensions

 It SEEMS all EC2 instances default to a different time zone (It's UTC, i think). We're able to change our instance's timezone with a `.config` file. This is the `change_timezone.config` file in the `.ebextensions` folder.

 Another config file, `options.config` in the `.ebextensions` folder sets the environment variables, so our VIC credentials are not stored in the source.

 IMPORTANT: We are ignoring via `.gitignore` the `options.config` file inside the `.ebestensions` folder. Here's what the file should look like:

    option_settings:
      - option_name:  VIC_user
        value:  this_is_your_VIC_username
      - option_name:  VIC_password
        value:  this_is_your_VIC_password

Nothing in this file should be enclosed in quotes.

Alternatively, you can set environment variables from the EB console. Just make sure to set them immediately upon deployment.

### Misc

Don't forget to continually update your `requirement.txt` file as you go (via `pip freeze > requirements.txt`).
