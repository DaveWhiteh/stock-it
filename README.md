# Stock-!t

---

## About

Stock !t, is a website that allows users to create multiple stock lists for both personal and small business use. The user can create an unlimited amount of locations, for example, kitchen, garage, racking 1, racking 2, etc. Then in these locations you can create stock lists which will help the user keep on top of how many items they have, noting the name, description, quantity, date of purchase and expiry date.

The site will be targeted towards individuals who require a basic yet effective way to manage inventory, whether that be from a personal perspective or a small business user.

***Click **[here]()** to view the live website.***

---

## User Experiences (UX)

### **User Stories**

**As a First-time User:**

+ I want to clearly understand the purpose of the site, when arriving at the home page
+ I want the website to be responsive so it can be used on any device
+ I want the registration process to be smooth and easy

**As a Returning User:**

+ I want to easily login to my account
+ I want to be able to create, edit and delete locations
+ I want to be able to create, edit and delete stock lists
+ I want to be able to access the website from any device

**As a Business Owner:**

+ I want the user to be able to see only there stock lists when they are logged in
+ I want to create a website that looks aesthetically pleasing on any device
+ I want the user to experience a smooth and easy process when creating, editing or deleting both locations and stock lists

### **Strategy**

**Site Goals**

This project is based around creating a fully functional website that allows users to manipulate data records, utilising HTML, CSS, Javascript, Python, Flask and mongoDB.

The main goal of the website is to allow users to create stock lists, that only they can see once they register for an account. They will need to be able to create, read, update and delete (CRUD functionality) both locations and stock lists. The website will need to be of a professional outlay with an attractive design that is both modern and simple to navigate. The site will need to be fully responsive allowing for the site to look great on all devices.

### **Scope**

The main features for this website are to provide users with the ability to register for an account, then login and access there very own dashboard. Then by utilising full crud functionality they will be able to create, read, update and delete both locations and items.

**Homepage**

The homepage is where the user will see a 3/4 height hero which will clearly state the company name and simply what the website is about. The homepage as a whole will be made up of short and direct captions and sentences that get straight to the point of what Stock-!t is all about and what it has to offer a new user. Scrolling down the page at two points are buttons, one that will take the user to the registration page and the other to the login page. This clearly shows the simple yet thought out navigation that has been put in place.

**Login / Register**

Both these pages have been made to look and feel the same for consistency. The colours used are in keeping with the theme of the site and are bold to make them stand out. Both have a centralised form that is easy to fill out with a button below the form to submit. Below both forms will be a link that takes them to the other page respectively, should they have gone to the wrong one in the first place.

**Dashboard**

Once the user has either registered or logged in as an existing user they will be instantly redirected to there own dashboard page. This page will add pastel colouring to the look, which will help break up and distinguish between the selling of the web application and the application itself. By default there will be two card panels, one for locations which will show the current user how many locations they have created, and one for items which will provide them with a total count of items they have. Both panels will be clickable which will be a link to both the locations and items pages respectively.

**Locations**

The locations page will provide the user a place to see all there locations that they have created. There will be a red banner that will contain the locations title and a 'Add Location' button which will link to a new page where the user can add a new location. Below the red banner will be a smaller banner that will contain all flash messages. Below this banner there will be the actual list of locations. Very simple each location element will contain the location name on the left and three dots on the right, which will be a drop down link that will allow the user to edit or delete that particular location.

**Items**

Using the same layout as the locations page. The only differences will be that the button on the red banner will be for adding an item. Within the list of items, each element will now contain an arrow icon before the item name, that will allow the user to click and therefore activate a collapsible section. This section below will contain the text, quantity, dates, etc.

### **Structure**

The structure of the site will be of multiple webpages that will be linked throughout, via the use of buttons and other elements. The user will have clear instructions and be able to clearly identify what they are required to do throughout the site. The navigation throughout will allow the experience to be fluid and should they run into trouble at any point they will be directed straight back to the home page or dashboard depending on whether they are logged in or not.

### **Skeleton**

Figma has been used to create the design layouts for this site. Figma is a perfect creative tool that allows for a much more extensive design layout to be created rather than just wireframes. These designs allow the whole process of the site creation to be easier and smoother knowing where each element goes and the colours of each element within the site.

Mobile (360 x 640)<br>
Tablet (1024 x 1366)<br>
Desktop (1920 x 1080)

<details>
<summary>Design Layout</summary>
<img src="static/images/readme/design_layout.jpg" width="500">
</details>

### **Surface**

**Colour**

The colours were chosen using color-hex.com. A red-blue combination was searched for with this particular palette chosen due to the addition of pastel colours. The pastel colours were always going to be utilised within the actual web application. This was important to have the main selling point of the web application to use the bold branded colours and then for the application to have a softer feel once the user had signed up.

Tints and shades of these colours were found at [maketintsandshade.com](https://maketintsandshades.com/).

<details>
<summary>Colour Palette</summary>
<img src="static/images/readme/colour-palette.jpg" width="250">
</details>

**Typography**

Chosen throughout this site was the font Poppins. It was chosen because of its simple look and very easy to read. It is also a very versatile font that has many font weights. This font is available at [Google Fonts](https://fonts.google.com/).

**Images**

The images within the home page were chosen specifically for there relation to the actual web application. They will have a huge impact as to the selling of the app giving the user a perfect visual as to the use of the application. All the sources where the images came from can be found within the [credits](#credits) section.

**Icons**

The icons within the site can be found at [Font Awesome](https://fontawesome.com/). The main icons within the site are the social media links that can be found on each page in the footer. These give the opportunity for the user to go straight to these social media sites to find out the most recent info regarding the business and the web application. The other icon is the arrow that is used within the items collapsible list.