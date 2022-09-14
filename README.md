This tool's purpose is to calculate course grades in Blackboard without any sort of LMS interaction to provide a more efficient method of viewing grades.
I began development of this tool on February 3rd 2021, and finished on May 18th 2021,
but because of constant updates to the Blackboard LMS, the tool does not function as expected and contains several bugs of which I will resolve soon.

To use this tool, you will need to download and run this source code locally on your machine. This is because the Selenium library uses chromedriver for
the web automation and without it, the program won't function.

Steps:

1. Download the code and chromedriver onto your local machine.
2. Ensure that chromedriver is compatible with your version of Chrome. This version of chromedriver works on Chrome v105. 
If it isn't, the program will throw an error, saying chromedriver is outdated. To fix this, navigate to https://chromedriver.chromium.org/downloads 
and download the version of chromedriver that matches Chrome's version.
3. You may need to install several libraries like BeautifulSoup, requests, etc to properly run the tool. 
4. That's it! You should be able to run the program successfully, assuming you have valid credentials. 

If you aren't enrolled or associated with the University of Windsor, you won't be able to see the tool's function as you will need vaild credentials to 
authenticate with Blackboard LMS. 
