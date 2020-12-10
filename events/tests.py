from django.test import TestCase, Client
from .models import Event, Location
from django.urls import reverse
from .views import find_place
import os 
from django.contrib.auth.models import User
class EventTestCase(TestCase):
    def setUp(self):
        Event.objects.create(name="testname1", location="Rice Hall", date="2020-10-20", time="12:00:00", host="host1",
                             rating=1)
        Event.objects.create(name="testname2", location="Elson Hall", date="2020-11-20", time="13:00:00", host="host2",
                             rating=2)
        Event.objects.create(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)


    # The test should pass because the format of date is right
    def test_get_one(self):
        two = Event.objects.get(name="testname2")
        self.assertEqual(two.location, "Elson Hall")

    def test_getAll(self):
        all_events = Event.objects.all()
        self.assertIsNotNone(all_events)

    def test__str__(self):
        obj1 = Event(name="testname2", location="Rice Hall", date="2020-10-20", time="12:00:00", host="host1", rating=1)
        self.assertIs(obj1.__str__(), "testname2")

    def test__str__wrong(self):
        obj1 = Event(name="testname2", location="Rice Hall", date="2020/10/20", time="12:00:00", host="host1", rating=1)
        self.assertIsNot(obj1.__str__(), "testname1")

    def test__location__(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIs(obj1.location, "Thornton Hall")

    def test__location__wrong(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIsNot(obj1.location, "Rice Hall")

    def test__date__(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIs(obj1.date, "2020-11-21")
    
    def test__date__wrong(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIsNot(obj1.date, 2)
    
    def test__time__(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIs(obj1.time, "11:00:00")

    def test__time__wrong(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIsNot(obj1.time, "hello")

    def test__host__(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIs(obj1.host, "host3")

    def test__host__wrong(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIsNot(obj1.host, "host1")

    def test__rating__(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIs(obj1.rating, 2)

    def test__rating__wrong(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertIsNot(obj1.rating, 4)

    def test__count__(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertEqual(len(Event.objects.all()), 3)
    
    def test__count__wrong(self):
        obj1 = Event(name="testname3", location="Thornton Hall", date="2020-11-21", time="11:00:00", host="host3", rating=2, description="not much...", addedTOMyEvent=True, lng=-70, lat=30)
        self.assertNotEqual(len(Event.objects.all()), 4)

class LocationTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='zichao', password='12345')
        self.user2 = User.objects.create_user(username='chao', password='12345')

        self.obj1 = Location.objects.create(user=self.user1)
        self.obj2 = Location.objects.create(user=self.user2, location="Barracks Road", lat=38, lng = -78, distance = 1200)

    def test_user(self):
        self.assertEqual(self.obj1.user, self.user1)
    
    def test_user2(self):
        self.assertEqual(self.obj2.user, self.user2)

    def test_location(self):
        self.assertEqual(self.obj1.location, "University of Virginia")
    
    def test_location2(self):
        self.assertEqual(self.obj2.location, "Barracks Road")

    def test_lat1(self):
        self.assertEqual(self.obj1.lat, 38.0336)

    def test_lat2(self):
        self.assertEqual(self.obj2.lat, 38)

    def test_lng1(self):
        self.assertEqual(self.obj1.lng, -78.5080)

    def test_lng2(self):
        self.assertEqual(self.obj2.lng, -78)
    
    def test_distance1(self):
        self.assertEqual(self.obj1.distance, 1000)

    def test_distance2(self):
        self.assertEqual(self.obj2.distance, 1200)


class ViewTestCase(TestCase):
    def test_find_place1(self):
        if os.getenv("APIKEY"):
            APIKEY = os.getenv("APIKEY")
            result = find_place("boars head", APIKEY)
            self.assertIsNotNone(result)
    def test_find_place2(self):
        if os.getenv("APIKEY"):
            APIKEY = os.getenv("APIKEY")
            result = find_place("beijing", APIKEY)
            self.assertEqual(result, [])

        
