# PlataBot

 Discord bot that compares the prices of steam store prices. It currently only supports two countries, Chile and Argentina. This is mainly because Chile is the country where I live in and it blew my mind how different the steam store prices between two neighbouring countries can be. It was made to show this abysmal difference. This project was made around mid 2020 and was just uploaded now. Some code was updated to be able to work properly again, and when I have the time I will update it to recover the lost search feature that I talk about in the discussion.
 
 # Usage
 
 This bot's prefix is just a dot (.) and it currently features two commands:
 
 ## .precio
 
 Receives the name of a game. It is not case senstive, as shown in this example:
 ![imagen](https://user-images.githubusercontent.com/60141816/198533181-c709cb15-cfc2-4703-97c0-f10bde20ed07.png)
 
 The written output can be translated as:
 > Base Game
 >
 >
 > **Price in Argentina**
 >
 > $55.00 pesos argentinos (ARS) *argentinian currency*, which are $333 pesos chilenos (CLP) *chilean currency*
 >
 > **Price in Chile**
 >
 > $2,750 CLP which are $453.69 ARS
 >
 >**Price difference**
 >
 > This Base Game is cheaper in Argentina. It is about 87.89% more cheaper in Argentina than Chile.
 
 ## .tasa
 
 Sends a message showing the current exchange rates of Chile and Argentina, having USD as base currency.
 
 ![imagen](https://user-images.githubusercontent.com/60141816/198537810-f286ba70-c64e-4644-930e-e727a2a397eb.png)

# Discussion

This bot used to have a search feature, in which the user could input a message and it showed a list of possible matches, as shown in these examples bellow:

![imagen](https://user-images.githubusercontent.com/60141816/198538881-b83ab31f-b85a-4999-aea3-75d33cb731d9.png)

![imagen](https://user-images.githubusercontent.com/60141816/198539450-d3deef13-80c0-4d30-9d17-0330abf35d57.png)

To get those search results I web scraped [steamDB](https://steamdb.info/) using a python implementation of [Selenium](https://selenium-python.readthedocs.io/) and [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) to get around the dynamic nature of the website. At that time I didn't know they had such strict policies surronding web scraping, until my friends (users of this bot) told me the bot didn't work. As of today, [they totally prohibited web scraping in their website](https://steamdb.info/faq/#can-i-use-auto-refreshing-plugins-or-automatically-scrape-crawl-steamdb).

But luckily, they provided some workarounds for this. I might be able to get the same results as them, [following this guide.](https://steamdb.info/faq/#how-are-we-getting-this-information) But that might suggest that I'll have to implement a search algorithm, which I'll probably do in the future when I get spare time.
