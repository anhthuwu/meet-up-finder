# NoReply

*NoReply* is a project created by team 2-31 that intends to connect people by helping them find meet-ups of various types of events that happen nearby to attend. Users can post events as well as search for available events within a specified distance from their location.

## Demo
Please visit our website https://noreply231.herokuapp.com/. 

## Features
1. **Search Events:** There is a search bar on the left side of the page. The users can search an event by the name, description, location, and hostname.
2. **Post Events:** There is a “+” button to the right of the event search bar. The users can post events by clicking on the button, enter general information about the event, and click submit.
3. **View All Events:** Click on the "View All Events" button. All created events will show up as a list on the left side of the screen. In the meanwhile, the events will show up as a marker on the map.
4. **Starred Events:** There is a “View  Starred Event” button under the event search bar. The users can view events that are currently starred by clicking on this button. There is a “✩” button to the right of each event name. The users can draw attention to an event by clicking that button. The “✩” button will be red-bordered if the event is already starred. Similarly, the users can unstar a starred event by clicking the red-bordered star button.
5. **Find Events Nearby:** There is a “View Events Near Me” button next to the “View Starred Event”. The users can view the event nearby by inputting his/her location under the “Your Location” panel. Users can also change the distance parameter of the search by inputting a distance of his/her choice. The default location will be University of Virginia, and the user will be able to see events around the location within a default distance of 1000 meters. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install *NoReply*.

```bash
pip install -r requirements.txt
```
## Built With
1. [Django](https://www.djangoproject.com/)
2. [Bootstrap](https://getbootstrap.com/)
3. [Google Map API](https://cloud.google.com/maps-platform/?utm_source=google&utm_medium=cpc&utm_campaign=FY18-Q2-global-demandgen-paidsearchonnetworkhouseads-cs-maps_contactsal_saf&utm_content=text-ad-none-none-DEV_c-CRE_460848633508-ADGP_Hybrid%20%7C%20AW%20SEM%20%7C%20BKWS%20~%20Google%20Maps%20API-KWID_43700033921822012-aud-669071680939%3Akwd-1952727095-userloc_9008337&utm_term=KW_google%20map%20api-ST_google%20map%20api&gclid=CjwKCAiA2O39BRBjEiwApB2Ikgza1L9DxeM2uZX1WdznA3fWzDRJTcsiwx9EVYMqH5Dt95GUmQ8HxRoC5AwQAvD_BwE)

## Development
1. Clone the project into your local PC and open up the project
```git
git clone https://github.com/uva-cs3240-f20/project-2-31.git
```

2. Checkout to the ```dev``` branch: we will develop on the sub branches and leave master as the production branch (AKA: we don't touch master until we merge it with other development branches!!)
```git
git checkout dev
```

3. Download all the necessary files to run this project
```bash
pip install -r requirements.txt
```

4. Make migrations
```bash
python manage.py events
```

5. Migrate
```bash
python manage.py migrate
```

6. Create superuser and follow its default prompt
```bash
python manage.py createsuperuser
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
