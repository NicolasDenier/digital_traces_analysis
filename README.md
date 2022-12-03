# Digital traces Analysis
**Small flask web application hosted on Deta and linked with Google Analytics**

## Set up
After following Deta's tutorial to [set up a micro](https://docs.deta.sh/docs/micros/getting_started), a [Google Analytics](https://analytics.google.com/analytics/web/) account is created and linked to the deployed web application.  

## App
The app is available at [https://lhkxlc.deta.dev/](https://lhkxlc.deta.dev/)   
The home page contains some text and a link that redirect to a sub path called [click](https://lhkxlc.deta.dev/click), where there is nothing much to see.  
![home](images/home.png)

## Analytics
A few different sessions are opened to simulate various users:

| OS      | Browser | Country     |  
|---------|---------|-------------|  
| Linux   | Opera   | France      |  
| Linux   | Opera   | Indonesia   |  
| Linux   | Firefox | France      |  
| Linux   | Chrome  | France      |  
| Android | Opera   | France      |  
| Android | Opera   | Netherlands |  

Clicking, reloading pages, staying, for each session will leave digital traces that can be visualized on Google Analytic's dashboard.  
It has indeed identified distinct users, without them to connect, simply by the unicity of all their digital traces combined:  

![os](images/os.png)
![browser](images/browser.png)
![countries](images/countries.png)

An interesting plot of real time traffic shows the number of active users, how much and when they click, and which urls are the most viewed (here the home page is loaded more times than the /click sub path).  

![](images/real-time.png)

Among the various insights available, the total activity can give a good idea of the peak hours.  

![](images/total-activity.png)

