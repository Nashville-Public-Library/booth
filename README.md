# booth
 a simple web app to assist with TL booth schedule

 ----

 DON'T FORGET TO SET ENVIRONMENT VARIABLES AS EXPLAINED IN THE `.EBEXTENSIONS` SECTION BELOW

 ## notes on deploying to AWS EB

 ### Health Checks

 DO THIS AS SOON AS YOU DEPLOY to EB

 First, some Background. When you go to the home route (`/`), unless the TL is closed, the first thing that happens is we're calling up Selenium to do its thing. It takes time for Selenium to load a page, log in, click a few links, and search through the HTML. Sometimes up to 10+ seconds.

 EB's health check feature defaults to returning a warning if the app doesn't give a proper response within a few seconds. It keeps sending more checks to the server, and eventually this creates a loop which consumes more and more of the CPU & RAM, and the instance eventually becomes unusable.

 The fix for this is to adjust the health checks paramaters. Once you deploy the app on EB, head to the EC2 dashboard. On the left column, go down to the Load Balancing tab, and under that click Target Groups. Once there, select the target group. Under the Health Checks tab, click Edit. Once there, (you may need to select Advanced Settings) increase both the timeout and interval options. As of this writing, Timeout is at 20 and Interval is at 25 (interval must be higher than Timeout).

 You need to make these change immediately after deploying, or else the health checks will begin failing immediately and the resources will start draining. 

 It SEEMS you only need to do this when you first create your EB environment. In other worse, if you're just updating your code and redeploying, the previous settings for this will remain. AGAIN, you don't need to go do this each time you update your source code. I'm just putting this note here for future reference. It took a looooong time to figure out why the app worked for only the first few minutes it was deployed.

 ### Selenium

 I tried uploading a linux binary of the chrome driver at root of project and passing in that location when creating the `driver = webdriver.Chrome(...)` instance. this did not work. long story short, I found [selenium's preferred method](https://www.selenium.dev/documentation/webdriver/getting_started/install_drivers/#1-driver-management-software) is using [webdriver manager](https://github.com/SergeyPirogov/webdriver_manager). this will install it for you, and also keep it up to date.

 even still, when running this on EC2, chrome fails to start properly. it seems this is because webdriver manager does install the web driver, but not Chome itself. so you need to add a [predeploy hook](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/platforms-linux-extend.html) to do this; that's what the bash script in `.platform\hooks\predeploy\` is for. note that Amazon's version of Linux doesn't use `apt/apt-get` for packages; it uses `yum`.

 once I got this working, Chrome still complained. the error was `Chrome failed to start: exited abnormally.` this has something to do with the virtual display settings. the solution was provided on [SO](https://stackoverflow.com/questions/22424737/unknown-error-chrome-failed-to-start-exited-abnormally). also note that according to one commentator, `no-sandbox` needs to be passed in as the first argument (I don't know why.)

 ### .ebextensions

 It SEEMS all EC2 instances default to a different time zone (It's UTC, i think). We could deal with this in the code directly, but that seems messy; we don't want to have to change things depending on where it's run. instead we're able to change our instance's timezone with a `.config` file. This is the `change_timezone.config` file in the `.ebextensions` folder.

 Another config file, `options.config`, sets the environment variables, so our VIC username/password are not stored in the source.

 IMPORTANT: If you do not see a `options.config` file inside the `.ebestensions` folder it's because I decided to `gitignore` this file. here's what the file should look like:

    option_settings:
      - option_name:  VIC_user
        value:  this_is_your_VIC_username
      - option_name:  VIC_password
        value:  this_is_your_VIC_password

Nothing in this file should be enclosed in quotes.

### Misc

don't forget to continually update your `requirement.txt` file as you go (via `pip freeze > requirements.txt`).
